# -----------------------------------------------------------
#  PHASE 5: Mutation
# -----------------------------------------------------------

import random
from ga.data import ROOMS, TIME_SLOTS, FACILITATORS, ACTIVITIES


def mutate(schedule, mutation_rate=0.01):
    """
    Mutates the schedule IN PLACE.

    For each activity:
        For each attribute (room/time/facilitator):
            With probability mutation_rate:
                Replace with a random valid value.
    """
    for activity in ACTIVITIES.keys():
        assignment = schedule.assignments[activity]

        # Mutate room
        if random.random() < mutation_rate:
            assignment["room"] = random.choice(list(ROOMS.keys()))

        # Mutate time
        if random.random() < mutation_rate:
            assignment["time"] = random.choice(TIME_SLOTS)

        # Mutate facilitator
        if random.random() < mutation_rate:
            assignment["facilitator"] = random.choice(FACILITATORS)

    return schedule  # return for convenience
