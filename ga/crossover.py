# -----------------------------------------------------------
#  PHASE 5: Crossover Operations
# -----------------------------------------------------------

import random
from ga.schedule import Schedule
from ga.data import ACTIVITIES


ACTIVITY_LIST = list(ACTIVITIES.keys())  # fixed order of activities


def single_point_crossover(parent_a, parent_b):
    """
    Single-point crossover:
      - Choose index k
      - First k activities copied from parent A
      - Remaining copied from parent B
    """
    k = random.randint(0, len(ACTIVITY_LIST) - 1)
    child_assignments = {}

    for i, activity in enumerate(ACTIVITY_LIST):
        if i <= k:
            child_assignments[activity] = parent_a.assignments[activity].copy()
        else:
            child_assignments[activity] = parent_b.assignments[activity].copy()

    return Schedule(child_assignments)


def uniform_crossover(parent_a, parent_b, swap_prob=0.5):
    """
    Uniform crossover:
      - For each activity, choose parent A or B with equal probability.
    """
    child_assignments = {}

    for activity in ACTIVITY_LIST:
        if random.random() < swap_prob:
            child_assignments[activity] = parent_a.assignments[activity].copy()
        else:
            child_assignments[activity] = parent_b.assignments[activity].copy()

    return Schedule(child_assignments)
