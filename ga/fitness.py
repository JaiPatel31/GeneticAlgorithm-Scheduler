# -----------------------------------------------------------
#  PHASE 4: Fitness Function (Appendix A)
# -----------------------------------------------------------

from ga.data import (
    ACTIVITIES,
    ROOMS,
    TIME_SLOTS,
    PAIR_SLA101,
    PAIR_SLA191,
    CROSS_101_191,
)


# Map time labels to indices for easy distance calculations
TIME_INDEX = {t: i for i, t in enumerate(TIME_SLOTS)}


def _time_diff_hours(time_a: str, time_b: str) -> int:
    """
    Returns the absolute 'step' difference between two time slots.
    Each step is 1 hour (10 AM -> 11 AM -> 12 PM -> ...).
    """
    if time_a not in TIME_INDEX or time_b not in TIME_INDEX:
        return 0
    return abs(TIME_INDEX[time_a] - TIME_INDEX[time_b])


def _is_beach_or_roman(room_name: str) -> bool:
    """Return True if room is in Beach or Roman buildings."""
    if room_name is None:
        return False
    return room_name.startswith("Beach") or room_name.startswith("Roman")


def _score_pair_time_spacing(act1: str, act2: str, assignments: dict) -> float:
    """
    Special rule for the two sections of SLA 101 or SLA 191:
        - More than 4 hours apart: +0.5
        - Both in the same time slot: -0.5
    This is computed once per pair and added to act1's score.
    """
    a1 = assignments.get(act1)
    a2 = assignments.get(act2)
    if a1 is None or a2 is None:
        return 0.0

    t1 = a1.get("time")
    t2 = a2.get("time")
    if t1 is None or t2 is None:
        return 0.0

    if t1 == t2:
        # Same time slot: penalty
        return -0.5

    diff = _time_diff_hours(t1, t2)
    # More than 4 hours apart
    if diff > 4:
        return +0.5

    return 0.0


def _score_cross_101_191(a101: str, a191: str, assignments: dict) -> float:
    """
    Special rules for SLA101 (A/B) vs SLA191 (A/B):

      - Consecutive time slots (e.g., 10 & 11): +0.5
          In this case only: if one is in Beach/Roman and the other is not:
              -0.4 (we want to avoid long walks between consecutive classes)

      - Separated by 1 hour (e.g., 10 & 12): +0.25

      - Same time slot: -0.25

    This is computed once per pair and added to the 101 side's activity score.
    """
    a_101 = assignments.get(a101)
    a_191 = assignments.get(a191)
    if a_101 is None or a_191 is None:
        return 0.0

    t1 = a_101.get("time")
    t2 = a_191.get("time")
    r1 = a_101.get("room")
    r2 = a_191.get("room")

    if t1 is None or t2 is None:
        return 0.0

    score = 0.0

    if t1 == t2:
        # Same time slot
        score -= 0.25
        return score

    diff = _time_diff_hours(t1, t2)

    # Consecutive time slots
    if diff == 1:
        score += 0.5
        # Check distance penalty: one in Beach/Roman, other not
        if r1 is not None and r2 is not None:
            in_b_or_r_1 = _is_beach_or_roman(r1)
            in_b_or_r_2 = _is_beach_or_roman(r2)
            if in_b_or_r_1 ^ in_b_or_r_2:
                score -= 0.4
        return score

    # Separated by 1 hour (one-hour gap, e.g., 10 & 12)
    if diff == 2:
        score += 0.25

    return score


