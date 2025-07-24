from openai import OpenAI
import httpx
from prompt_Ablation import E2G_Base_prompt, E2G_Gen_prompt
import json
import time

CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
LEVEL = "hard"
TYPE = "train"
MAX_EPOCH = 2

base_path = "./processed_data/hotpotqa/"
file_path = base_path + str(LEVEL) + "_" + str(TYPE) + ".json"
datasets = []
result_path = "result\\Q&A\\result_" + str(LEVEL) + "_" + str(TYPE) + "_" + str(CurrentTime) + ".txt"
trajectory_path = "result\\Q&A\\trajectory_" + str(LEVEL) + "_" + str(TYPE) + "_" + str(CurrentTime) + ".txt"

client = OpenAI(
    base_url="https://chatapi.a3e.top/v1",
    api_key="sk-0WhUcxdLZuJ2ngPC035016508c5b4aB7B125F8Cd25B70097",
    http_client=httpx.Client( base_url="https://api.xiaoai.plus/v1", follow_redirects=True,),
)
'''
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]
)
'''
# set_prompt = '''你一个有用的助手，现在请告诉我第三任美国总统是谁？'''

def is_number_empty(answer):
    if answer == "":
        return 0
    else:
        return 1

def is_date_empty(answer_data):
    if all(field == '' for field in [answer_data['day'], answer_data['month'], answer_data['year']]):
        return 0
    else:
        return 10

def is_spans_non_empty(answer):
    if len(answer) > 0:
        return 100
    else:
        return 0

with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 解析每一行为一个JSON对象，并添加到列表中
        datasets.append(json.loads(line))

with open(result_path, "w", encoding='utf-8') as result_file, open(trajectory_path, 'w', encoding='utf-8') as trajectory_file:
    iters = 0
    goal = 0
    for dataset in datasets:
        iters += 1
        if iters > 1000:
            break

        question = dataset["question_text"]
        context = dataset["contexts"]

        # 现在 data 包含了文件中所有的 JSON 对象
        answer_data = dataset["answers_objects"][0]
        answer_type = is_number_empty(answer_data["number"]) + is_date_empty(answer_data["date"]) + is_spans_non_empty(
            answer_data["spans"])
        if answer_type == 1:
            Right_answer = answer_data['number']
        elif answer_type == 10:
            Right_answer = answer_data['date']
        elif answer_type == 100:
            Right_answer = answer_data['spans'][0]

        epoch = 0

        Context_prompt = '''Context:''' + str(context)
        Evidence_prompt = '''Context:'''
        Question_prompt = '''Question:''' + str(question)

        while epoch < MAX_EPOCH:
            print(f"ID:{iters}" + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer)
            result_file.write("#" * 10 + "\n")
            trajectory_file.write("#" * 10 + "\n")
            result_file.write(
                "ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")
            trajectory_file.write(
                "ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")

            if epoch == 0:
                set_prompt = E2G_Base_prompt + Question_prompt + Context_prompt
            elif epoch > 0:
                set_prompt = E2G_Gen_prompt + Question_prompt + Evidence_prompt

            epoch += 1
            completion = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=set_prompt,
                max_tokens=200,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                temperature=0.5
            )
            response = completion.choices[0].text.strip()
            print(f"RESPONSE:\n" + response)
            # 手动解析回复并提取信息
            dict_response = {
                "answer": response.split("\n")[0].replace("Answer: ", ""),
                "E2": response.split("\n")[1].replace("Evidence and explanation:", ""),
                "Step-by-step E2": response.split("\n")[2].replace(
                    "Step-by-step reasoning with evidence and explanation: ", "")
            }

            E2 = dict_response["E2"]
            Evidence_prompt = '''Context:''' + str(E2)
            trajectory_file.write(response + "\n")


        result_file.write(dict_response["answer"] + "\n")
        result_file.write("#" * 10 + "\n")
        trajectory_file.write("#" * 10 + "\n")

        if str(dict_response["answer"]).lower() in str(Right_answer).lower() or str(Right_answer).lower() in str(dict_response["answer"]).lower():
            goal += 1
        print(goal)
        #  messages=[ {"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "Hello!"}]

final_goal = goal / iters * 100
print(f"准确率：: {final_goal}%")
