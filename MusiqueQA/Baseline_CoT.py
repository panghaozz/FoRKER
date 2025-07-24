from openai import OpenAI
import httpx
from prompt_Ablation import *
import json
import time
from time import sleep
from painting import painting_from_list
from evaluate_single_4o import normalize_answer, f1_score
from knowledgeEditing import knowledge_edit
from Function import find_best_match


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

def Evidengce_QA(client: OpenAI, LEVEL: str, TYPE: str, MAX_ITERATION: int, base_path: str, CurrentTime: time.strftime, Input_prompt: list, Output_prompt: list, start_iter: int, ISKE: bool, ISAP: bool, Version = ""):
    file_path = base_path + str(LEVEL) + "_" + str(TYPE) + ".json"
    datasets = []
    acc_list = []
    acc_em_list = []
    acc_em_pro_list = []
    acc_f1_list = []
    result_path = "result\\Baselines\\CoT\\DeepSeekV3\\" + str(Version) + "_" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    trajectory_path = "result\\Baselines\\CoT\\DeepSeekV3\\" + str(Version) + "_" + str(CurrentTime) + "_" + "trajectory_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    result_json_path = "result\\Baselines\\CoT\\DeepSeekV3\\JSON\\" + str(Version) + "_" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".json"
    trajectory_json_path = "result\\Baselines\\CoT\\DeepSeekV3\\JSON\\" + str(Version) + "_" + str(CurrentTime) + "_" + "trajectory_" + str(LEVEL) + "_" + str(TYPE) + ".json"

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    with open(result_path, "w", encoding='utf-8') as result_file, open(trajectory_path, 'w', encoding='utf-8') as trajectory_file, open(result_json_path, "w", encoding='utf-8') as result_json_file, open(trajectory_json_path, 'w', encoding='utf-8') as trajectory_json_file:
        result_instance = {}
        trajectory_instance = {}
        iters = start_iter
        goal = 0
        goal_em = 0
        goal_em_process = 0
        goal_f1 = 0
        ERROR = 0
        # for dataset in datasets:
        while iters < MAX_ITERATION:
            dataset = datasets[iters]
            iters += 1
            # if iters > MAX_ITERATION:
            #    break
            Support_Context_Idx_List = []

            question = dataset["question_text"]
            context = dataset["contexts"]

            IS_YN = 0
            if str(question).split(" ")[0].lower() in ["were", "are", "do"]:
                IS_YN = 1

            # 现在 data 包含了文件中所有的 JSON 对象
            answer_data = dataset["answers_objects"][0]
            answer_type = is_number_empty(answer_data["number"]) + is_date_empty(answer_data["date"]) + is_spans_non_empty(answer_data["spans"])
            if answer_type == 1:
                Right_answer = answer_data['number']
            elif answer_type == 10:
                Right_answer = answer_data['date']
            elif answer_type == 100:
                Right_answer = answer_data['spans'][0]

            Support_Context_List = context
            Temp_Context_List = context
            reasoning_step = dataset["reasoning_steps"]


            # Context_prompt = '''Context:''' + str(processed_contexts_no_title)
            Context_prompt = '''Context:''' + str(Support_Context_List) + '''\n'''
            Question_prompt = '''Question:''' + str(question) + '''\n'''
            ReasoningStep_prompt = ''' Reasoning Steps:''' + str(reasoning_step) + '''\n'''

            # print(Context_prompt)

            print(f"ID:{iters}" + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer)
            print(ReasoningStep_prompt)
            result_file.write("#" * 10 + "\n")
            trajectory_file.write("#" * 10 + "\n")
            result_file.write("ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")
            trajectory_file.write("ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")

            result_instance["ID"] = str(iters)
            result_instance["Question"] = str(question)
            result_instance["Right Answer"] = str(Right_answer)
            # result_instance["Support idx"] = str(Support_Context_Idx_List)
            result_instance["context"] = str(Temp_Context_List)
            # result_instance["processed context"] = str(processed_contexts)
            trajectory_instance["ID"] = str(iters)
            trajectory_instance["Question"] = str(question)
            trajectory_instance["Right Answer"] = str(Right_answer)
            # trajectory_instance["Support idx"] = str(Support_Context_Idx_List)
            trajectory_instance["context"] = str(Temp_Context_List)
            # trajectory_instance["processed context"] = str(processed_contexts)

            set_prompt = Input_prompt[IS_YN] + Question_prompt + ReasoningStep_prompt + Context_prompt + Output_prompt[IS_YN]

            is_made_it = False
            error_times = 0
            while not is_made_it:
                try:
                    completion = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": set_prompt},
                        ],
                        temperature=0,
                        max_tokens=1000,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0,
                    )
                    if completion.choices[0].message.content == None:
                        print(f"Response is None\n{goal}")
                        is_made_it = True
                        ERROR += 1
                    else:
                        response = completion.choices[0].message.content.strip()
                        print(f"RESPONSE:\n" + response)
                        # 手动解析回复并提取信息
                        resp_text_list = response.split("\n")
                        filtered_list = [element for element in resp_text_list if element.strip()]

                        getAns = False
                        for line in filtered_list:
                            if "answer:" in line.lower() and line[0].lower() == "a":
                                Re_Answer = line.split(":")[1]
                                getAns = True
                        if not getAns:
                            omo = 1/0

                        dict_response = {
                            "answer": Re_Answer
                        }
                        answer = normalize_answer(dict_response["answer"])
                        ground_truth_answer = normalize_answer(Right_answer)
                        target_phrases = []
                        target_phrases.append(str(ground_truth_answer))
                        found_answer = find_best_match(answer, target_phrases)
                        response_answer = found_answer if ISAP else answer
                        EM_answer = answer

                        trajectory_file.write(response + "\n")
                        result_file.write(dict_response["answer"] + "\n")
                        trajectory_instance["response"] = str(response)
                        result_instance["answer"] = str(dict_response["answer"])

                        CORRECT = False
                        CORRECT_em = False
                        CORRECT_em_process = False
                        if str(response_answer).lower() in str(ground_truth_answer).lower() or str(
                                ground_truth_answer).lower() in str(response_answer).lower():
                            goal += 1
                            CORRECT = True
                        if EM_answer == ground_truth_answer:
                            goal_em += 1
                            CORRECT_em = True
                        if response_answer == ground_truth_answer:
                            goal_em_process += 1
                            CORRECT_em_process = True
                        f1 = f1_score(response_answer, ground_truth_answer)[0]
                        goal_f1 += f1
                        current_acc = goal / (iters - ERROR - start_iter) * 100
                        current_em_acc = goal_em / (iters - ERROR - start_iter) * 100
                        current_em_process_acc = goal_em_process / (iters - ERROR - start_iter) * 100
                        current_f1_acc = goal_f1 / (iters - ERROR - start_iter) * 100
                        acc_list.append(round(current_acc, 2))
                        acc_em_list.append(round(current_em_acc, 2))
                        acc_em_pro_list.append(round(current_em_process_acc, 2))
                        acc_f1_list.append(round(current_f1_acc, 2))
                        print(
                            f"原始EM:{goal_em}, 总数:{iters - start_iter}, 网络错误:{ERROR}, 当前原始EM分数:{current_em_acc}%, 增强EM答对:{goal_em_process}，当前增强EM分数:{current_em_process_acc}%，当前F1分数:{current_f1_acc}%")

                        result_file.write(
                            "原始EM：" + str(goal_em) + ", 总数：" + str(iters - start_iter) + ", 网络错误：" + str(
                                ERROR) + ", 当前原始EM分数：" + str(current_em_acc) + "%, 增强EM答对：" + str(
                                goal_em_process) + ", 当前增强EM分数：" + str(
                                current_em_process_acc) + "%, 当前F1分数：" + str(current_f1_acc) + "%\n")
                        trajectory_file.write(
                            "原始EM：" + str(goal_em) + ", 总数：" + str(iters - start_iter) + ", 网络错误：" + str(
                                ERROR) + ", 当前原始EM分数：" + str(current_em_acc) + "%, 增强EM答对：" + str(
                                goal_em_process) + ", 当前增强EM分数：" + str(
                                current_em_process_acc) + "%, 当前F1分数：" + str(current_f1_acc) + "%\n")
                        result_file.write("#" * 10 + "\n")
                        trajectory_file.write("#" * 10 + "\n")

                        result_instance["EM pro correct"] = str(CORRECT_em_process)
                        result_instance["EM correct"] = str(CORRECT_em)
                        trajectory_instance["EM pro correct"] = str(CORRECT_em_process)
                        trajectory_instance["EM correct"] = str(CORRECT_em)
                        result_json_file.write(json.dumps(result_instance) + "\n")
                        trajectory_json_file.write(json.dumps(trajectory_instance) + "\n")

                        is_made_it = True

                except Exception as e:
                    error_times += 1
                    print("#" * 5 + "ERROR" + str(error_times) + "#" * 5)
                    print(e)
                    sleep(1)

        final_goal = goal_em_process / (iters - ERROR - start_iter) * 100
        print(f"准确率：: {final_goal}%")
        result_file.write("\n准确率：" + str(final_goal) + "%\n网络错误：" + str(ERROR))
        trajectory_file.write("\n准确率：" + str(final_goal) + "%\n网络错误：" + str(ERROR))

    save_path = "result\\baselines\\CoT\\DeepSeekV3\\picture\\"
    painting_from_list(list=acc_em_list, save_path=save_path, LEVEL=LEVEL, TYPE=TYPE, TIME=CurrentTime, Epochs="EM")
    painting_from_list(list=acc_em_list, save_path=save_path, LEVEL=LEVEL, TYPE=TYPE, TIME=CurrentTime, Epochs="EM pro")
    painting_from_list(list=acc_em_list, save_path=save_path, LEVEL=LEVEL, TYPE=TYPE, TIME=CurrentTime, Epochs="F1")


CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
LEVEL_list = {"2hop"}  # {"easy", "hard", "medium"} or {"total"} or {"distractor"}
TYPE = "test"  # {"train", "test"}
# MAX_EPOCH = 2
MAX_ITERATION = 150
base_path = "./data/"
Input_prompt = [CoT_prompt, CoT_prompt_YN]
Output_prompt = [CoT_output_prompt, CoT_output_prompt_YN]
Version = "CoT_150"
start_iter = 0
ISKE = False  # 知识编辑
ISAP = False  # 答案处理

client4 = OpenAI(
    base_url="https://xiaoai.plus/v1",
    api_key="sk-97A50hasR28rziaSC3A5DcE5C1Eb4bD18c896c3824E72cE5",
    http_client=httpx.Client( base_url="https://xiaoai.plus/v1", follow_redirects=True,),
)

client35 = OpenAI(
    base_url="https://api.xiaoai.plus/v1",
    api_key="sk-YMrZo7k1RTpVdNOa7eDb12319dB7471fB841F5Dc2c49Df3e",
    http_client=httpx.Client( base_url="https://api.xiaoai.plus/v1", follow_redirects=True,),
)

clientDS = OpenAI(
    api_key="sk-90d78271083243e18799cee96c412218",
    base_url="https://api.deepseek.com",
    http_client=httpx.Client(base_url="https://api.deepseek.com", follow_redirects=True, ),
)

for LEVEL in LEVEL_list:
    print(f"正在运行{LEVEL}类型的实验\n是否使用知识编辑：{ISKE}")
    Evidengce_QA(client=clientDS, LEVEL=LEVEL, TYPE=TYPE, MAX_ITERATION=MAX_ITERATION, base_path=base_path, CurrentTime=CurrentTime, Input_prompt=Input_prompt, Output_prompt=Output_prompt, start_iter=start_iter, ISKE=ISKE, ISAP=ISAP, Version=Version)
