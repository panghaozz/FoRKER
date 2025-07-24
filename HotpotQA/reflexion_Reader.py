import os
import json
import ast
from Function import find_best_match
from evaluate_single_4o import normalize_answer, evaluate_all

def reflexion_reader(ITEM_PATH: str):
    directory = "result\\Q&A GOLDEN V3\\distractor\\"
    full_filepath = os.path.join(directory, ITEM_PATH)
    print(f"Writing in: {full_filepath}")

    answer_list = []
    with open(full_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            if "Right Answer:" in line and line[0] == "R":
                answers = dict(goldenanswer="", answer="")
                golden_answer = line.split(":")[1]
                answers["goldenanswer"] = golden_answer
            if "answer:" in line.lower() and line[0].lower() == "a":
                getAnswer = line.split(":")[1]
                answers["answer"] = getAnswer
                answer_list.append(answers)

    print(len(answer_list))
    predictionsList = []
    predictionsProList = []
    goldenAnswerList = []

    for Item in answer_list:
        if Item["answer"] == "":
            print(Item)
            break
        goldenAnswer = normalize_answer(Item["goldenanswer"])
        preAnswer = normalize_answer(Item["answer"])
        target_phrases = []
        target_phrases.append(goldenAnswer)
        preAnswerPRO = find_best_match(preAnswer, target_phrases)
        predictionsList.append(preAnswer)
        predictionsProList.append(preAnswerPRO)
        goldenAnswerList.append(goldenAnswer)
    return predictionsList, predictionsProList, goldenAnswerList

QA_file_path = "result\\Q&A GOLDEN V3\\distractor\\JSON\\KE_new_result.json"
QA_datasets = []
with open(QA_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        # 解析每一行为一个JSON对象，并添加到列表中
        QA_datasets.append(json.loads(line))

predictions = []
predictions_pro = []
golden_answers = []
pred_contexts = []
gold_contexts = []
base_path = "./processed_data/hotpotqa/"
LEVEL = "distractor"
TYPE_GOLDEN = "train"
file_path_golden = base_path + str(LEVEL) + "_" + str(TYPE_GOLDEN) + ".json"
datasets_golden = []
with open(file_path_golden, 'r', encoding='utf-8') as file:
    for line in file:
        # 解析每一行为一个JSON对象，并添加到列表中
        datasets_golden.append(json.loads(line))

iters = 0
while iters < 236:
    QA_dataset = QA_datasets[iters]
    data_golden = datasets_golden[iters]
    iters += 1

    # 统计Sup数据
    sp_ctx_list = []
    for context in data_golden['contexts']:
        if context["is_supporting"] == True:
            golden_supporting_ctx = [str(context["title"]), int(context["idx"])]
            sp_ctx_list.append(golden_supporting_ctx)
    gold_contexts.append(sp_ctx_list)

    pre_ctx_list = []
    ctxs = ast.literal_eval(QA_dataset["context"])
    for ctx in ctxs:
        pre_cp_ctx = [str(ctx["title"]), int(ctx["idx"])]
        pre_ctx_list.append(pre_cp_ctx)
    pred_contexts.append(pre_ctx_list)

    if QA_dataset["EM correct"] == "True":
        predictions.append(normalize_answer(QA_dataset["Right Answer"]))
        predictions_pro.append(normalize_answer(QA_dataset["Right Answer"]))
        golden_answers.append(normalize_answer(QA_dataset["Right Answer"]))

ITEM_PATH_1 = "Reflexion_06-05_17-02_trajectory_distractor_test.txt"
ITEM_PATH_2 = "Reflexion_06-05_19-39_trajectory_distractor_test.txt"
predictionsList1, predictionsProList1, goldAnswersList1 = reflexion_reader(ITEM_PATH_1)
predictionsList2, predictionsProList2, goldAnswersList2 = reflexion_reader(ITEM_PATH_2)

predictionsList = predictions + predictionsList1 + predictionsList2
predictions_proList = predictions_pro + predictionsProList1 + predictionsProList2
golden_answersList = golden_answers + goldAnswersList1 + goldAnswersList2

ISPRO = False
if ISPRO:
    evaluate_all(predictions_proList, golden_answersList, pred_contexts, gold_contexts, 236)
if not ISPRO:
    evaluate_all(predictionsList, golden_answersList, pred_contexts, gold_contexts, 236)