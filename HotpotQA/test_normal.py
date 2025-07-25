import os
import json
from Function import find_best_match
from evaluate_single_4o import normalize_answer

directory = "result/Q&A GOLDEN V3/distractor/JSON/"
ITEM_PATH1 = "KE_new_trajectory.json"
ITEM_PATH2 = "Reflexion_06-05_17-02_trajectory_distractor_test.json"
ITEM_PATH3 = "Reflexion_06-05_19-39_trajectory_distractor_test.json"

MAX_ITERATION = 236
full_filepath = os.path.join(directory, ITEM_PATH1)
ref1_filepath = os.path.join(directory, ITEM_PATH2)
ref2_filepath = os.path.join(directory, ITEM_PATH3)
print(f"Writing in: {full_filepath}")

QA_datasets = []
with open(full_filepath, 'r', encoding='utf-8') as fullfile:
    for line in fullfile:
        # 解析每一行为一个JSON对象，并添加到列表中
        QA_datasets.append(json.loads(line))

Ref1_datasets = []
with open(ref1_filepath, 'r', encoding='utf-8') as ref1file:
    for line1 in ref1file:
        # 解析每一行为一个JSON对象，并添加到列表中
        Ref1_datasets.append(json.loads(line1))

Ref2_datasets = []
with open(ref2_filepath, 'r', encoding='utf-8') as ref2file:
    for line2 in ref2file:
        # 解析每一行为一个JSON对象，并添加到列表中
        Ref2_datasets.append(json.loads(line2))

write_ITEM = "Joint_trajectory.txt.json"
write_path = os.path.join(directory, write_ITEM)
with open(write_path, 'w', encoding='utf-8') as writefile:
    iters = 0
    qaIter = 0
    ref1Iter = 0
    ref2Iter = 0
    while iters < MAX_ITERATION:
        instance = {}
        if qaIter < len(QA_datasets):
            QA_data = QA_datasets[qaIter]
        if ref1Iter < len(Ref1_datasets):
            ref1_data = Ref1_datasets[ref1Iter]
        if ref2Iter < len(Ref2_datasets):
            ref2_data = Ref2_datasets[ref2Iter]

        if ref1Iter < len(Ref1_datasets) and (iters + 1) == int(ref1_data["ID"]):
            instance = ref1_data
            instance["context"] = QA_data["context"]
            instance["isRef"] = True
            ref1Iter += 1
        elif ref2Iter < len(Ref2_datasets) and (iters + 1) == int(ref2_data["ID"]):
            instance = ref2_data
            instance["context"] = QA_data["context"]
            instance["isRef"] = True
            ref2Iter += 1
        else:
            instance = QA_data
            instance["isRef"] = False
        qaIter += 1  #不管什么时候这个都要加一
        iters += 1
        writefile.write(json.dumps(instance) + "\n")





