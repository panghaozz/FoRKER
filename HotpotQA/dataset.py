
import os
import json
from tqdm import tqdm
from collections import Counter
from typing import List, Dict

def write_hotpotqa_instances_to_filepath(instances: str, full_filepath: str, type: str):

    max_num_tokens = 1300  # clip later.
    hop_sizes = Counter()
    print(f"Writing in: {full_filepath}")

    hard_filepath = os.path.join(full_filepath, "hard_" + type + ".json")
    medium_filepath = os.path.join(full_filepath, "medium_" + type + ".json")
    easy_filepath = os.path.join(full_filepath, "easy_" + type + ".json")

    with open(hard_filepath, "w") as hard_file, open(medium_filepath, "w") as medium_file, open(easy_filepath, "w") as easy_file:
        for raw_instance in tqdm(instances):
            # Generic RC Format
            processed_instance = {}
            processed_instance["dataset"] = "hotpotqa"
            processed_instance["question_id"] = raw_instance["_id"]
            processed_instance["question_text"] = raw_instance["question"]
            processed_instance["level"] = raw_instance["level"]
            processed_instance["type"] = raw_instance["type"]

            answers_object = {
                "number": "",
                "date": {"day": "", "month": "", "year": ""},
                "spans": [raw_instance["answer"]],
            }
            processed_instance["answers_objects"] = [answers_object]

            raw_context = raw_instance.pop("context")
            # supporting_titles = raw_instance.pop("supporting_facts")["title"]
            supporting_facts = raw_instance.pop("supporting_facts")
            supporting_titles = [fact[0] for fact in supporting_facts]  # 提取每个fact的标题部分

            # title_to_paragraph = { title: "".join(text) for title, text in zip(raw_context["title"], raw_context["sentences"])}

            title_to_paragraph = {}
            for item in raw_context:
                title = item[0]  # 标题
                sentences = item[1]  # 与该标题相关的句子列表
                paragraph_text = "".join(sentences)  # 将句子合并为一个段落
                title_to_paragraph[title] = paragraph_text

            # paragraph_to_title = {"".join(text): title for title, text in zip(raw_context["title"], raw_context["sentences"])}
            paragraph_to_title = {}
            for item in raw_context:
                title = item[0]  # 标题
                sentences = item[1]  # 与该标题相关的句子列表
                paragraph_text = "".join(sentences)  # 将句子合并为一个段落
                paragraph_to_title[paragraph_text] = title

            gold_paragraph_texts = [title_to_paragraph[title] for title in supporting_titles]
            gold_paragraph_texts = set(list(gold_paragraph_texts))

            # paragraph_texts = ["".join(paragraph) for paragraph in raw_context["sentences"]]
            paragraph_texts = []
            for item in raw_context:
                # item[0] 是标题, item[1] 是句子列表
                sentences = item[1]
                paragraph_text = "".join(sentences)
                paragraph_texts.append(paragraph_text)

            paragraph_texts = list(set(paragraph_texts))

            processed_instance["contexts"] = [
                {
                    "idx": index,
                    "title": paragraph_to_title[paragraph_text].strip(),
                    "paragraph_text": paragraph_text.strip(),
                    "is_supporting": paragraph_text in gold_paragraph_texts,
                }
                for index, paragraph_text in enumerate(paragraph_texts)
            ]

            supporting_contexts = [context for context in processed_instance["contexts"] if context["is_supporting"]]
            hop_sizes[len(supporting_contexts)] += 1

            for context in processed_instance["contexts"]:
                context["paragraph_text"] = " ".join(context["paragraph_text"].split(" ")[:max_num_tokens])
            level = processed_instance["level"]
            if level == "hard":
                hard_file.write(json.dumps(processed_instance) + "\n")
            elif level == "medium":
                medium_file.write(json.dumps(processed_instance) + "\n")
            elif level == "easy":
                easy_file.write(json.dumps(processed_instance) + "\n")

    print(f"Hop-sizes: {str(hop_sizes)}")

def write_hotpotqa_test_to_filepath(instances:str, full_filepath:str):
    max_num_tokens = 1300  # clip later.
    print(f"Writing in: {full_filepath}")

    target_filepath = os.path.join(full_filepath, "test_fullwiki.json")

    with open(target_filepath, "w") as target_file:
        for raw_instance in tqdm(instances):
            # Generic RC Format
            processed_instance = {}
            processed_instance["dataset"] = "hotpotqa"
            processed_instance["question_id"] = raw_instance["_id"]
            processed_instance["question_text"] = raw_instance["question"]

            raw_context = raw_instance.pop("context")

            title_to_paragraph = {}
            for item in raw_context:
                title = item[0]  # 标题
                sentences = item[1]  # 与该标题相关的句子列表
                paragraph_text = "".join(sentences)  # 将句子合并为一个段落
                title_to_paragraph[title] = paragraph_text

            # paragraph_to_title = {"".join(text): title for title, text in zip(raw_context["title"], raw_context["sentences"])}
            paragraph_to_title = {}
            for item in raw_context:
                title = item[0]  # 标题
                sentences = item[1]  # 与该标题相关的句子列表
                paragraph_text = "".join(sentences)  # 将句子合并为一个段落
                paragraph_to_title[paragraph_text] = title

            # paragraph_texts = ["".join(paragraph) for paragraph in raw_context["sentences"]]
            paragraph_texts = []
            for item in raw_context:
                # item[0] 是标题, item[1] 是句子列表
                sentences = item[1]
                paragraph_text = "".join(sentences)
                paragraph_texts.append(paragraph_text)

            paragraph_texts = list(set(paragraph_texts))

            processed_instance["contexts"] = [
                {
                    "idx": index,
                    "title": paragraph_to_title[paragraph_text].strip(),
                    "paragraph_text": paragraph_text.strip(),
                }
                for index, paragraph_text in enumerate(paragraph_texts)
            ]

            for context in processed_instance["contexts"]:
                context["paragraph_text"] = " ".join(context["paragraph_text"].split(" ")[:max_num_tokens])
            target_file.write(json.dumps(processed_instance) + "\n")

