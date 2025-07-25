from openai import OpenAI
import httpx
import json
from promptInFocusing import *
import time
from time import sleep
from painting import painting_from_list

def locate_context(idx: int, context: list):
    for location in range(len(context)):
        if context[location]["idx"] == idx:
            return location

def Supporting_context(client: OpenAI, LEVEL:str, TYPE_INPUT:str, TYPE_GOLDEN:str, MAX_ITERATION:int, base_path:str, CurrentTime:str, Input_prompt:list, Output_prompt:list, Eps: str, Epochs_list: list, start_iter: int, Max_Epoch: int):
    file_path = base_path + str(LEVEL) + "_" + str(TYPE_INPUT) + ".json"
    file_path_golden = base_path + str(LEVEL) + "_" + str(TYPE_GOLDEN) + ".json"
    datasets = []
    datasets_golden = []
    recall_list = []
    reslut_path = "result/SupIdx_GPT4o/" + str(Eps) + "_" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE_INPUT) + ".txt"
    trajectory_path = "result/SupIdx_GPT4o/" + str(Eps) + "_" + str(CurrentTime) + "_trajectory_" + str(LEVEL) + "_" + str(TYPE_INPUT) + ".txt"
    reslut_json_path = "result/SupIdx_GPT4o/JSON/" + str(Eps) + "_" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE_INPUT) + ".json"
    trajectory_json_path = "result/SupIdx_GPT4o/JSON/" + str(Eps) + "_" + str(CurrentTime) + "_trajectory_" + str(LEVEL) + "_" + str(TYPE_INPUT) + ".json"

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    with open(file_path_golden, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets_golden.append(json.loads(line))

    with open(reslut_path, 'w', encoding='utf-8') as result_file, open(trajectory_path, "w", encoding='utf-8') as trajectory_file, open(reslut_json_path, 'w', encoding='utf-8') as result_json_file, open(trajectory_json_path, "w", encoding='utf-8') as trajectory_json_file:
        iters = start_iter
        result_instance = {}
        trajectory_instance = {}
        goal = 0
        goal1 = 0
        goal2 = 0
        goal3 = 0
        goal4 = 0
        Sub_Error = [goal1, goal2, goal3, goal4]
        Total = 0
        ERROR = 0
        while iters < MAX_ITERATION:
            dataset = datasets[iters]
            dataset_golden = datasets_golden[iters]
            iters += 1

            Is_Sub_Error = False
            golden_supporting_idx = []
            for context in dataset_golden['contexts']:
                if context["is_supporting"] == True:
                    golden_supporting_idx.append(context["idx"])
            Total += len(golden_supporting_idx)

            question = dataset["question_text"]
            context = dataset["contexts"]
            reasoning_step = dataset["reasoning_steps"]

            Question_prompt = '''Question:''' + str(question) + '''\n'''
            ReasoningStep_prompt = ''' Reasoning Steps:''' + str(reasoning_step) + '''\n'''

            print(f"ID:{iters}" + "\n" + Question_prompt + "golden idx: " + str(golden_supporting_idx) + "\n")
            result_file.write("#" * 10 + "\n")
            result_file.write("ID:" + str(iters) + "\n" + Question_prompt + "golden idx: " + str(golden_supporting_idx) + "\n")
            trajectory_file.write("#" * 10 + "\n")
            trajectory_file.write("ID:" + str(iters) + "\n" + Question_prompt + "golden idx: " + str(golden_supporting_idx) + "\n")

            result_instance["ID"] = str(iters)
            result_instance["Question"] = str(question)
            result_instance["Golden idx"] = str(golden_supporting_idx)
            result_instance["context"] = str(context)
            trajectory_instance["ID"] = str(iters)
            trajectory_instance["Question"] = str(question)
            trajectory_instance["Golden idx"] = str(golden_supporting_idx)
            trajectory_instance["context"] = str(context)

            processed_context = []
            supporting_facts = [[], [], [],[]]
            supporting_facts[0] = context
            result_suopporting_facts = []
            pre_supporting_facts_id = [i for i in range(20)]
            epochs = 0
            while epochs < Max_Epoch:
                print(pre_supporting_facts_id)
                error_times = 0
                print(f"进行第{epochs}轮访问：\n")
                Context_prompt = '''Context:''' + str(supporting_facts[epochs]) + '''\n'''  # 需要选择context，所以放在循环里

                set_prompt = str(Input_prompt[epochs]) + Question_prompt + ReasoningStep_prompt + Context_prompt + str(Output_prompt[epochs])
                IS_MADE_IT = False
                while not IS_MADE_IT:
                    try:
                        completion = client.chat.completions.create(
                            model="gpt-4o-2024-11-20",
                            messages=[
                                {"role": "system", "content": set_prompt},
                            ],
                            temperature=0,
                            max_tokens=1000,
                            frequency_penalty=0,
                            presence_penalty=0,
                        )
                        if completion.choices[0].message.content == None:
                            print(f"Response is None\n{goal}")
                            IS_MADE_IT = True
                            epochs = 10
                            ERROR += 1
                        else:
                            response = completion.choices[0].message.content.strip()
                            print(f"RESPONSE:\n" + response + "\n")
                            resp_text_list = response.split("\n")
                            filtered_list = [element for element in resp_text_list if element.strip()]
                            getIdx = False
                            for line in filtered_list:
                                if "idx:" in line.lower():
                                    Re_Idx = line.split(":")[1]
                                    getIdx = True
                            if not getIdx:
                                print("not getIdx")
                                omo = 1 / 0
                            # 手动解析回复并提取信息
                            dict_response = {
                                "idx": Re_Idx,
                            }
                            response_supporting_fact = json.loads(dict_response["idx"])
                            for get_id in response_supporting_fact:
                                if get_id not in pre_supporting_facts_id:
                                    print("error2")
                                    omo = 1 / 0

                            result_file.write(str(dict_response["idx"]) + "\n" + "\n")
                            trajectory_file.write(str(response) + "\n" + "\n")

                            epochs += 1
                            Exist = True
                            it = 0
                            while Exist and not Is_Sub_Error:
                                if it < 2:
                                    idx = golden_supporting_idx[it]
                                    if idx not in response_supporting_fact:
                                        Sub_Error[epochs - 1] += 1
                                        Exist = False
                                        Is_Sub_Error = True
                                    it += 1
                                else:
                                    Exist = False

                            if Max_Epoch > 1:
                                if epochs < Max_Epoch:
                                    for i in range(int(Epoch_list[epochs - 1])):
                                        supporting_facts[epochs].append(
                                            context[locate_context(response_supporting_fact[i], context)])

                                    IS_MADE_IT = True
                                    pre_supporting_facts_id = response_supporting_fact

                            if epochs == Max_Epoch:
                                for idx in response_supporting_fact:
                                    if idx in golden_supporting_idx:
                                        goal += 1

                                result_instance["idx"] = str(dict_response["idx"])
                                trajectory_instance["response"] = str(response)

                                current_goal = goal / (Total - ERROR * len(golden_supporting_idx)) * 100
                                recall_list.append(round(current_goal, 2))
                                print(
                                    f"成功的数量为：{goal}, 总数：{Total}, 当前回溯率：{current_goal}% \n 第一轮错误：{Sub_Error[0]}，第二轮错误：{Sub_Error[1]}，第三轮错误：{Sub_Error[2]}，第四轮错误：{Sub_Error[3]}")
                                result_file.write(
                                    "成功的数量为：" + str(goal) + "总数：" + str(Total) + "当前回溯率：" + str(
                                        current_goal) + "%\n" + "第1轮错误：" + str(Sub_Error[0]) + "，第2轮错误：" + str(
                                        Sub_Error[1]) + "，第3轮错误：" + str(Sub_Error[2]) + "，第4轮错误：" + str(Sub_Error[3]) + "\n" + "#" * 10 + "\n")
                                trajectory_file.write(
                                    "成功的数量为：" + str(goal) + "总数：" + str(Total) + "当前回溯率：" + str(
                                        current_goal) + "%\n" + "第1轮错误：" + str(Sub_Error[0]) + "，第2轮错误：" + str(
                                        Sub_Error[1]) + "，第3轮错误：" + str(Sub_Error[2]) + "，第4轮错误：" + str(Sub_Error[3]) + "\n" + "#" * 10 + "\n")

                                result_json_file.write(json.dumps(result_instance) + "\n")
                                trajectory_json_file.write(json.dumps(trajectory_instance) + "\n")
                                IS_MADE_IT = True
                                pre_supporting_facts_id = response_supporting_fact

                    except Exception as e:
                        error_times += 1
                        print("#" * 5 + "ERROR" + str(error_times) + "#" * 5)
                        print(e)
                        sleep(1)

        final_goal = goal / (Total - ERROR * len(golden_supporting_idx)) * 100
        print(f"回溯率：: {final_goal}%")
        result_file.write("\n回溯率：" + str(final_goal) + "%")

    save_path = "result/SupIdx_GPT4o/picture/"
    # painting_from_list(recall_list, LEVEL, TYPE_INPUT, CurrentTime, Epochs=Eps)
    painting_from_list(list=recall_list, save_path=save_path, LEVEL=LEVEL, TYPE=TYPE_INPUT, TIME=CurrentTime, Epochs=Eps)

if __name__ == "__main__":
    CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
    # MAX_EPOCH = 2
    # LEVEL = "easy" # {"hard", "medium", "easy"}
    LEVEL_LIST = {"2hop"}  # {"easy", "hard", "medium"} or {"total"} or {"distractor"}
    TYPE_INPUT = "test"  # {"train", "test"}
    TYPE_GOLDEN = "train"  # {"train", "test"}
    Epochs = "GPT4o-16-8-4-3_100"
    # Epoch_list = [8, 4, 3]
    Epoch_list = [16, 8, 4, 3]
    MAX_ITERATION = 100
    base_path = "./data/"
    # Input_prompt = [Supporting_prompt_V2, Supporting_prompt_V2_Thd, Supporting_prompt_V2_4th]
    Input_prompt = [Supporting_prompt_V2, Supporting_prompt_V2_Sec, Supporting_prompt_V2_Thd, Supporting_prompt_V2_4th]
    # Output_prompt = [Supporting_output_prompt_V2, Supporting_output_prompt_V2_Thd, Supporting_output_prompt_V2_4th]
    Output_prompt = [Supporting_output_prompt_V2, Supporting_output_prompt_V2_Sec, Supporting_output_prompt_V2_Thd, Supporting_output_prompt_V2_4th]
    start_iter = 0
    Max_Epoch = 4

    clientGPT = OpenAI(
        base_url="https://xiaoai.plus/v1",
        api_key="sk-inNndrUrn8S4hfpy328c83E091364cF1B743Ee6d1dA9818f",
        http_client=httpx.Client( base_url="https://xiaoai.plus/v1", follow_redirects=True,),
    )

    for LEVEL in LEVEL_LIST:
        print(f"正在运行{LEVEL}的实验\n")
        Supporting_context(clientGPT, LEVEL, TYPE_INPUT, TYPE_GOLDEN, MAX_ITERATION, base_path, CurrentTime, Input_prompt, Output_prompt, Epochs, Epoch_list, start_iter, Max_Epoch)

