# -----------------------------------------------------------
#  STREAMLIT UI FOR GENETIC ALGORITHM SCHEDULER
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from ga.engine import run_genetic_algorithm
from ga.schedule import Schedule
from ga.fitness import compute_violations

# Persistent GA results across UI interactions
if "ga_results" not in st.session_state:
    st.session_state.ga_results = None

st.set_page_config(
    page_title="Genetic Algorithm Scheduler",
    layout="wide"
)

st.title("📅 SLA Activity Scheduler — Genetic Algorithm")
st.write("This tool uses a genetic algorithm to optimize room, time, and facilitator assignments.")

# -----------------------------------------------------------
# Sidebar Controls
# -----------------------------------------------------------

st.sidebar.header("⚙️ GA Configuration")

population_size = st.sidebar.slider(
    "Population Size",
    min_value=250,
    max_value=1000,
    value=250,
    step=50
)

mutation_rate = st.sidebar.slider(
    "Initial Mutation Rate",
    min_value=0.0005,
    max_value=0.05,
    value=0.01,
    step=0.0005,
    format="%.4f"
)

min_generations = st.sidebar.slider(
    "Minimum Generations",
    min_value=100,
    max_value=300,
    value=100,
    step=10
)

max_generations = st.sidebar.slider(
    "Maximum Generations",
    min_value=200,
    max_value=1000,
    value=500,
    step=50
)

crossover_mode = st.sidebar.radio(
    "Crossover Mode",
    ["single_point", "uniform"],
    index=0
)

elitism_count = st.sidebar.slider(
    "Elitism Count",
    min_value=1,
    max_value=10,
    value=1
)

run_button = st.sidebar.button("🚀 Run Genetic Algorithm")


# -----------------------------------------------------------
# Run GA
# -----------------------------------------------------------

if run_button:
    with st.spinner("Running Genetic Algorithm... This may take a moment."):
        st.session_state.ga_results = run_genetic_algorithm(
            population_size=population_size,
            min_generations=min_generations,
            max_generations=max_generations,
            initial_mutation_rate=mutation_rate,
            crossover_mode=crossover_mode,
            elitism_count=elitism_count
        )


# -----------------------------------------------------------
# SHOW RESULTS (persistent)
# -----------------------------------------------------------
if st.session_state.ga_results is not None:

    results = st.session_state.ga_results
    best_schedule = results["best_schedule"]
    history = results["history"]
    generations_run = results["generations_run"]

    df_history = pd.DataFrame(history)

    # Format improvement % nicely
    if "improvement" in df_history.columns:
        df_history["improvement"] = df_history["improvement"].apply(
            lambda x: f"{x:.2f}%" if x is not None and not pd.isna(x) else "N/A"
        )

    st.success(f"Genetic Algorithm completed in **{generations_run}** generations!")

    # -----------------------------------------------------------
    # Fitness Plot
    # -----------------------------------------------------------
    st.subheader("📈 Fitness Over Generations")

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df_history["generation"], df_history["best"], label="Best Fitness", linewidth=2)
    ax.plot(df_history["generation"], df_history["avg"], label="Average Fitness", linestyle="--")
    ax.plot(df_history["generation"], df_history["worst"], label="Worst Fitness", linestyle=":")
    ax.set_xlabel("Generation")
    ax.set_ylabel("Fitness")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()

    st.pyplot(fig)

    # -----------------------------------------------------------
    # Best Schedule Table
    # -----------------------------------------------------------
    st.subheader("🏆 Best Schedule (Final Generation)")

    row_mode = st.radio(
        "How many activities to show?",
        ["First 6", "All"],
        horizontal=True
    )

    sort_mode = st.radio(
        "Sort Schedule By:",
        ["Time", "Activity"],
        horizontal=True
    )

    df = best_schedule.to_dataframe()

    time_order = {
        "10 AM": 10,
        "11 AM": 11,
        "12 PM": 12,
        "1 PM": 13,
        "2 PM": 14,
        "3 PM": 15,
    }

    if sort_mode == "Time":
        df["TimeSort"] = df["Time"].map(time_order)
        df = df.sort_values(["TimeSort", "Activity"], ascending=[True, True]).drop(columns=["TimeSort"])
    else:
        df = df.sort_values("Activity")

    df_display = df.head(6) if row_mode == "First 6" else df
    st.dataframe(df_display, use_container_width=True)

    # -----------------------------------------------------------
    # Optional: Group by Room / Facilitator
    # -----------------------------------------------------------
    st.subheader("📚 Optional Groupings")

    with st.expander("🏫 Group Activities by Room"):
        grouped_room = df.groupby("Room")
        for room, table in grouped_room:
            st.markdown(f"### Room: **{room}**")
            st.dataframe(table, use_container_width=True)

    with st.expander("🧑‍🏫 Group Activities by Facilitator"):
        grouped_fac = df.groupby("Facilitator")
        for fac, table in grouped_fac:
            st.markdown(f"### Facilitator: **{fac}**")
            st.dataframe(table, use_container_width=True)

    # -----------------------------------------------------------
    # Downloads
    # -----------------------------------------------------------
    st.subheader("⬇️ Downloads")

    csv = df.to_csv(index=False).encode("utf-8")
    best_schedule.save_csv("output/best_schedule.csv")

    st.download_button(
        label="📥 Download Schedule as CSV",
        data=csv,
        file_name="best_schedule.csv",
        mime="text/csv"
    )

    with st.expander("📊 View Full Generation Metrics"):
        st.dataframe(df_history, use_container_width=True)

    hist_csv = df_history.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Fitness History CSV",
        data=hist_csv,
        file_name="fitness_history.csv",
        mime="text/csv"
    )

    # -----------------------------------------------------------
    # Violations
    # -----------------------------------------------------------
    st.subheader("⚠️ Constraint Violations")

    violations = compute_violations(best_schedule)

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Room Conflicts:** {violations['room_conflicts']}")
        st.write(f"**Room Too Small:** {violations['room_too_small']}")
        st.write(f"**Room Too Big (>1.5x):** {violations['room_too_big_15']}")
        st.write(f"**Room Too Big (>3x):** {violations['room_too_big_30']}")

    with col2:
        st.write(f"**Facilitator Overloads (>4):** {violations['facilitator_overload']}")
        st.write(f"**Facilitator Underloads (<3):** {violations['facilitator_underload']}")
        st.write(f"**Same-Time Facilitator Conflicts:** {violations['facilitator_same_time_conflict']}")
        st.write(f"**SLA101A/B Same Slot Violations:** {violations['sla101_same_slot']}")
        st.write(f"**SLA191A/B Same Slot Violations:** {violations['sla191_same_slot']}")
        st.write(f"**SLA101 ↔ SLA191 Same Slot:** {violations['sla101_191_same_slot']}")
        st.write(f"**SLA101 ↔ SLA191 Distance Issues:** {violations['sla101_191_distance_issue']}")
        st.write(f"**SLA101 ↔ SLA191 One Hour Gap Count:** {violations['sla101_191_one_hour_gap']}")
        st.write(f"**SLA101 ↔ SLA191 Consecutive Slot Count:** {violations['sla101_191_consecutive_ok']}")

else:
    st.info("Configure parameters in the sidebar and click **Run Genetic Algorithm** to begin.")
