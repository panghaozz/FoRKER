import numpy as np

def estimate_ci_radius(p_A, p_B, n, confidence_level=0.95):
    """
    估算两个独立比例之差的置信区间半径。

    这个函数基于正态分布近似二项分布的原理，用于快速估算
    两个模型性能差异的置信区间宽度的一半（即“半径”）。

    参数:
    p_A (float): 模型A的得分（EM或F1），小数形式，例如 0.85。
    p_B (float): 模型B的得分（EM或F1），小数形式，例如 0.75。
    n (int): 测试集的样本数量。
    confidence_level (float): 置信水平，默认为0.95（对应95%置信区间）。

    返回:
    float: 估算出的置信区间半径（小数形式）。
           最终的置信区间约等于 (p_A - p_B) ± 半径。
    """
    # 1. 输入验证
    if not (0 <= p_A <= 1 and 0 <= p_B <= 1):
        raise ValueError("模型得分 p_A 和 p_B 必须在0和1之间。")
    if n <= 0:
        raise ValueError("样本数量 n 必须是正整数。")
    if not (0 < confidence_level < 1):
        raise ValueError("置信水平 confidence_level 必须在0和1之间。")

    # 2. 计算性能差异的标准误差 (Standard Error of the Difference)
    # SE_d = sqrt( SE_A^2 + SE_B^2 )
    # 其中 SE_A^2 = p_A * (1 - p_A) / n
    #      SE_B^2 = p_B * (1 - p_B) / n
    se_A_squared = p_A * (1 - p_A) / n
    se_B_squared = p_B * (1 - p_B) / n
    
    # 检查方差是否为负（由于浮点数精度问题，在p接近0或1时可能发生）
    if se_A_squared < 0 or se_B_squared < 0:
        se_A_squared = max(0, se_A_squared)
        se_B_squared = max(0, se_B_squared)
        
    se_difference = np.sqrt(se_A_squared + se_B_squared)

    # 3. 查找对应置信水平的临界值 (Z-score)
    # 例如，95% -> alpha=0.05 -> alpha/2=0.025 -> Z_score ≈ 1.96
    # 我们使用 scipy.stats.norm.ppf 来精确计算
    try:
        from scipy.stats import norm
        alpha = 1 - confidence_level
        z_score = norm.ppf(1 - alpha / 2)
    except ImportError:
        # 如果没有安装scipy，使用常见的近似值
        if confidence_level == 0.95:
            z_score = 1.96
        elif confidence_level == 0.99:
            z_score = 2.576
        else:
            # 对于其他不常见的值，给出提示
            print("警告: 未安装scipy库，将使用1.96作为Z-score的近似值（对应95%置信度）。")
            z_score = 1.96

    # 4. 计算置信区间半径 (Margin of Error)
    # 半径 = 临界值 * 标准误差
    radius = z_score * se_difference
    
    return radius

score_forker = 0.929
score_baseline = 0.718
NUM = 500
radius = estimate_ci_radius(score_forker, score_baseline, NUM)
gap = score_forker - score_baseline
print(f"半径为：{radius}\t性能差异为{gap * 100}\t")
print(f"95% 置信区间 (性能差异): [{gap - radius:.3f}%, {gap + radius:.3f}%]")