def write_hotpotqa_instances_to_fullfilepath(instances: str, full_filepath: str, type: str):

    max_num_tokens = 1300  # clip later.
    hop_sizes = Counter()
    print(f"Writing in: {full_filepath}")

    target_filepath = os.path.join(full_filepath, "total_" + type + ".json")

    with open(target_filepath, "w") as target_filepath:
        for raw_instance in tqdm(instances):
            # Generic RC Format
            processed_instance = {}
            processed_instance["dataset"] = "hotpotqa"
            processed_instance["question_id"] = raw_instance["_id"]
            processed_instance["question_text"] = raw_instance["question"]
            processed_instance["level"] = raw_instance["level"]
            processed_instance["type"] = raw_instance["type"]

            answers_object = {
                "number": "",
                "date": {"day": "", "month": "", "year": ""},
                "spans": [raw_instance["answer"]],
            }
            processed_instance["answers_objects"] = [answers_object]

            raw_context = raw_instance.pop("context")
            # supporting_titles = raw_instance.pop("supporting_facts")["title"]
            supporting_facts = raw_instance.pop("supporting_facts")
            supporting_titles = [fact[0] for fact in supporting_facts]  # 提取每个fact的标题部分

            # title_to_paragraph = { title: "".join(text) for title, text in zip(raw_context["title"], raw_context["sentences"])}

            title_to_paragraph = {}
            for item in raw_context:
                title = item[0]  # 标题
                sentences = item[1]  # 与该标题相关的句子列表
                paragraph_text = "".join(sentences)  # 将句子合并为一个段落
                title_to_paragraph[title] = paragraph_text

            # paragraph_to_title = {"".join(text): title for title, text in zip(raw_context["title"], raw_context["sentences"])}
            paragraph_to_title = {}
            for item in raw_context:
                title = item[0]  # 标题
                sentences = item[1]  # 与该标题相关的句子列表
                paragraph_text = "".join(sentences)  # 将句子合并为一个段落
                paragraph_to_title[paragraph_text] = title

            gold_paragraph_texts = [title_to_paragraph[title] for title in supporting_titles]
            gold_paragraph_texts = set(list(gold_paragraph_texts))

            # paragraph_texts = ["".join(paragraph) for paragraph in raw_context["sentences"]]
            paragraph_texts = []
            for item in raw_context:
                # item[0] 是标题, item[1] 是句子列表
                sentences = item[1]
                paragraph_text = "".join(sentences)
                paragraph_texts.append(paragraph_text)

            paragraph_texts = list(set(paragraph_texts))

            processed_instance["contexts"] = [
                {
                    "idx": index,
                    "title": paragraph_to_title[paragraph_text].strip(),
                    "paragraph_text": paragraph_text.strip(),
                    "is_supporting": paragraph_text in gold_paragraph_texts,
                }
                for index, paragraph_text in enumerate(paragraph_texts)
            ]

            supporting_contexts = [context for context in processed_instance["contexts"] if context["is_supporting"]]
            hop_sizes[len(supporting_contexts)] += 1

            for context in processed_instance["contexts"]:
                context["paragraph_text"] = " ".join(context["paragraph_text"].split(" ")[:max_num_tokens])

            target_filepath.write(json.dumps(processed_instance) + "\n")

    print(f"Hop-sizes: {str(hop_sizes)}")


Type = "train"
json_file_path = "P:\\上海大学 code\\HotpotQA\\HotpotQA\\data\\hotpot_train_v1.1.json"
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)
# 加载数据集
directory = "processed_data\\hotpotqa"
os.makedirs(directory, exist_ok=True)
print(type(data), type(data[0]["_id"]), data[0]["question"])


# 写入train_v1.1到hard、medium、easy三个数据
# write_hotpotqa_instances_to_filepath(data, directory, Type)

# 写入test_wiki数据
# write_hotpotqa_test_to_filepath(data, directory)

# 写入写入train_v1.1数据
# write_hotpotqa_instances_to_fullfilepath(data, directory, Type)

