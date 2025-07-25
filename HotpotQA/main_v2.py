from openai import OpenAI
import httpx
from prompt import Evidence_prompt_v2, Evidence_output_prompt_v2
import json
import time
from time import sleep
from painting import painting_from_list

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

def Evidengce_QA(client: OpenAI, LEVEL: str, TYPE: str, MAX_ITERATION: int, base_path: str, CurrentTime: time.strftime):
    file_path = base_path + str(LEVEL) + "_" + str(TYPE) + ".json"
    datasets = []
    acc_list = []
    result_path = "result/Q&A V2/" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    trajectory_path = "result/Q&A V2/" + str(CurrentTime) + "_" + "trajectory_" + str(LEVEL) + "_" + str(TYPE) + ".txt"

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    with open(result_path, "w", encoding='utf-8') as result_file, open(trajectory_path, 'w', encoding='utf-8') as trajectory_file:
        iters = 0
        goal = 0
        ERROR = 0
        for dataset in datasets:
            iters += 1
            if iters > MAX_ITERATION:
                break

            question = dataset["question_text"]
            context = dataset["contexts"]

            # 现在 data 包含了文件中所有的 JSON 对象
            answer_data = dataset["answers_objects"][0]
            answer_type = is_number_empty(answer_data["number"]) + is_date_empty(
                answer_data["date"]) + is_spans_non_empty(answer_data["spans"])
            if answer_type == 1:
                Right_answer = answer_data['number']
            elif answer_type == 10:
                Right_answer = answer_data['date']
            elif answer_type == 100:
                Right_answer = answer_data['spans'][0]

            Context_prompt = '''Context:''' + str(context)
            Question_prompt = '''Question:''' + str(question)

            print(f"ID:{iters}" + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer)
            result_file.write("#" * 10 + "\n")
            trajectory_file.write("#" * 10 + "\n")
            result_file.write(
                "ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")
            trajectory_file.write(
                "ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")

            set_prompt = Evidence_prompt_v2 + Question_prompt + Context_prompt + Evidence_output_prompt_v2

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

                        if str(dict_response["answer"]).lower() in str(Right_answer).lower() or str(
                                Right_answer).lower() in str(dict_response["answer"]).lower():
                            goal += 1
                        currend_acc = goal / (iters - ERROR) * 100
                        acc_list.append(round(currend_acc, 2))
                        print(f"答对:{goal}, 总数:{iters}, 网络错误:{ERROR}, 当前准确率:{currend_acc}%")

                        result_file.write("答对：" + str(goal) + " ,总数：" + str(iters) + " ,网络错误：" + str(ERROR) + " ,当前准确率：" + str(currend_acc * 100) + "%\n")
                        trajectory_file.write("答对：" + str(goal) + " ,总数：" + str(iters) + " ,网络错误：" + str(ERROR) + " ,当前准确率：" + str(currend_acc * 100) + "%\n")
                        result_file.write("#" * 10 + "\n")
                        trajectory_file.write("#" * 10 + "\n")

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

    save_path = "result/Q&A V2 PICTURE/"
    painting_from_list(acc_list, LEVEL, TYPE, CurrentTime, save_path)


CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
LEVEL_list = {"total"}  # {"easy", "hard", "medium"} or {"total"}
TYPE = "test"  # {"train", "test", "distractor"}
# MAX_EPOCH = 2
MAX_ITERATION = 200
base_path = "./processed_data/hotpotqa/"

client = OpenAI(
    base_url="https://api.xiaoai.plus/v1",
    api_key="sk-YMrZo7k1RTpVdNOa7eDb12319dB7471fB841F5Dc2c49Df3e",
    http_client=httpx.Client( base_url="https://api.xiaoai.plus/v1", follow_redirects=True,),
)


for LEVEL in LEVEL_list:
    print(f"正在运行{LEVEL}类型的实验\n")
    Evidengce_QA(client, LEVEL, TYPE, MAX_ITERATION, base_path, CurrentTime)
