import numpy as np
import json

# 1. 准备数据 (假设你已经从预测文件中加载了每个样本的得分)
# 例如，对于 MuSiQue AN EM
# scores_forker: [1, 0, 1, 1, ..., 1] (N个元素的列表或数组)
# scores_baseline: [0, 0, 1, 0, ..., 1] (N个元素的列表或数组)
# 假设 N = len(scores_forker)


def run_bootstrap_analysis(scores_model_A, scores_model_B, num_samples=1000, alpha=0.05):
    """
    对模型A和模型B的得分进行全面的Bootstrap分析。
    - 模型A是我们的模型，模型B是baseline模型。
    - 计算单边检验的p值 (H1: mean(A) > mean(B))。
    - 计算性能差异的置信区间。
    参数:
    scores_model_A (list or np.array): 模型A在每个样本上的得分。
    scores_model_B (list or np.array): 模型B在每个样本上的得分。
    num_samples (int): Bootstrap重采样的次数，推荐5000或更高以获得稳定结果。
    alpha (float): 显著性水平，用于计算置信区间。alpha=0.05 对应 95% 置信区间。
    返回:
    tuple: (p_value, delta_orig, confidence_interval)
           - p_value: 统计显著性的p值。
           - delta_orig: 原始的性能差异（小数形式）。
           - confidence_interval: 一个包含下界和上界的元组（小数形式）。
    """
    scores_model_A = np.array(scores_model_A)
    scores_model_B = np.array(scores_model_B)
    # 样本数量
    n = len(scores_model_A)
    if n == 0:
        raise ValueError("输入得分列表不能为空。")
    # 计算原始观测到的平均分差异
    delta_orig = np.mean(scores_model_A) - np.mean(scores_model_B)
    # --- 核心的Bootstrap重采样过程 ---
    # 存储每次重采样计算出的性能差异
    bootstrap_deltas = []
    for _ in range(num_samples):
        # a. 有放回地抽取索引
        indices = np.random.choice(n, size=n, replace=True)
        # b. 根据索引创建自助样本集
        scores_A_sample = scores_model_A[indices]
        scores_B_sample = scores_model_B[indices]
        # c. 计算自助样本的差异并存储
        delta_sample = np.mean(scores_A_sample) - np.mean(scores_B_sample)
        bootstrap_deltas.append(delta_sample)
    # --- 1. 计算 p-value ---
    # 零假设 H0: mean(A) <= mean(B)
    # 计算在模拟中，差异小于等于0的次数
    count_le_zero = np.sum(np.array(bootstrap_deltas) <= 0)
    p_value = (count_le_zero + 1) / (num_samples + 1)
    # --- 2. 计算置信区间 (Confidence Interval) ---
    # 首先对所有模拟差异进行排序
    bootstrap_deltas.sort()
    # 计算置信区间的上下界索引
    lower_bound_index = int(num_samples * (alpha / 2))
    upper_bound_index = int(num_samples * (1 - alpha / 2))
    # 获取置信区间的下界和上界
    lower_bound = bootstrap_deltas[lower_bound_index]
    upper_bound = bootstrap_deltas[upper_bound_index]
    confidence_interval = (lower_bound, upper_bound)
    return p_value, delta_orig, confidence_interval

if __name__ == "__main__":
    path_to_forker = "./2wikiMHQA/result/QA/JSON/Joint-2hop_result.json"
    path_to_baseline = "./2wikiMHQA/result/Baselines/CoT/GPT4/JSON/CoT_150_03-04_19-57_result_2hop_test.json"
    np.random.seed(42) # 为了结果可复现
    MAX_ITEMS = 150
    result_data_forker = []
    result_data_baseline = []
    scores_forker = []
    scores_baseline = []

    with open(path_to_forker, "r", encoding="utf-8") as f:
        for line in f:
            result_data_forker.append(json.loads(line))
    with open(path_to_baseline, "r", encoding="utf-8") as f:
        for line in f:
            result_data_baseline.append(json.loads(line))
    iters = 0
    while iters < MAX_ITEMS:
        result_item_forker = result_data_forker[iters]
        result_item_baseline = result_data_baseline[iters]
        if result_item_forker["ID"] == result_item_baseline["ID"]:
            score_forker = 1 if result_item_forker['EM correct'] == 'True' else 0
            score_baseline = 1 if result_item_baseline['EM correct'] == 'True' else 0
            scores_forker.append(score_forker)
            scores_baseline.append(score_baseline)
        else:
            print(f"ID 不一样，算forker对，baseline错")
            scores_forker.append(1)
            scores_baseline.append(0)
        iters += 1

    p_value, delta_orig, ci = run_bootstrap_analysis(scores_forker, scores_baseline)
    print(f"p-value: {p_value:.7f}, delta_orig: {delta_orig:.4f}")
    print(f"95% 置信区间 (性能差异): [{ci[0] * 100:.2f}%, {ci[1] * 100:.2f}%]")
    write_path = "./2wikiMHQA/result/BootStrap/GPT40_CoT_boot_strap_count.txt"
    with open(write_path, "w", encoding="utf-8") as f:
        f.write(f"p-value: {p_value:.7f}, 原始性能差异: {delta_orig:.4f}, 95% 置信区间 (性能差异): [{ci[0] * 100:.2f}%, {ci[1] * 100:.2f}%]")
# --- 使用示例 ---
# 假设你已经加载了你的模型和基线模型在MuSiQue AN EM上的逐样本得分
# scores_forker_musique_an_em = [...]
# scores_beam_retrieval_musique_an_em = [...]

# p_value, _ = run_bootstrap_test(scores_forker_musique_an_em, scores_beam_retrieval_musique_an_em)

# print(f"计算出的 p-value 为: {p_value:.4f}")

# if p_value < 0.05:
#     print("提升是统计显著的 (在 p < 0.05 水平上)。")
# else:
#     print("提升在统计上不显著。")

