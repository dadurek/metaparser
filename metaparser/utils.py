import math


def entropy(string: str) -> float:
    prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob])

    return entropy
