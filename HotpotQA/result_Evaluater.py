import os
import json
import ast
from evaluate_single_4o import evaluate_all, normalize_answer
from Function import find_best_match

def Sumarize_result(full_filepath: str, MAX_ITERATION: int, ISPRO: bool):
    datasets = []
    with open(full_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    # pred_contexts_236 = [[["Paris", 1], ["France", 3], ["Landmark", 2]]] * 236  # 示例预测支持事实
    # gold_contexts_236 = [[["Paris", 1], ["France", 3]]] * 236  # 示例金标支持事实
    base_path = "./processed_data/hotpotqa/"
    LEVEL = "distractor"
    TYPE_GOLDEN = "train"
    file_path_golden = base_path + str(LEVEL) + "_" + str(TYPE_GOLDEN) + ".json"
    datasets_golden = []

    predictions = []
    predictions_pro = []
    gold_answers = []
    pred_contexts = []
    gold_contexts = []

    with open(file_path_golden, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets_golden.append(json.loads(line))
    iters = 0
    while iters < MAX_ITERATION:
        data_golden = datasets_golden[iters]
        dataset = datasets[iters]
        iters += 1
        # 统计Sup数据
        sp_ctx_list = []
        for context in data_golden['contexts']:
            if context["is_supporting"] == True:
                golden_supporting_ctx = [str(context["title"]), int(context["idx"])]
                sp_ctx_list.append(golden_supporting_ctx)
        gold_contexts.append(sp_ctx_list)

        pre_ctx_list = []
        ctxs = ast.literal_eval(dataset["context"])
        for ctx in ctxs:
            pre_cp_ctx = [str(ctx["title"]), int(ctx["idx"])]
            pre_ctx_list.append(pre_cp_ctx)
        pred_contexts.append(pre_ctx_list)

        # 统计Ans数据
        input_text = normalize_answer(str(dataset["answer"]))
        right_answer = normalize_answer(str(dataset["Right Answer"]))
        target_phrases = []
        target_phrases.append(right_answer)
        best_answer = find_best_match(input_text, target_phrases)
        get_Answer = input_text
        predictions_pro.append(str(best_answer))
        predictions.append(str(get_Answer))
        gold_answers.append(right_answer)

    if ISPRO:
        return predictions_pro, gold_answers, pred_contexts, gold_contexts
    else:
        return predictions, gold_answers, pred_contexts, gold_contexts

if __name__ == '__main__':
    # print(f"{predictions[1]}\n{gold_answers[1]}\n{pred_contexts[235]}\n{gold_contexts[235]}")
    # directory = "result/Q&A GOLDEN V3/distractor/JSON/"
    directory = "result/Q&A GOLDEN V3/GPT4o/JSON/"
    ITEM_PATH = "GPT4o_100_07-23_00-44_result_distractor_test.json"
    MAX_ITERATION = 100
    ISPRO = True
    Version = "GPT4o-100"

    full_filepath = os.path.join(directory, ITEM_PATH)
    print(f"Writing in: {full_filepath}")
    predictions, gold_answers, pred_contexts, gold_contexts = Sumarize_result(full_filepath, MAX_ITERATION, ISPRO)
    evaluate_all(predictions=predictions, gold_answers=gold_answers, pred_contexts=pred_contexts, gold_contexts=gold_contexts, MAX_ITERATION=MAX_ITERATION, Version=Version)