# -----------------------------------------------------------
#  PHASE 2: Schedule Representation for Genetic Algorithm
# -----------------------------------------------------------

from copy import deepcopy
import pandas as pd
from ga.data import ACTIVITIES, ROOMS, TIME_SLOTS, FACILITATORS


class Schedule:
    """
    Represents a full schedule of 11 activities.
    Each activity has:
        - room
        - time
        - facilitator

    This class provides:
        - initialization
        - deep copying
        - exporting to table/CSV
        - readable string formatting
    """

    def __init__(self, assignments=None):
        """
        assignments: optional dictionary like:
            {
                "SLA101A": {"room": "...", "time": "...", "facilitator": "..."},
                ...
            }
        If None → create empty structure (GA will fill later)
        """
        if assignments is None:
            # Create empty assignment slots for all activities
            self.assignments = {
                activity: {"room": None, "time": None, "facilitator": None}
                for activity in ACTIVITIES.keys()
            }
        else:
            self.assignments = assignments

        # Set fitness score placeholder (optional but convenient)
        self.fitness = None

    # -----------------------------------------------------------
    # Deep Copy
    # -----------------------------------------------------------
    def copy(self):
        """Return a deep copy of this schedule."""
        return Schedule(deepcopy(self.assignments))

    # -----------------------------------------------------------
    # Pretty Print
    # -----------------------------------------------------------
    def __str__(self):
        lines = []
        for activity, data in self.assignments.items():
            lines.append(
                f"{activity:8s}  |  Room: {data['room']:<10s}  |  "
                f"Time: {data['time']:<5s}  |  Facilitator: {data['facilitator']}"
            )
        return "\n".join(lines)

    # -----------------------------------------------------------
    # Export as Pandas DataFrame (perfect for Streamlit)
    # -----------------------------------------------------------
    def to_dataframe(self):
        """
        Convert schedule into a DataFrame:
        Activity | Room | Time | Facilitator
        """
        records = []
        for activity, data in self.assignments.items():
            records.append({
                "Activity": activity,
                "Room": data["room"],
                "Time": data["time"],
                "Facilitator": data["facilitator"],
            })
        return pd.DataFrame(records)

    # -----------------------------------------------------------
    # Export CSV
    # -----------------------------------------------------------
    def save_csv(self, filepath):
        df = self.to_dataframe()
        df.to_csv(filepath, index=False)
