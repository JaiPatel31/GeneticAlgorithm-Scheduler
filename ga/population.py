# -----------------------------------------------------------
#  PHASE 3: Population Initialization (Random Schedules)
# -----------------------------------------------------------

import random
from ga.data import ACTIVITIES, ROOMS, TIME_SLOTS, FACILITATORS
from ga.schedule import Schedule


# -----------------------------------------------------------
# Random Assignment for a Single Activity
# -----------------------------------------------------------
def random_assignment():
    """
    Returns a dictionary like:
        {"room": <room>, "time": <time>, "facilitator": <facilitator>}
    Selected uniformly at random from their domains.

    IMPORTANT:
    - Does NOT use preferred facilitators.
    - All facilitators are available as required by instructions.
    """
    room = random.choice(list(ROOMS.keys()))
    time = random.choice(TIME_SLOTS)
    facilitator = random.choice(FACILITATORS)

    return {
        "room": room,
        "time": time,
        "facilitator": facilitator,
    }


# -----------------------------------------------------------
# Generate One Full Random Schedule
# -----------------------------------------------------------
def random_schedule():
    """
    Creates a Schedule object and fills in ALL 11 activities
    with random (room, time, facilitator) assignments.
    """
    schedule = Schedule()

    for activity in ACTIVITIES.keys():
        schedule.assignments[activity] = random_assignment()

    return schedule


# -----------------------------------------------------------
# Initialize Full Population (Generation 0)
# -----------------------------------------------------------
def initialize_population(size=250):
    """
    Returns a list of <size> random Schedule objects.
    Requirement: size >= 250
    """
    population = []
    for _ in range(size):
        population.append(random_schedule())
    return population
