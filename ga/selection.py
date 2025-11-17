# -----------------------------------------------------------
#  PHASE 5: Selection (Softmax + Parent Pair Selection)
# -----------------------------------------------------------

import math
import random


def softmax(fitness_list):
    """
    Convert a list of fitness values to a probability distribution.
    p_i = exp(f_i) / Σ exp(f_j)
    """
    # Stabilize by subtracting max before exponentiation (avoids overflow)
    max_f = max(fitness_list)
    exp_values = [math.exp(f - max_f) for f in fitness_list]
    total = sum(exp_values)
    return [ev / total for ev in exp_values]


def select_parents(population, probabilities, num_pairs):
    """
    Select `num_pairs` pairs of parents according to softmax probabilities.

    Returns a list of tuples: [(parentA, parentB), ...]
    """
    parents = []
    for _ in range(num_pairs):
        # random.choices chooses with replacement using probability weights
        parent_a = random.choices(population, weights=probabilities, k=1)[0]
        parent_b = random.choices(population, weights=probabilities, k=1)[0]
        parents.append((parent_a, parent_b))
    return parents
