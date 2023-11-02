from sklearn.metrics import (
    f1_score,
    accuracy_score,
    precision_score,
    recall_score
)

def evaluate_claim_detection(
        target,
        predicted,
):
    acc = accuracy_score(target, predicted)
    f1 = f1_score(target, predicted)
    prec = precision_score(target, predicted)
    rec = recall_score(target, predicted)

    return acc, f1, prec, rec