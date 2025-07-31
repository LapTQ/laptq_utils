import numpy as np
from pprint import pprint


ls_params = [
    {
        "num_samples": 1174124,
        "expected_ratio_of_num_effective": 1 / 7,
    },
    {
        "num_samples": 391578,
        "expected_ratio_of_num_effective": 1 / 7 / 66,
    },
]


def solve_beta(num_samples, num_effective, tolerance=1e-15, beta0=0):

    def f(beta, num_samples, num_effective):
        return np.power(beta, num_samples) - num_effective * beta + num_effective - 1

    def df(x, num_samples, num_effective):
        return num_samples * np.power(x, num_samples - 1) - num_effective

    while True:
        beta1 = beta0 - f(beta0, num_samples, num_effective) / df(
            beta0, num_samples, num_effective
        )
        if abs(beta1 - beta0) < tolerance:
            break
        beta0 = beta1

    return beta1


def get_weight_based_on_expected_ratio_of_num_effective(ls_params):
    no_of_classes = len(ls_params)
    weights = []
    for id_class in range(no_of_classes):
        print(f"\nClass {id_class} params")

        num_samples = ls_params[id_class]["num_samples"]
        expected_ratio_of_num_effective = ls_params[id_class][
            "expected_ratio_of_num_effective"
        ]
        num_effective = num_samples * expected_ratio_of_num_effective
        beta = solve_beta(
            num_samples=num_samples,
            num_effective=num_effective,
        )
        num_prototypes = 1 / (1 - beta)

        print(f" + num_samples:    {num_samples}")
        print(f" + %effective:     {expected_ratio_of_num_effective}")
        print(f" + num_effective:  {num_effective}")
        print(f" + num_prototypes: {num_prototypes}")
        print(f" + beta:           {beta}")

        weights.append(1 / num_effective)

    weights = np.array(weights)
    weights = weights / np.sum(weights) * no_of_classes
    return weights


weights = get_weight_based_on_expected_ratio_of_num_effective(ls_params=ls_params)

print("\nFinal weights for class balanced loss:")
print(weights)


# import torch
# labels = torch.tensor([0, 1, 0, 1, 0])  # Example labels
# torch.manual_seed(0)  # For reproducibility
# inputs = torch.randn(5, 2)  # Example inputs


# from torch.nn import CrossEntropyLoss
# weights = torch.tensor(weights).float()
# celoss = CrossEntropyLoss(weight=weights, reduction='none')
# loss = celoss(inputs, labels)
# print("Loss:", loss)


# import torch
# from torch.nn import functional as F
# labels_one_hot = torch.tensor(
#     [
#         [1, 0],
#         [0, 1],
#         [1, 0],
#         [0, 1],
#         [1, 0],
#     ], dtype=torch.float32
# )
# weights = torch.tensor(weights).float()
# weights = weights.unsqueeze(0)
# weights = weights.repeat(labels_one_hot.shape[0],1) * labels_one_hot
# weights = weights.sum(1)
# weights = weights.unsqueeze(1)
# weights = weights.repeat(1,no_of_classes)

# celoss = F.binary_cross_entropy(input = F.softmax(inputs, dim=1), target = labels_one_hot, weight = weights, reduction='none')
# print("Binary Cross Entropy Loss:", celoss)
