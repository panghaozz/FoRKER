import json
import requests
import time

#api_key = "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"
api_key = "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"
#api_url = "https://clopenai.cn/v1/chat/completions"
api_url = "https://api.xiaoai.plus/v1/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

with open('question_text/result/token_actvation.jsonl', 'r', encoding='utf-8') as file:
    lines = file.readlines()

processed_lines = []
line_number = 0  # 初始化行号计数器
for line in lines:
    line_number += 1  # 对于每行，行号加一
    data = json.loads(line.strip())
    activations = data["Activate"]
    tokens = data["Token"]
    
    prompt1 = "We're studying model in a neural network. model looks for some particular " \
        "thing in a short document in answering questions. Look at the parts of the document the model activates for " \
        "and summarize in a single sentence what the model is looking for. Don't list " \
        "examples of words!!! One-sentence summary!!!\n\nThe activation format is token<tab>activation." \
        "model finding what it's looking for is represented by a " \
        "non-zero activation value. The higher the activation value, the stronger the match.\n\n" \
        "model 1\n" \
        "Activations:\n" \
        "<start>\n"
    prompt2 = "Explain what the model focuses on in answering the question: \n"
    
    formatted_strings = prompt1
    
    for token, activation in zip(tokens, activations[0].split(',')):
        formatted_strings += f"{token}     {activation}\n"
    
    formatted_strings += "\n" + prompt2

    data_request = {
        "model": "gpt-4-1106-preview",
        "messages": [{
            "role": "user",
            "content": formatted_strings
        }]
    }
    
    attempt = 0
    max_attempts = 50  # 设置最大尝试次数
    success = False
    while attempt < max_attempts and not success:
        response = requests.post(api_url, headers=headers, json=data_request)
        
        if response.status_code == 200:
            explanation = response.json()['choices'][0]['message']['content']
            data['explain'] = explanation
            processed_lines.append(json.dumps(data, ensure_ascii=False) + '\n')
            success = True
            print(explanation)
            print(f"第{line_number}行请求成功，已标记处理。")  # 请求成功时打印消息和行号
            time.sleep(5)
        else:
            print(f"第{line_number}行请求失败，状态码：{response.status_code}，尝试次数：{attempt + 1}")
            attempt += 1
            time.sleep(5)  # 如果请求失败，则暂停30秒
    
    if not success:
        print(f"第{line_number}行请求多次失败，跳过此项。")

with open('question_text/result/result_updated1.jsonl', 'w', encoding='utf-8') as file:
    file.writelines(processed_lines)
