import json
import os

def get_question_item(question_id:str, question_text:str, contexts:list,answer:str):
    question_item = {
        "question_id": question_id,
        "question_text":question_text,
        "contexts": contexts,
        "answer": answer
    }
    return question_item

def get_context_item(idx:int, paragraph_text:str, title:str, is_supporting:bool):
    context_item = {
        "idx": idx,
        "title": title,
        "paragraph_text": paragraph_text,
        "is_supporting": is_supporting
    }
    return context_item

data_path = "./data/StrategyQA/strategyqa_dataset/strategyqa_train.json"
with open(data_path, "r", encoding="utf-8") as file:
    datasets = json.load(file)

data_list = list()
for data in datasets:
    question_id = data["qid"]
    question_text = data["question"]
    facts = data["facts"]
    answer_bool = data["answer"]
    if answer_bool:
        answer = "yes"
    else:
        answer = "no"
    ctx_idx = 0
    contexts = list()
    for fact in facts:
        context_item = get_context_item(idx=ctx_idx, title=str(ctx_idx), paragraph_text=fact, is_supporting=True)
        ctx_idx += 1
        contexts.append(context_item)

    question_item = get_question_item(question_id, question_text, contexts, answer)
    data_list.append(question_item)

print(len(data_list))

data_list_json = json.dumps(data_list, indent=4, ensure_ascii=False)
save_path = "./data/strategyqa.json"
with open(save_path, "w", encoding="utf-8") as save_file:
    save_file.write(data_list_json)
