from openai import OpenAI
import httpx
from prompt import *
import json
import time
from time import sleep
from painting import painting_from_list
from evaluate_single_4o import normalize_answer, f1_score
from knowledgeEditing import knowledge_edit
from Function import find_best_match

def locate_context(idx: int, context: list):
    for location in range(len(context)):
        if context[location]["idx"] == idx:
            return location

def Evidengce_QA(client: OpenAI, LEVEL: str, TYPE: str, MAX_ITERATION: int, base_path: str, CurrentTime: time.strftime, Input_prompt: list, Output_prompt: list, Input_Rprompt: list, Output_Rprompt: list,  start_iter: int, ISKE: bool, ISAP: bool, Version = ""):
    file_path = base_path + "multihopRag_clean.json"
    datasets = []
    acc_list = []
    acc_em_list = []
    acc_em_pro_list = []
    acc_f1_list = []
    result_path = "result/QA_GPT4o/" + str(Version) + "_" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    trajectory_path = "result/QA_GPT4o/" + str(Version) + "_" + str(CurrentTime) + "_" + "trajectory_" + str(LEVEL) + "_" + str(TYPE) + ".txt"
    result_json_path = "result/QA_GPT4o/JSON/" + str(Version) + "_" + str(CurrentTime) + "_" + "result_" + str(LEVEL) + "_" + str(TYPE) + ".json"
    trajectory_json_path = "result/QA_GPT4o/JSON/" + str(Version) + "_" + str(CurrentTime) + "_" + "trajectory_" + str(LEVEL) + "_" + str(TYPE) + ".json"

    with open(file_path, 'r', encoding='utf-8') as file:
        # 解析每一行为一个JSON对象，并添加到列表中
        datasets = json.load(file)

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

            question = dataset["question_text"]
            contexts = dataset["contexts"]
            Right_answer = dataset["answer"]
            question_type = dataset["question_type"]
            IS_YN = 1 if question_type == "judgment_query" else 0

            Support_Context_Idx_List = list()

            for ctx in contexts:
                context_idx = ctx["idx"]
                Support_Context_Idx_List.append(int(context_idx))

            print(Support_Context_Idx_List)

            Support_Context_List = []
            Temp_Context_List = []
            for Sup_Con_Idx in Support_Context_Idx_List:
                located_context = contexts[int(Sup_Con_Idx)]
                SupportContext = {"idx": located_context["idx"], "paragraph_text": located_context["paragraph_text"]}
                Temp_Context_List.append(located_context)
                Support_Context_List.append(SupportContext)
            processed_contexts, processed_contexts_no_title = knowledge_edit(Temp_Context_List, str(Right_answer))

            Context_KE = [Support_Context_List, processed_contexts_no_title]
            # Context_prompt = '''Context:''' + str(processed_contexts_no_title)
            Context_prompt = '''Context:''' + str(Context_KE[int(ISKE)]) + '''\n'''
            Question_prompt = '''Question:''' + str(question) + '''\n'''

            # print(Context_prompt)

            print(f"ID:{iters}" + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer)
            result_file.write("#" * 10 + "\n")
            trajectory_file.write("#" * 10 + "\n")
            result_file.write("ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")
            trajectory_file.write("ID:" + str(iters) + "\n" + Question_prompt + "\n" + "Right Answer:" + Right_answer + "\n")

            result_instance["ID"] = str(iters)
            result_instance["Question"] = str(question)
            result_instance["Right Answer"] = str(Right_answer)
            result_instance["Support idx"] = str(Support_Context_Idx_List)
            result_instance["context"] = str(Temp_Context_List)
            result_instance["processed context"] = str(processed_contexts)
            trajectory_instance["ID"] = str(iters)
            trajectory_instance["Question"] = str(question)
            trajectory_instance["Right Answer"] = str(Right_answer)
            trajectory_instance["Support idx"] = str(Support_Context_Idx_List)
            trajectory_instance["context"] = str(Temp_Context_List)
            trajectory_instance["processed context"] = str(processed_contexts)

            set_prompt = Input_prompt[IS_YN] + Question_prompt + Context_prompt + Output_prompt[IS_YN]
            is_made_it = False
            error_times = 0
            while not is_made_it:
                try:
                    completion = client.chat.completions.create(
                        model="gpt-4o-2024-11-20",
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
                        '''
                        dict_response = {
                            "answer": filtered_list[0].split(":")[1],
                            "E2": filtered_list[1].split(":")[1],
                            "Step-by-step E2": filtered_list[2].split(":")[1]
                        }
                        '''
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

                        if response_answer != ground_truth_answer:
                            print(f"回答错误，开始反思\n")
                            Context_ref_prompt = '''Context:''' + str(contexts) + '''\n'''
                            Trajectory = str(response)
                            Trajectory_prompt = '''Previous round's results and trajectory:''' + str(Trajectory) + '''\n'''
                            ref_prompt = Input_Rprompt[IS_YN] + Question_prompt + Context_ref_prompt + Trajectory_prompt + Output_Rprompt[IS_YN]
                            is_made_it_ref = False
                            error_times_ref = 0
                            trial_times_ref = 0
                            while not is_made_it_ref:
                                try:
                                    while trial_times_ref < 3:
                                        completion = client.chat.completions.create(
                                            model="gpt-4o-2024-11-20",
                                            messages=[
                                                {"role": "system", "content": ref_prompt},
                                            ],
                                            temperature=0,
                                            max_tokens=1000,
                                            top_p=1,
                                            frequency_penalty=0,
                                            presence_penalty=0,
                                        )
                                        if completion.choices[0].message.content == None:
                                            print(f"Response is None\n{goal}")
                                            is_made_it_ref = True
                                            trial_times_ref = 1000
                                            ERROR += 1
                                        else:
                                            response = completion.choices[0].message.content.strip()
                                            print(f"RESPONSE:\n" + response)
                                            # 手动解析回复并提取信息
                                            resp_text_list = response.split("\n")
                                            filtered_list = [element for element in resp_text_list if element.strip()]
                                            getAns_ref = False
                                            getRef = False
                                            for line in filtered_list:
                                                if "answer:" in line.lower() and line[0].lower() == "a":
                                                    Re_Answer = line.split(":")[1]
                                                    getAns_ref = True
                                                if "reflexion:" in line.lower() and line[0].lower() == "r":
                                                    Re_Reflexion = line.split(":")[1]
                                                    getRef = True
                                            if not getAns_ref and not getRef:
                                                omo = 1 / 0
                                            dict_response_ref = {
                                                "answer": Re_Answer,
                                                "reflexion": Re_Reflexion
                                            }
                                            answer_ref = normalize_answer(dict_response_ref["answer"])
                                            ground_truth_answer_ref = normalize_answer(Right_answer)
                                            target_phrases_ref = []
                                            target_phrases_ref.append(str(ground_truth_answer_ref))
                                            response_answer_ref = find_best_match(answer_ref, target_phrases_ref)
                                            EM_answer_ref = answer_ref
                                            if response_answer_ref != ground_truth_answer_ref:
                                                trial_times_ref += 1
                                                print(f"第 {trial_times_ref}次反思失败，再来一次\n")
                                                if trial_times_ref == 3:
                                                    print(f"答不对，不再尝试\n")
                                            else:
                                                trial_times_ref = 100

                                            if trial_times_ref >= 3:
                                                trajectory_file.write(f"进行反思\n")
                                                trajectory_file.write(response + "\n")
                                                result_file.write(f"进行反思\n")
                                                result_file.write(dict_response_ref["reflexion"] + "\n")
                                                result_file.write(dict_response_ref["answer"] + "\n")
                                                trajectory_instance["response"] = str(response)
                                                trajectory_instance["isRef"] = True
                                                result_instance["answer"] = str(dict_response_ref["answer"])
                                                result_instance["reflexion"] = str(dict_response_ref["reflexion"])
                                                result_instance["isRef"] = True

                                                CORRECT = False
                                                CORRECT_em = False
                                                CORRECT_em_process = False
                                                if str(response_answer_ref).lower() in str(ground_truth_answer_ref).lower() or str(
                                                        ground_truth_answer_ref).lower() in str(response_answer_ref).lower():
                                                    goal += 1
                                                    CORRECT = True
                                                if EM_answer_ref == ground_truth_answer_ref:
                                                    goal_em += 1
                                                    CORRECT_em = True
                                                if response_answer_ref == ground_truth_answer_ref:
                                                    goal_em_process += 1
                                                    CORRECT_em_process = True
                                                f1 = f1_score(response_answer_ref, ground_truth_answer_ref)[0]
                                                goal_f1 += f1
                                                current_acc = goal / (iters - ERROR - start_iter) * 100
                                                current_em_acc = goal_em / (iters - ERROR - start_iter) * 100
                                                current_em_process_acc = goal_em_process / (iters - ERROR - start_iter) * 100
                                                current_f1_acc = goal_f1 / (iters - ERROR - start_iter) * 100
                                                acc_list.append(round(current_acc, 2))
                                                acc_em_list.append(round(current_em_acc, 2))
                                                acc_em_pro_list.append(round(current_em_process_acc, 2))
                                                acc_f1_list.append(round(current_f1_acc, 2))
                                                print(f"原始EM:{goal_em}, 总数:{iters - start_iter}, 网络错误:{ERROR}, 当前原始EM分数:{current_em_acc}%, 增强EM答对:{goal_em_process}，当前增强EM分数:{current_em_process_acc}%，当前F1分数:{current_f1_acc}%")

                                                result_file.write("原始EM：" + str(goal_em) + ", 总数：" + str(iters - start_iter) + ", 网络错误：" + str(ERROR) + ", 当前原始EM分数：" + str(current_em_acc) + "%, 增强EM答对：" + str(goal_em_process) + ", 当前增强EM分数：" + str(current_em_process_acc) + "%, 当前F1分数：" + str(current_f1_acc) + "%\n")
                                                trajectory_file.write("原始EM：" + str(goal_em) + ", 总数：" + str(iters - start_iter) + ", 网络错误：" + str(ERROR) + ", 当前原始EM分数：" + str(current_em_acc) + "%, 增强EM答对：" + str(goal_em_process) + ", 当前增强EM分数：" + str(current_em_process_acc) + "%, 当前F1分数：" + str(current_f1_acc) + "%\n")
                                                result_file.write("#" * 10 + "\n")
                                                trajectory_file.write("#" * 10 + "\n")

                                                result_instance["EM pro correct"] = str(CORRECT_em_process)
                                                result_instance["EM correct"] = str(CORRECT_em)
                                                trajectory_instance["EM pro correct"] = str(CORRECT_em_process)
                                                trajectory_instance["EM correct"] = str(CORRECT_em)
                                                result_json_file.write(json.dumps(result_instance) + "\n")
                                                trajectory_json_file.write(json.dumps(trajectory_instance) + "\n")

                                                is_made_it_ref = True
                                                is_made_it = True
                                except Exception as e:
                                    error_times_ref += 1
                                    print("#" * 5 + "ERROR" + str(error_times_ref) + "#" * 5)
                                    print(e)
                                    sleep(1)

                        else:
                            trajectory_file.write(f"不进行反思\n")
                            trajectory_file.write(response + "\n")
                            result_file.write(f"不进行反思\n")
                            result_file.write(dict_response["answer"] + "\n")
                            trajectory_instance["response"] = str(response)
                            trajectory_instance["isRef"] = False
                            result_instance["answer"] = str(dict_response["answer"])
                            result_instance["isRef"] = False

                            CORRECT = False
                            CORRECT_em = False
                            CORRECT_em_process = False
                            if str(response_answer).lower() in str(ground_truth_answer).lower() or str(ground_truth_answer).lower() in str(response_answer).lower():
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
                            print(f"原始EM:{goal_em}, 总数:{iters - start_iter}, 网络错误:{ERROR}, 当前原始EM分数:{current_em_acc}%, 增强EM答对:{goal_em_process}，当前增强EM分数:{current_em_process_acc}%，当前F1分数:{current_f1_acc}%")

                            result_file.write("原始EM：" + str(goal_em) + ", 总数：" + str(iters - start_iter) + ", 网络错误：" + str(ERROR) + ", 当前原始EM分数：" + str(current_em_acc) + "%, 增强EM答对：" + str(goal_em_process) + ", 当前增强EM分数：" + str(current_em_process_acc) + "%, 当前F1分数：" + str(current_f1_acc) + "%\n")
                            trajectory_file.write("原始EM：" + str(goal_em) + ", 总数：" + str(iters - start_iter) + ", 网络错误：" + str(ERROR) + ", 当前原始EM分数：" + str(current_em_acc) + "%, 增强EM答对：" + str(goal_em_process) + ", 当前增强EM分数：" + str(current_em_process_acc) + "%, 当前F1分数：" + str(current_f1_acc) + "%\n")
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

    save_path = "result/QA_GPT4o/picture/"
    painting_from_list(list=acc_em_list, save_path=save_path, LEVEL=LEVEL, TYPE=TYPE, TIME=CurrentTime, Epochs="EM")
    painting_from_list(list=acc_em_list, save_path=save_path, LEVEL=LEVEL, TYPE=TYPE, TIME=CurrentTime, Epochs="EM pro")
    painting_from_list(list=acc_em_list, save_path=save_path, LEVEL=LEVEL, TYPE=TYPE, TIME=CurrentTime, Epochs="F1")

if __name__ == "__main__":
    CurrentTime = time.strftime("%m-%d_%H-%M", time.localtime())
    LEVEL_list = {"2hop"}  # {"4hop", "2hop"}
    TYPE = "test"  # {"train", "test"}
    # MAX_EPOCH = 2
    MAX_ITERATION = 100
    base_path = "./data/"
    Input_prompt = [Evidence_prompt_golden, Evidence_prompt_golden_YN]
    Output_prompt = [Evidence_output_prompt_golden, Evidence_output_prompt_golden_YN]
    Input_Ref_prompt = [Reflexion_prompt, Reflexion_prompt_YN]
    Output_Ref_prompt = [Reflexion_output_prompt, Reflexion_output_prompt_YN]
    Version = "GPT4o_100"
    start_iter = 0
    ISKE = True  # 知识编辑
    ISAP = False  # 答案处理

    clientGPT = OpenAI(
        base_url="https://xiaoai.plus/v1",
        api_key="sk-inNndrUrn8S4hfpy328c83E091364cF1B743Ee6d1dA9818f",
        http_client=httpx.Client(base_url="https://xiaoai.plus/v1", follow_redirects=True, ),
    )

    for LEVEL in LEVEL_list:
        print(f"正在运行{LEVEL}类型的实验\n是否使用知识编辑：{ISKE}")
        Evidengce_QA(client=clientGPT, LEVEL=LEVEL, TYPE=TYPE, MAX_ITERATION=MAX_ITERATION, base_path=base_path, CurrentTime=CurrentTime, Input_prompt=Input_prompt, Output_prompt=Output_prompt, Input_Rprompt=Input_Ref_prompt, Output_Rprompt=Output_Ref_prompt, start_iter=start_iter, ISKE=ISKE, ISAP=ISAP, Version=Version)
