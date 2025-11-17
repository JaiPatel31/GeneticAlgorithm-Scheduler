# -----------------------------------------------------------
#  PHASE 1: DATA DEFINITIONS FOR GENETIC ALGORITHM SCHEDULER
# -----------------------------------------------------------

# -------------------------------
# Facilitators (10 total)
# -------------------------------
FACILITATORS = [
    "Lock", "Glen", "Banks", "Richards", "Shaw",
    "Singer", "Uther", "Tyler", "Numen", "Zeldin"
]

# -------------------------------
# Time Slots (6 total)
# Order matters for “consecutive” rules
# -------------------------------
TIME_SLOTS = [
    "10 AM",
    "11 AM",
    "12 PM",
    "1 PM",
    "2 PM",
    "3 PM"
]


# -------------------------------
# Rooms + Capacities
# -------------------------------
ROOMS = {
    "Beach 201": 18,
    "Beach 301": 25,
    "Frank 119": 95,
    "Loft 206": 55,
    "Loft 310": 48,
    "James 325": 110,
    "Roman 201": 40,
    "Roman 216": 80,
    "Slater 003": 32,
}


# -------------------------------
# Activities (11 total)
# Includes: expected enrollment,
# preferred facilitators list,
# other facilitators list
# -------------------------------
ACTIVITIES = {
    "SLA101A": {
        "expected": 40,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA101B": {
        "expected": 35,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA191A": {
        "expected": 45,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA191B": {
        "expected": 40,
        "preferred": ["Glen", "Lock", "Banks"],
        "other": ["Numen", "Richards", "Shaw", "Singer"],
    },
    "SLA201": {
        "expected": 60,
        "preferred": ["Glen", "Banks", "Zeldin", "Lock", "Singer"],
        "other": ["Richards", "Uther", "Shaw"],
    },
    "SLA291": {
        "expected": 50,
        "preferred": ["Glen", "Banks", "Zeldin", "Lock", "Singer"],
        "other": ["Richards", "Uther", "Shaw"],
    },
    "SLA303": {
        "expected": 25,
        "preferred": ["Glen", "Zeldin"],
        "other": ["Banks"],
    },
    "SLA304": {
        "expected": 20,
        "preferred": ["Singer", "Uther"],
        "other": ["Richards"],
    },
    "SLA394": {
        "expected": 15,
        "preferred": ["Tyler", "Singer"],
        "other": ["Richards", "Zeldin"],
    },
    "SLA449": {
        "expected": 30,
        "preferred": ["Tyler", "Zeldin", "Uther"],
        "other": ["Zeldin", "Shaw"],
    },
    "SLA451": {
        "expected": 90,
        "preferred": ["Lock", "Banks", "Zeldin"],
        "other": ["Tyler", "Singer", "Shaw", "Glen"],
    },
}


# -------------------------------
# Special Activity Pairs (for SLA rules)
# -------------------------------
PAIR_SLA101 = ("SLA101A", "SLA101B")
PAIR_SLA191 = ("SLA191A", "SLA191B")

# All cross-pairs (101* vs 191*)
CROSS_101_191 = [
    ("SLA101A", "SLA191A"),
    ("SLA101A", "SLA191B"),
    ("SLA101B", "SLA191A"),
    ("SLA101B", "SLA191B"),
]


# -------------------------------
# (Optional) Equipment requirements
# Not required by base assignment, but available
# -------------------------------
ACTIVITY_EQUIPMENT = {
    "SLA304": {"lab": True, "projector": False},
    "SLA303": {"lab": True, "projector": True},
    "SLA191A": {"lab": True},
    "SLA191B": {"lab": True},
    "SLA291": {"lab": True},
    "SLA449": {"projector": True},
    "SLA451": {"lab": True, "projector": True},
}

ROOM_EQUIPMENT = {
    "Beach 201": {"lab": False, "projector": True},
    "Beach 301": {"lab": True, "projector": True},
    "Loft 310": {"lab": True, "projector": False},
    "Frank 119": {"lab": True, "projector": True},
    "Roman 216": {"lab": True, "projector": True},
    "Slater 003": {"lab": True, "projector": True},
    "James 325": {"lab": True, "projector": True},
    # Rooms without equipment defaults:
    "Loft 206": {"lab": False, "projector": False},
    "Roman 201": {"lab": False, "projector": False},
}