def compute_schedule_fitness(schedule) -> float:
    """
    Compute the total fitness of a schedule according to Appendix A.

    Strategy:
      - Precompute helper counts:
          * room-time usage
          * facilitator-time usage
          * facilitator total load
      - For each activity:
          * Room size fitness
          * Room-time conflict penalty
          * Facilitator preference bonus/penalty
          * Facilitator concurrent load (same-time) bonus/penalty
          * Facilitator overall load (too many / too few)
          * Special SLA101/191 rules added to the "first" activity in each pair

      - Sum all activity fitness values to get schedule fitness.
    """
    assignments = schedule.assignments

    # --------------------------------------------
    # Precompute counts for conflicts & loads
    # --------------------------------------------
    room_time_counts: dict[tuple, int] = {}
    fac_time_counts: dict[tuple, int] = {}
    fac_total_counts: dict[str, int] = {}

    for activity, data in assignments.items():
        room = data.get("room")
        time = data.get("time")
        fac = data.get("facilitator")

        if room is not None and time is not None:
            key_rt = (room, time)
            room_time_counts[key_rt] = room_time_counts.get(key_rt, 0) + 1

        if fac is not None and time is not None:
            key_ft = (fac, time)
            fac_time_counts[key_ft] = fac_time_counts.get(key_ft, 0) + 1

        if fac is not None:
            fac_total_counts[fac] = fac_total_counts.get(fac, 0) + 1

    # --------------------------------------------
    # Per-activity fitness accumulation
    # --------------------------------------------
    activity_scores: dict[str, float] = {}

    for activity, data in assignments.items():
        score = 0.0

        room = data.get("room")
        time = data.get("time")
        fac = data.get("facilitator")

        # -------- Room size fitness ------------
        # Uses expected enrollment vs room capacity
        if room is not None and activity in ACTIVITIES:
            expected = ACTIVITIES[activity]["expected"]
            capacity = ROOMS.get(room)
            if capacity is not None and expected > 0:
                if capacity < expected:
                    # Room too small
                    score -= 0.5
                else:
                    ratio = capacity / expected
                    if ratio > 3.0:
                        score -= 0.4
                    elif ratio > 1.5:
                        score -= 0.2
                    else:
                        # Good fit
                        score += 0.3

        # -------- Facilitator preference fitness ------------
        if fac is not None and activity in ACTIVITIES:
            preferred = ACTIVITIES[activity]["preferred"]
            other = ACTIVITIES[activity]["other"]
            if fac in preferred:
                score += 0.5
            elif fac in other:
                score += 0.2
            else:
                score -= 0.1

        # -------- Room-time conflict penalty ------------
        if room is not None and time is not None:
            if room_time_counts.get((room, time), 0) > 1:
                # This activity shares a room/time slot with at least one other activity
                score -= 0.5

        # -------- Facilitator same-time load ------------
        if fac is not None and time is not None:
            count_ft = fac_time_counts.get((fac, time), 0)
            if count_ft == 1:
                score += 0.2
            elif count_ft > 1:
                score -= 0.2

        # -------- Facilitator overall load ------------
        if fac is not None:
            total = fac_total_counts.get(fac, 0)

            # Overloaded facilitator
            if total > 4:
                score -= 0.5

            # Underused (<3)
            elif total < 3:
                if fac == "Tyler":
                    # Tyler exception: NO penalty ONLY if total <2
                    if total >= 2:
                        score -= 0.4  # Tyler teaching exactly 2 → penalty applies
                else:
                    score -= 0.4

        # -------- Special SLA101/SLA191 spacing rules ------------
        # To avoid double-counting, we only apply pair-based scores
        # when this activity is the "first" member in the pair.

        # SLA101A/SLA101B
        if activity == PAIR_SLA101[0]:
            score += _score_pair_time_spacing(PAIR_SLA101[0], PAIR_SLA101[1], assignments)

        # SLA191A/SLA191B
        if activity == PAIR_SLA191[0]:
            score += _score_pair_time_spacing(PAIR_SLA191[0], PAIR_SLA191[1], assignments)

        # Cross pairs: SLA101x vs SLA191y
        # Add the entire cross-pair score to the SLA101 (first element) side.
        for (a101, a191) in CROSS_101_191:
            if activity == a101:
                score += _score_cross_101_191(a101, a191, assignments)

        activity_scores[activity] = score

    # Sum up all activity scores to get schedule fitness
    total_fitness = sum(activity_scores.values())
    # Store it on the schedule object as a convenience
    schedule.fitness = total_fitness
    return total_fitness
# -----------------------------------------------------------
# COMPLETE CONSTRAINT VIOLATION CHECKER (Matches Fitness Exactly)
# -----------------------------------------------------------

