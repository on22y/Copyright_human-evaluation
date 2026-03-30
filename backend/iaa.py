import numpy as np
from collections import defaultdict, Counter
from sklearn.metrics import cohen_kappa_score
import krippendorff

# Fleiss' Kappa
def compute_fleiss_kappa(data):
    label_map = {"F":0, "C":1, "M":2}
    k = 3

    sample_dict = defaultdict(lambda: [0]*k)

    for d in data:
        s = d["sample_id"]
        l = label_map[d["label"]]
        sample_dict[s][l] += 1

    M = np.array(list(sample_dict.values()))

    n = np.sum(M[0])
    N = len(M)

    P = (np.sum(M*M, axis=1) - n) / (n*(n-1))
    P_bar = np.mean(P)

    p = np.sum(M, axis=0) / (N*n)
    P_e = np.sum(p*p)

    kappa = (P_bar - P_e) / (1 - P_e)
    return float(kappa)


# Exact Agreement
def compute_exact_agreement(sample_dict):
    total = len(sample_dict)
    agree = 0

    for labels in sample_dict.values():
        if len(set(labels)) == 1:
            agree += 1

    return agree / total if total > 0 else 0



# Partial Agreement
def compute_partial_agreement(sample_dict):
    total = len(sample_dict)
    agree = 0

    for labels in sample_dict.values():
        counter = Counter(labels)
        if max(counter.values()) >= 2:
            agree += 1

    return agree / total if total > 0 else 0



# Cohen’s Kappa (pairwise)
def compute_cohen_kappa(sample_dict_with_annotator):
    pairs = [("A","B"), ("A","C"), ("B","C")]
    results = {}

    for a1, a2 in pairs:
        y1, y2 = [], []

        for sample_id, items in sample_dict_with_annotator.items():
            label_map = {a:l for a,l in items}

            if a1 in label_map and a2 in label_map:
                y1.append(label_map[a1])
                y2.append(label_map[a2])

        if len(y1) > 0:
            results[f"{a1}-{a2}"] = float(cohen_kappa_score(y1, y2))

    return results



# Krippendorff’s Alpha
def compute_krippendorff_alpha(sample_dict_with_annotator):
    label_map = {"F":0, "C":1, "M":2}

    matrix = []

    for sample_id, items in sample_dict_with_annotator.items():
        row = []
        annot_map = {a:l for a,l in items}

        for a in ["A","B","C"]:
            if a in annot_map:
                row.append(label_map[annot_map[a]])
            else:
                row.append(np.nan)

        matrix.append(row)

    if len(matrix) == 0:
        return 0

    matrix = np.array(matrix).T

    try:
        alpha = krippendorff.alpha(matrix, level_of_measurement='nominal')
        if np.isnan(alpha) or np.isinf(alpha):
            return 0
        return float(alpha)
    except:
        return 0