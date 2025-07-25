from openai import OpenAI
import httpx
from prompt import Evidence_prompt_v2, Evidence_output_prompt_v2
import json
import time
from time import sleep
from painting import painting_from_list

def locate_context(idx: int, context: list):
    for location in range(len(context)):
        if context[location]["idx"] == idx:
            return location

def get_Context_List(List_path:str):
    context_list = []
    # List_path = "./result/SupIdx/V5/8-4-3_05-11_02-31_result_total_test.txt"
    with open(List_path, "r", encoding="utf-8") as file:
        for line in file:
            text = (line.strip())
            if "ID:" in text:
                Item = dict(ID=-1, LIST=[])
                ID_data = int(text.split(":")[1])
                Item["ID"] = ID_data
            if "[" in text and text[0] == "[":
                data = json.loads(text)
                if len(data) == 3:
                    Item["LIST"] = data
                    context_list.append(Item)
    return context_list

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

def Evidengce_QA(client: OpenAI, LEVEL: str, TYPE: str, MAX_ITERATION: int, base_path: str, CurrentTime: time.strftime, Input_prompt: str, Output_prompt: str):
    file_path = base_path + str(LEVEL) + "_" + str(TYPE) + ".json"
    datasets = []
    acc_list = []
    result_path = "result/Q&A V3/distractor/" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    trajectory_path = "result/Q&A V3/distractor/" + str(CurrentTime) + "_" + "trajectory_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    result_json_path = "result/Q&A V3/distractor/JSON/" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".json"
    trajectory_json_path = "result/Q&A V3/distractor/JSON/" + str(CurrentTime) + "_" + "trajectory_" + str(LEVEL) + "_" + str(TYPE) + ".json"

    List_path = "./result/SupIdx/distractor/V2/8-4-3_05-20_18-36_result_distractor_test.txt"
    context_dict_list = get_Context_List(List_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    with open(result_path, "w", encoding='utf-8') as result_file, open(trajectory_path, 'w', encoding='utf-8') as trajectory_file, open(result_json_path, "w", encoding='utf-8') as result_json_file, open(trajectory_json_path, 'w', encoding='utf-8') as trajectory_json_file:
        result_instance = {}
        trajectory_instance = {}
        iters = 0
        goal = 0
        ERROR = 0
        for dataset in datasets:
            iters += 1
            if iters > MAX_ITERATION:
                break

            Support_Context_Idx_List = []
            DictItem = context_dict_list[iters - 1]
            if DictItem['ID'] == iters:
                    Support_Context_Idx_List = DictItem['LIST']


            question = dataset["question_text"]
            context = dataset["contexts"]

            # 现在 data 包含了文件中所有的 JSON 对象
            answer_data = dataset["answers_objects"][0]
            answer_type = is_number_empty(answer_data["number"]) + is_date_empty(answer_data["date"]) + is_spans_non_empty(answer_data["spans"])
            if answer_type == 1:
                Right_answer = answer_data['number']
            elif answer_type == 10:
                Right_answer = answer_data['date']
            elif answer_type == 100:
                Right_answer = answer_data['spans'][0]

            Supprt_Context_List = []
            for Sup_Con_Idx in Support_Context_Idx_List:
                Supprt_Context_List.append(context[locate_context(Sup_Con_Idx, context)])


            Context_prompt = '''Context:''' + str(Supprt_Context_List)
            Question_prompt = '''Question:''' + str(question)

            print(f"ID:{iters}" + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer)
            result_file.write("#" * 10 + "\n")
            trajectory_file.write("#" * 10 + "\n")
            result_file.write("ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")
            trajectory_file.write("ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")

            result_instance["ID"] = str(iters)
            result_instance["Question"] = str(question)
            result_instance["Right Answer"] = str(Right_answer)
            result_instance["context"] = str(Supprt_Context_List)
            trajectory_instance["ID"] = str(iters)
            trajectory_instance["Question"] = str(question)
            trajectory_instance["Right Answer"] = str(Right_answer)
            trajectory_instance["context"] = str(Supprt_Context_List)

            set_prompt = Input_prompt + Question_prompt + Context_prompt + Output_prompt

            is_made_it = False
            error_times = 0
            while not is_made_it:
                try:
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo-16k",
                        messages=[
                            {"role": "system", "content": set_prompt},
                        ],
                        temperature=0.5,
                        max_tokens=500,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )
                    if completion.choices[0].message.content != None:
                        response = completion.choices[0].message.content.strip()
                        print(f"RESPONSE:\n" + response)
                        # 手动解析回复并提取信息
                        dict_response = {
                            "answer": response.split("\n")[0].replace("Answer: ", ""),
                            "idx": response.split("\n")[1].replace("idx: ", ""),
                            "E2": response.split("\n")[2].replace("Evidence and explanation:", ""),
                            "Step-by-step E2": response.split("\n")[3].replace("Step-by-step reasoning with evidence and explanation: ", "")
                        }

                        trajectory_file.write(response + "\n")
                        result_file.write(dict_response["idx"] + "\n" + dict_response["answer"] + "\n")
                        trajectory_instance["response"] = str(response)
                        result_instance["answer"] = str(dict_response["answer"])

                        CORRECT = False
                        if str(dict_response["answer"]).lower() in str(Right_answer).lower() or str(Right_answer).lower() in str(dict_response["answer"]).lower():
                            goal += 1
                            CORRECT = True
                        currend_acc = goal / (iters - ERROR) * 100
                        acc_list.append(round(currend_acc, 2))
                        print(f"答对:{goal}, 总数:{iters}, 网络错误:{ERROR}, 当前准确率:{currend_acc}%")

                        result_file.write("答对：" + str(goal) + " ,总数：" + str(iters) + " ,网络错误：" + str(ERROR) + " ,当前准确率：" + str(currend_acc) + "%\n")
                        trajectory_file.write("答对：" + str(goal) + " ,总数：" + str(iters) + " ,网络错误：" + str(ERROR) + " ,当前准确率：" + str(currend_acc) + "%\n")
                        result_file.write("#" * 10 + "\n")
                        trajectory_file.write("#" * 10 + "\n")

                        result_instance["correct"] = str(CORRECT)
                        trajectory_instance["correct"] = str(CORRECT)
                        result_json_file.write(json.dumps(result_instance) + "\n")
                        trajectory_json_file.write(json.dumps(trajectory_instance) + "\n")

                        is_made_it = True
                    else:
                        print(f"Response is None\n{goal}")
                        is_made_it = True
                        ERROR += 1

                except Exception as e:
                    error_times += 1
                    print("#" * 5 + "ERROR" + str(error_times) + "#" * 5)
                    print(e)
                    sleep(1)

        final_goal = goal / (iters - ERROR) * 100
        print(f"准确率：: {final_goal}%")
        result_file.write("\n准确率：" + str(final_goal) + "%\n网络错误：" + str(ERROR))
        trajectory_file.write("\n准确率：" + str(final_goal) + "%\n网络错误：" + str(ERROR))

    save_path = "result/Q&A V3 PICTURE/distractor/"
    painting_from_list(acc_list, LEVEL, TYPE, CurrentTime, save_path)


CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
LEVEL_list = {"distractor"}  # {"easy", "hard", "medium"} or {"total"} or {"distractor"}
TYPE = "test"  # {"train", "test"}
# MAX_EPOCH = 2
MAX_ITERATION = 236
base_path = "./processed_data/hotpotqa/"
Input_prompt = Evidence_prompt_v2
Output_prompt = Evidence_output_prompt_v2

client = OpenAI(
    base_url="https://api.xiaoai.plus/v1",
    api_key="sk-YMrZo7k1RTpVdNOa7eDb12319dB7471fB841F5Dc2c49Df3e",
    http_client=httpx.Client( base_url="https://api.xiaoai.plus/v1", follow_redirects=True,),
)


for LEVEL in LEVEL_list:
    print(f"正在运行{LEVEL}类型的实验\n")
    Evidengce_QA(client, LEVEL, TYPE, MAX_ITERATION, base_path, CurrentTime, Input_prompt, Output_prompt)