def compute_violations(schedule):
    """
    Returns a dictionary of violation counts that correspond exactly to
    the rules used by the fitness function.

    Includes:
      - room conflicts
      - room too small
      - room too big (1.5x, 3x)
      - facilitator overloads (>4)
      - facilitator underloads (<3) with correct Tyler exception
      - facilitator same-time conflicts (>1 in same time slot)
      - SLA101A/B same-slot or correct spacing
      - SLA191A/B same-slot or correct spacing
      - SLA101 vs SLA191 spacing & distance penalties
    """

    assignments = schedule.assignments

    # Counters
    violations = {
        "room_conflicts": 0,
        "room_too_small": 0,
        "room_too_big_15": 0,
        "room_too_big_30": 0,
        "facilitator_overload": 0,
        "facilitator_underload": 0,
        "facilitator_same_time_conflict": 0,
        "sla101_same_slot": 0,
        "sla191_same_slot": 0,
        "sla101_191_same_slot": 0,
        "sla101_191_distance_issue": 0,
        "sla101_191_one_hour_gap": 0,
        "sla101_191_consecutive_ok": 0,
    }

    # Precompute data for conflicts & loads
    room_time_counts = {}
    fac_time_counts = {}
    fac_total = {}

    # -----------------------------------------------------------
    # PASS 1: Count things needed for violations
    # -----------------------------------------------------------
    for act, d in assignments.items():
        room = d["room"]
        time = d["time"]
        fac = d["facilitator"]

        # Room-time conflicts
        key_rt = (room, time)
        room_time_counts[key_rt] = room_time_counts.get(key_rt, 0) + 1

        # Facilitator same-time load
        key_ft = (fac, time)
        fac_time_counts[key_ft] = fac_time_counts.get(key_ft, 0) + 1

        # Facilitator total load
        fac_total[fac] = fac_total.get(fac, 0) + 1

        # Room size violations
        expected = ACTIVITIES[act]["expected"]
        capacity = ROOMS.get(room)

        if capacity < expected:
            violations["room_too_small"] += 1
        else:
            ratio = capacity / expected
            if ratio > 3.0:
                violations["room_too_big_30"] += 1
            elif ratio > 1.5:
                violations["room_too_big_15"] += 1

    # -----------------------------------------------------------
    # Room-time conflict count
    # -----------------------------------------------------------
    for (room, time), count in room_time_counts.items():
        if count > 1:
            violations["room_conflicts"] += (count - 1)

    # -----------------------------------------------------------
    # Facilitator overload/underload & same-time conflicts
    # -----------------------------------------------------------
    for fac, total in fac_total.items():

        # Overload (>4)
        if total > 4:
            violations["facilitator_overload"] += 1

        # Underload (<3)
        if total < 3:
            if fac == "Tyler":
                # Tyler exception: no penalty ONLY if <2
                if total >= 2:
                    violations["facilitator_underload"] += 1
            else:
                violations["facilitator_underload"] += 1

    for (fac, time), count in fac_time_counts.items():
        if count > 1:
            violations["facilitator_same_time_conflict"] += (count - 1)

    # -----------------------------------------------------------
    # SLA101A/B and SLA191A/B same-slot or spacing
    # -----------------------------------------------------------
    # 101 pair
    t1 = assignments[PAIR_SLA101[0]]["time"]
    t2 = assignments[PAIR_SLA101[1]]["time"]
    if t1 == t2:
        violations["sla101_same_slot"] += 1

    # 191 pair
    t3 = assignments[PAIR_SLA191[0]]["time"]
    t4 = assignments[PAIR_SLA191[1]]["time"]
    if t3 == t4:
        violations["sla191_same_slot"] += 1

    # -----------------------------------------------------------
    # SLA101 ↔ SLA191 cross-pair rules
    # -----------------------------------------------------------
    for (a101, a191) in CROSS_101_191:
        d101 = assignments[a101]
        d191 = assignments[a191]

        time101 = d101["time"]
        time191 = d191["time"]
        room101 = d101["room"]
        room191 = d191["room"]

        if time101 == time191:
            violations["sla101_191_same_slot"] += 1
            continue

        diff = _time_diff_hours(time101, time191)

        if diff == 1:
            # Consecutive OK
            violations["sla101_191_consecutive_ok"] += 1
            # Check distance penalty
            inA = _is_beach_or_roman(room101)
            inB = _is_beach_or_roman(room191)
            if inA ^ inB:
                violations["sla101_191_distance_issue"] += 1

        elif diff == 2:
            violations["sla101_191_one_hour_gap"] += 1

    return violations
