import os
import json
from tqdm import tqdm
from collections import Counter
from typing import List, Dict

def write_train2test(instances:list, full_filepath: str, Type:str, level:str): # 把train文件里面的"is_supported"元素删掉
    print(f"Writing in: {full_filepath}")

    Targe_file = os.path.join(full_filepath, Type + ".json")

    with open(Targe_file, "w") as target_file:
        for raw_instance in tqdm(instances):
            for data in raw_instance["contexts"]:
                data.pop("is_supporting")

            target_file.write(json.dumps(raw_instance) + "\n")

LEVEL = "" # {"hard", "medium", "easy"} or {"total"} or {"distractor"}
TYPE = "train"  # {"train"}

base_path = "./data/"
file_path = base_path + str(TYPE) + ".json"
datasets = []
Type = "test"
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 解析每一行为一个JSON对象，并添加到列表中
        datasets.append(json.loads(line))

directory = "data"
os.makedirs(directory, exist_ok=True)

write_train2test(instances=datasets, full_filepath=directory, Type=Type, level=LEVEL)
# datasets[0]["contexts"][0].pop("is_supporting")
# length = len(data)
# print(type(datasets))
# print(datasets)
# print(length)
