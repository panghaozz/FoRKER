import os
import json
import ast
from evaluate_single_4o import evaluate_all, normalize_answer
from Function import find_best_match

def Sumarize_result(full_filepath: str, MAX_ITERATION: int, ISPRO: bool, LEVEL: str):
    datasets = []
    with open(full_filepath, 'r', encoding='utf-8') as file:
        for line in file:
            # 解析每一行为一个JSON对象，并添加到列表中
            datasets.append(json.loads(line))

    # pred_contexts_236 = [[["Paris", 1], ["France", 3], ["Landmark", 2]]] * 236  # 示例预测支持事实
    # gold_contexts_236 = [[["Paris", 1], ["France", 3]]] * 236  # 示例金标支持事实
    base_path = "./data/"
    # LEVEL = "4hop"  # "4hop", "2hop"
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
    directory = "./result/QA/JSON/"
    ITEM_PATH_2hop = "Joint-2hop_result.json"
    ITEM_PATH_4hop = "Joint-4hop_result.json"
    MAX_ITERATION_2hop = 381
    MAX_ITERATION_4hop = 119
    ISPRO = False
    Version_2hop = "2hop_381"
    Version_4hop = "4hop_119"
    LEVEL_2hop = "2hop"  # "4hop", "2hop"
    LEVEL_4hop = "4hop"  # "4hop", "2hop"
    full_filepath_2hop = os.path.join(directory, ITEM_PATH_2hop)
    full_filepath_4hop = os.path.join(directory, ITEM_PATH_4hop)
    print(f"Writing in: {full_filepath_2hop} and {full_filepath_4hop}")
    predictions_2hop, gold_answers_2hop, pred_contexts_2hop, gold_contexts_2hop = Sumarize_result(full_filepath=full_filepath_2hop, MAX_ITERATION=MAX_ITERATION_2hop, ISPRO=ISPRO, LEVEL=LEVEL_2hop)
    predictions_4hop, gold_answers_4hop, pred_contexts_4hop, gold_contexts_4hop = Sumarize_result(full_filepath=full_filepath_4hop, MAX_ITERATION=MAX_ITERATION_4hop, ISPRO=ISPRO, LEVEL=LEVEL_4hop)
    predictions = predictions_2hop + gold_answers_4hop
    gold_answers = gold_answers_2hop + gold_answers_4hop
    pred_contexts = pred_contexts_2hop + pred_contexts_4hop
    gold_contexts = gold_contexts_2hop + gold_contexts_4hop
    MAX_ITERATION = 500
    # evaluate_all(predictions=predictions_2hop, gold_answers=gold_answers_2hop, pred_contexts=pred_contexts_2hop, gold_contexts=gold_contexts_2hop, MAX_ITERATION=MAX_ITERATION_2hop, Version=Version_2hop)
    # evaluate_all(predictions=predictions_4hop, gold_answers=gold_answers_4hop, pred_contexts=pred_contexts_4hop, gold_contexts=gold_contexts_4hop, MAX_ITERATION=MAX_ITERATION_4hop, Version=Version_4hop)
    evaluate_all(predictions=predictions, gold_answers=gold_answers, pred_contexts=pred_contexts, gold_contexts=gold_contexts, MAX_ITERATION=MAX_ITERATION, Version="complete")