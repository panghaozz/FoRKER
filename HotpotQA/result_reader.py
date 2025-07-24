import os
import json
from Function import find_best_match
from evaluate_single_4o import normalize_answer

directory = "result\\Q&A GOLDEN V3\\distractor\\JSON\\"
ITEM_PATH = "KE_new_trajectory.json"
RESULT_PATH = "KE_new_result.json"

TXT_ITEM = "ANALYSE\\KE_new_trajectory_EM_pro.txt"
MAX_ITERATION = 236
full_filepath = os.path.join(directory, ITEM_PATH)
full_result_filepath = os.path.join(directory, RESULT_PATH)
full_txt_filepath = os.path.join(directory, TXT_ITEM)
print(f"Writing in: {full_filepath}")
datasets = []
result_datasets = []
with open(full_filepath, 'r', encoding='utf-8') as file:
    for line in file:
        # 解析每一行为一个JSON对象，并添加到列表中
        datasets.append(json.loads(line))
with open(full_result_filepath, 'r', encoding='utf-8') as result_file:
    for line in result_file:
        result_datasets.append(json.loads(line))

with open(full_txt_filepath, 'w', encoding='utf-8') as txt_file:
    iters = 0
    goal = 0
    while iters < MAX_ITERATION:
        dataset = datasets[iters]
        result_dataset = result_datasets[iters]
        iters += 1
        golden_Answer = normalize_answer(str(dataset["Right Answer"]))
        Answer = normalize_answer(str(result_dataset["answer"]))
        target_phrases = []
        target_phrases.append(golden_Answer)
        getAnswer = find_best_match(Answer, target_phrases)
        # getAnswer = Answer
        if getAnswer != golden_Answer:
        # if dataset["EM correct"] == "False":
            txt_file.write("#" * 10 + "\n")
            txt_file.write(str(dataset["ID"]) + "\n")
            txt_file.write(str(dataset["Question"]) + "\n")
            txt_file.write(str(dataset["Right Answer"]) + "\n")
            txt_file.write(str(dataset["response"]) + "\n\n")
            Context = dataset["context"].replace("[{", "").split("}, {")
            txt_file.write(str(Context[0]) + "\n" + str(Context[1]) + "\n" + str(Context[2]) + "\n")
            txt_file.write("#" * 10 + "\n")
        else:
            goal += 1
    txt_file.write(f"EM:{goal / MAX_ITERATION * 100}%")
print(f"EM:{goal / MAX_ITERATION * 100}%")
