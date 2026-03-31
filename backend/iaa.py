import numpy as np
from collections import defaultdict
import krippendorff


# Fleiss' Kappa (label)
def compute_fleiss_kappa(data):
    label_map = {"F":0, "C":1, "M":2}
    k = 3

    sample_dict = defaultdict(lambda: [0]*k)

    for d in data:
        s = d["sample_id"]
        l = label_map[d["label"]]
        sample_dict[s][l] += 1

    M = np.array(list(sample_dict.values()))

    if len(M) == 0:
        return 0

    n = np.max(np.sum(M, axis=1))
    if n < 2:
        return 0

    N = len(M)

    denominator = n * (n - 1)
    if denominator == 0:
        return 0

    P = (np.sum(M*M, axis=1) - n) / denominator
    P_bar = np.mean(P)

    p = np.sum(M, axis=0) / (N*n)
    P_e = np.sum(p*p)

    kappa = (P_bar - P_e) / (1 - P_e)

    if np.isnan(kappa) or np.isinf(kappa):
        return 0

    return float(kappa)


# Krippendorff Alpha (q1, ordinal)
def compute_krippendorff_alpha_q1(sample_dict):
    matrix = []

    for sample_id, items in sample_dict.items():
        row = []

        for annotator, label, q1 in items:
            if q1 is None:
                continue
            row.append(q1)

        if len(row) > 0:
            matrix.append(row)

    if len(matrix) == 0:
        return 0

    matrix = np.array(matrix).T
    
    # 완전 동일 값 처리
    if np.var(matrix) == 0:
        return 1.0

    try:
        alpha = krippendorff.alpha(
            matrix,
            level_of_measurement='ordinal'
        )

        if np.isnan(alpha) or np.isinf(alpha):
            return 1.0

        return float(alpha)

    except:
        return 0