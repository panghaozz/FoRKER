import json
import os
from evaluate_single_4o import normalize_answer

def get_question_item(question_id:str, question_text:str,  question_type:str, contexts:list,answer:str):
    question_item = {
        "question_id": question_id,
        "question_text": question_text,
        "question_type": question_type,
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

data_path = "./data/MultiHop-RAG/multihopRag_1000.json"
with open(data_path, "r", encoding="utf-8") as file:
    datasets = json.load(file)

question_idx = 0
data_list = list()

for data in datasets:
    question_id = str(question_idx)
    question_text = data["query"]
    evidences = data["evidence_list"]
    question_type = data["question_type"]
    answer = data["answer"]
    question_idx += 1
    if question_type == "inference_query":
        ctx_idx = 0
        contexts = list()
        for evidence in evidences:
            fact = evidence["fact"]
            title = evidence["title"]
            context_item = get_context_item(idx=ctx_idx, title=title, paragraph_text=fact, is_supporting=True)
            ctx_idx += 1
            contexts.append(context_item)
        question_item = get_question_item(question_id, question_text, question_type, contexts, answer)
        data_list.append(question_item)

    elif question_type == "comparison_query" or question_type == "inference_query":
        answer_normal = normalize_answer(answer)
        if answer_normal == "yes" or answer_normal == "no":
            ctx_idx = 0
            contexts = list()
            question_type = "judgment_query"
            for evidence in evidences:
                fact = evidence["fact"]
                title = evidence["title"]
                context_item = get_context_item(idx=ctx_idx, title=title, paragraph_text=fact, is_supporting=True)
                ctx_idx += 1
                contexts.append(context_item)
            question_item = get_question_item(question_id, question_text, question_type, contexts, answer)
            data_list.append(question_item)

print(len(data_list))

data_list_json = json.dumps(data_list, indent=4, ensure_ascii=False)
save_path = "./data/multihopRag_clean.json"
with open(save_path, "w", encoding="utf-8") as save_file:
    save_file.write(data_list_json)
