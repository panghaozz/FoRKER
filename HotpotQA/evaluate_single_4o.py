import re
import string
from collections import Counter
from painting import painting_from_list


def normalize_answer(s):
    def remove_and(text):
        # return text.replace(' and ', ' ')
        return text

    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_and(remove_articles(remove_punc(lower(s)))))


def f1_score(prediction, ground_truth):
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)
    ZERO_METRIC = (0, 0, 0)
    if normalized_prediction in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC
    if normalized_ground_truth in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC
    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return ZERO_METRIC
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, precision, recall


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def sp_score(prediction, gold):
    # 将支持事实转换为集合
    cur_sp_pred = set(map(tuple, prediction))
    gold_sp_pred = set(map(tuple, gold))

    # 初始化计数器
    tp, fp, fn = 0, 0, 0

    # 计算真阳性和假阳性
    for e in cur_sp_pred:
        if e in gold_sp_pred:
            tp += 1
        else:
            fp += 1
    # 调整假阳性逻辑
    if tp >= len(gold_sp_pred):
        fp = 0
    else:
        fp = len(gold_sp_pred) - tp
    # 计算假阴性
    for e in gold_sp_pred:
        if e not in cur_sp_pred:
            fn += 1

    # 计算精确度和召回率
    prec = 1.0 * tp / (tp + fp) if tp + fp > 0 else 0.0
    recall = 1.0 * tp / (tp + fn) if tp + fn > 0 else 0.0
    # 计算F1分数
    f1 = 2 * prec * recall / (prec + recall) if prec + recall > 0 else 0.0
    # 计算精确匹配
    em = 1.0 if fp + fn == 0 else 0.0
    return em, prec, recall, f1


def evaluate_all(predictions, gold_answers, pred_contexts, gold_contexts, MAX_ITERATION, Version: str):
    total_em = 0
    total_f1 = 0
    total_prec = 0
    total_recall = 0
    total_sp_em = 0
    total_sp_f1 = 0
    total_sp_prec = 0
    total_sp_recall = 0
    total_joint_em = 0
    total_joint_f1 = 0
    total_joint_prec = 0
    total_joint_recall = 0

    N = MAX_ITERATION
    print(N)
    em_list = []
    for i in range(N):
        pred_ans = predictions[i]
        gold_ans = gold_answers[i]
        pred_ctx = pred_contexts[i]
        gold_ctx = gold_contexts[i]

        # 计算答案的精确匹配
        em = exact_match_score(pred_ans, gold_ans)
        # 计算答案的F1分数
        f1, prec, recall = f1_score(pred_ans, gold_ans)
        # 计算支持事实的精确匹配和F1分数
        sp_em, sp_prec, sp_recall, sp_f1 = sp_score(pred_ctx, gold_ctx)

        # 计算联合指标
        joint_prec = prec * sp_prec
        joint_recall = recall * sp_recall
        if joint_prec + joint_recall > 0:
            joint_f1 = 2 * joint_prec * joint_recall / (joint_prec + joint_recall)
        else:
            joint_f1 = 0.0
        joint_em = em * sp_em

        # 累加各项指标
        total_em += em
        total_f1 += f1
        total_prec += prec
        total_recall += recall
        total_sp_em += sp_em
        total_sp_f1 += sp_f1
        total_sp_prec += sp_prec
        total_sp_recall += sp_recall
        total_joint_em += joint_em
        total_joint_f1 += joint_f1
        total_joint_prec += joint_prec
        total_joint_recall += joint_recall

        em_list.append(float(round(total_em / (i + 1) * 100, 2)))

    # 计算平均值
    avg_em = total_em / N
    avg_f1 = total_f1 / N
    avg_prec = total_prec / N
    avg_recall = total_recall / N
    avg_sp_em = total_sp_em / N
    avg_sp_f1 = total_sp_f1 / N
    avg_sp_prec = total_sp_prec / N
    avg_sp_recall = total_sp_recall / N
    avg_joint_em = total_joint_em / N
    avg_joint_f1 = total_joint_f1 / N
    avg_joint_prec = total_joint_prec / N
    avg_joint_recall = total_joint_recall / N

    results = {
        'em': round(avg_em * 100, 2),
        'f1': round(avg_f1 * 100, 2),
        'prec': round(avg_prec * 100, 2),
        'recall': round(avg_recall * 100, 2),
        'sp_em': round(avg_sp_em * 100, 2),
        'sp_f1': round(avg_sp_f1 * 100, 2),
        'sp_prec': round(avg_sp_prec * 100, 2),
        'sp_recall': round(avg_sp_recall * 100, 2),
        'joint_em': round(avg_joint_em * 100, 2),
        'joint_f1': round(avg_joint_f1 * 100, 2),
        'joint_prec': round(avg_joint_prec * 100, 2),
        'joint_recall': round(avg_joint_recall * 100, 2)
    }
    save_path = "result/Ablation/picture/"
    LEVEL = Version
    painting_from_list(em_list, save_path, LEVEL)

    print(results)
    return results


# 示例调用
predictions = ["The Eiffel Tower"] * 236  # 示例预测答案
gold_answers = ["Eiffel Tower"] * 236  # 示例金标答案
pred_contexts = [[["Paris", 1], ["France", 3], ["Landmark", 2]]] * 236  # 示例预测支持事实
gold_contexts = [[["Paris", 1], ["France", 3]]] * 236  # 示例金标支持事实

# evaluate_all(predictions, gold_answers, pred_contexts, gold_contexts)
