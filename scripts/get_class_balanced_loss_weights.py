import numpy as np
from pprint import pprint


def get_cb_info(beta, num_samples):
    effective_num = (1.0 - np.power(beta, num_samples)) / (1.0 - beta)
    weights = 1 / effective_num
    num_prototypes = 1 / (1 - beta)
    return {
        "effective_num": effective_num.item(),
        "num_prototypes": num_prototypes,
        "effective_num/num_samples": (effective_num / num_samples).item(),
        "num_samples/effective_num": (num_samples / effective_num).item(),
        "weights": weights.item(),
    }


def get_weights(ls_params):
    # ls_params: List of lists, each containing [beta, num_samples] for each class
    no_of_classes = len(ls_params)
    weights = []
    for id_class in range(no_of_classes):
        cb_info = get_cb_info(ls_params[id_class][0], ls_params[id_class][1])
        print(f"\nClass {id_class} info")
        pprint(cb_info)
        weights.append(cb_info["weights"])
    weights = np.array(weights)
    weights = weights / np.sum(weights) * no_of_classes
    return weights


weights = get_weights(
    [
        [0.9999941, 1174124],  # Class 0
        [0.99882, 5933],  # Class 1
    ]
)
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
