# 📅 SLA Activity Scheduler — Genetic Algorithm + Streamlit UI

This project implements a full **Genetic Algorithm (GA)** to optimize scheduling for the **Seminar Learning Association (SLA)**.  
The GA assigns each activity a **room**, **time slot**, and **facilitator**, then evolves solutions using fitness scoring based on the assignment’s official constraints.

This implementation includes:
- Complete GA pipeline (population → fitness → selection → crossover → mutation → elitism)
- Streamlit GUI (+5 bonus)
- Fitness visualization (best/avg/worst over generations)
- Final schedule table + CSV export
- Full compliance with Appendix A rules

---

## 🚀 Features

### ✔ Genetic Algorithm Core
- Random initial population (≥ 250 schedules)
- Softmax-based parent selection
- Single-point or uniform crossover
- Mutation with tunable rate
- Elitism to preserve strongest schedules
- Automatic fitness evaluation per generation
- Stopping conditions:
  - At least **100 generations**
  - Average fitness improvement < **1%**

### ✔ Fitness Function (Appendix A Rules)
- Room size violations
- Facilitator preference scoring
- Time slot conflicts
- Facilitator overload/underload
- SLA101A/B + SLA191A/B time-spacing rules
- SLA101 vs SLA191 interaction rules

### ✔ Streamlit UI
- Sidebar controls for all GA parameters
- “Run Genetic Algorithm” button
- Real-time fitness line chart
- Final schedule displayed as an interactive table
- Download schedule as CSV
- Expandable metrics table (generation-by-generation)

---

## 📂 Project Structure

genetic_scheduler/ \
│\
├── app.py # Streamlit GUI\
│\
├── ga/\
│ ├── data.py # Phase 1: static data definitions\
│ ├── schedule.py # Phase 2: schedule representation\
│ ├── population.py # Phase 3: random population generator\
│ ├── fitness.py # Phase 4: fitness scoring system\
│ ├── selection.py # Phase 5: softmax + parent selection\
│ ├── crossover.py # Phase 5: crossover operators\
│ ├── mutation.py # Phase 5: mutation operator\
│ ├── engine.py # Phase 6: full GA loop\
│\
├── output/\
│ ├── best_schedule.csv # Generated after GA run\
│\
└── README.md

---

## 🧠 How It Works

1. **Initialize Population**  
   Randomly generate N schedules (default: 250)

2. **Evaluate Fitness**  
   Apply Appendix A scoring for each activity and sum total fitness.

3. **Selection (Softmax)**  
   Higher fitness → more likely to be chosen for reproduction.

4. **Crossover**  
   Merge two parents using single-point or uniform crossover.

5. **Mutation**  
   Randomly mutate room/time/facilitator with configurable mutation rate.

6. **Elitism**  
   Top schedule(s) preserved each generation.

7. **Repeat** until:
   - ≥ 100 generations
   - improvement in average fitness < 1%

8. Display results in Streamlit.

---

## 🖥️ Running the Program

### 1. Install requirements
pip install -r requirements.txt



### 2. Start Streamlit UI
streamlit run app.py


### 3. Adjust GA parameters in sidebar  
Click **Run Genetic Algorithm** and watch evolution happen.

---

## 🧪 Dependencies

- Python 3.10+  
- streamlit  
- pandas  
- matplotlib  
- (optional) numpy  

---

## 🎉 Credits

Developed for **CS 461 – Artificial Intelligence**  
Implements every required constraint from Appendix A and includes optional GUI enhancements.