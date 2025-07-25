from openai import OpenAI
import httpx
import json
from prompt import Supporting_prompt_Neg, Supporting_output_prompt_Neg
import time
from time import sleep
from painting import painting_from_list


def Supporting_context(client: OpenAI, LEVEL:str, TYPE_INPUT:str, TYPE_GOLDEN:str, MAX_ITERATION:int, base_path:str, CurrentTime:str, Input_prompt:str, Output_prompt:str, Eps: str):
    file_path = base_path + str(LEVEL) + "_" + str(TYPE_INPUT) + ".json"
    file_path_golden = base_path + str(LEVEL) + "_" + str(TYPE_GOLDEN) + ".json"
    datasets = []
    datasets_golden = []
    recall_list = []
    reslut_path = "result/SupIdx/V_Neg/" + str(Eps) + "_"  + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE_INPUT) + ".txt"
    trajectory_path = "result/SupIdx/V_Neg/" + str(Eps) + "_"  + str(CurrentTime) + "_trajectory_" + str(LEVEL) + "_" + str(TYPE_INPUT) + ".txt"

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    with open(file_path_golden, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets_golden.append(json.loads(line))

    with open(reslut_path, 'w', encoding='utf-8') as result_file, open(trajectory_path, "w", encoding='utf-8') as trajectory_file:
        iters = 0
        goal = 0
        Total = 0
        ERROR = 0
        for dataset in datasets:
            dataset_golden = datasets_golden[iters]
            iters += 1
            if iters > MAX_ITERATION:
                break

            supporting_idx = []
            for context in dataset_golden['contexts']:
                if context["is_supporting"] == True:
                    supporting_idx.append(context["idx"])
            Total += len(supporting_idx)

            question = dataset["question_text"]
            context = dataset["contexts"]

            Context_prompt = '''Context:''' + str(context) + '''\n'''
            Question_prompt = '''Question:''' + str(question) + '''\n'''

            print(f"ID:{iters}" + "\n" + Question_prompt + "golden idx: " + str(supporting_idx) + "\n")
            result_file.write("#" * 10 + "\n")
            trajectory_file.write("#" * 10 + "\n")
            result_file.write("ID:" + str(iters) + "\n" + Question_prompt + "golden idx: " + str(supporting_idx) + "\n")
            trajectory_file.write("ID:" + str(iters) + "\n" + Question_prompt + "golden idx: " + str(supporting_idx) + "\n")

            set_prompt = Input_prompt + Question_prompt + Context_prompt + Output_prompt

            IS_MADE_IT = False
            error_times = 0
            while not IS_MADE_IT:
                try:
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo-16k",
                        messages=[
                            {"role": "system", "content": set_prompt},
                        ],
                        temperature=0,
                        max_tokens=500,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )
                    if completion.choices[0].message.content != None:
                        response = completion.choices[0].message.content.strip()
                        print(f"RESPONSE:\n" + response + "\n")
                        # 手动解析回复并提取信息
                        dict_response = {
                            "idx": response.split("\n")[-1].replace("idx: ", ""),
                            # "Step-by-step E2": response.split("\n")[1].replace("Step by step with evidence and explanation:", "")
                        }
                        response_supporting_fact = json.loads(dict_response["idx"])

                        result_file.write(str(dict_response["idx"]) + "\n")
                        trajectory_file.write(str(response) + "\n")

                        Get_Idx_List = []

                        for i in range(10):
                            if i not in response_supporting_fact:
                                Get_Idx_List.append(int(i))
                        print(f"得到的序列是：{Get_Idx_List}")

                        for idx in Get_Idx_List:
                            if idx in supporting_idx:
                                goal += 1

                        current_goal = goal / (Total - ERROR * len(supporting_idx)) * 100
                        recall_list.append(round(current_goal, 2))
                        print(f"成功的数量为：{goal}, 总数：{Total}, 当前回溯率：{current_goal}%")
                        result_file.write("成功的数量为：" + str(goal) + "总数：" + str(Total) + "当前回溯率：" + str(current_goal) + "%\n" + "#" * 10 + "\n")
                        trajectory_file.write("成功的数量为：" + str(goal) + "总数：" + str(Total) + "当前回溯率：" + str(current_goal) + "%\n" + "#" * 10 + "\n")
                        IS_MADE_IT = True

                    else:
                        print(f"Response is None\n{goal}")
                        result_file.write("Response is None" + str(goal) + "\n" + "#" * 10 + "\n")
                        trajectory_file.write("Response is None" + str(goal) + "\n" + "#" * 10 + "\n")
                        IS_MADE_IT = True
                        ERROR += 1

                except Exception as e:
                    error_times += 1
                    print("#"*5 + "ERROR" + str(error_times) + "#"*5)
                    print(e)
                    sleep(1)


        final_goal = goal / Total * 100
        print(f"回溯率：: {final_goal}%")
        result_file.write("\n回溯率：" + str(final_goal) + "%")

    save_path = "result/SupIdx PICTURE/V_Neg/"
    painting_from_list(recall_list, LEVEL, TYPE_INPUT, CurrentTime, save_path, Epochs=Eps)

client = OpenAI(
    base_url="https://api.xiaoai.plus/v1",
    api_key="sk-YMrZo7k1RTpVdNOa7eDb12319dB7471fB841F5Dc2c49Df3e",
    http_client=httpx.Client( base_url="https://api.xiaoai.plus/v1", follow_redirects=True,),
)

CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
# MAX_EPOCH = 2
# LEVEL = "easy" # {"hard", "medium", "easy"}
LEVEL_LIST = {"total"}  # {"easy", "hard", "medium"} or {"total"}
TYPE_INPUT = "test"  # {"train", "distractor", "test"}
TYPE_GOLDEN = "train"  # {"train", "distractor", "test"}
MAX_ITERATION = 200
base_path = "./processed_data/hotpotqa/"
Input_prompt = Supporting_prompt_Neg
Output_prompt = Supporting_output_prompt_Neg
Epochs = "8-Neg"

for LEVEL in LEVEL_LIST:
    print(f"正在运行{LEVEL}的实验\n")
    Supporting_context(client, LEVEL, TYPE_INPUT, TYPE_GOLDEN, MAX_ITERATION, base_path, CurrentTime, Input_prompt, Output_prompt, Epochs)

