# -----------------------------------------------------------
#  PHASE 6: Genetic Algorithm Engine
# -----------------------------------------------------------

from __future__ import annotations

from statistics import mean
from typing import List, Dict, Any, Tuple

from ga.population import initialize_population
from ga.fitness import compute_schedule_fitness
from ga.selection import softmax, select_parents
from ga.crossover import single_point_crossover, uniform_crossover
from ga.mutation import mutate
from ga.data import ACTIVITIES


def evaluate_population(population) -> Tuple[list[float], float, float, float]:
    """
    Compute fitness for each schedule in the population and return:
      - list of fitness values
      - best fitness
      - avg fitness
      - worst fitness
    """
    fitness_list: List[float] = []
    for schedule in population:
        f = compute_schedule_fitness(schedule)
        fitness_list.append(f)

    best_f = max(fitness_list)
    avg_f = mean(fitness_list)
    worst_f = min(fitness_list)
    return fitness_list, best_f, avg_f, worst_f


def run_genetic_algorithm(
    population_size: int = 250,
    min_generations: int = 100,
    max_generations: int = 500,
    initial_mutation_rate: float = 0.01,
    crossover_mode: str = "single_point",  # or "uniform"
    elitism_count: int = 1,
) -> Dict[str, Any]:
    """
    Run the full genetic algorithm loop.

    Returns a dictionary containing:
      - "best_schedule": best schedule from final generation
      - "history": list of per-generation metrics:
            {
              "generation": int,
              "best": float,
              "avg": float,
              "worst": float,
              "improvement": float | None,
              "mutation_rate": float,
            }
      - "final_mutation_rate": float
      - "generations_run": int
    """

    # -----------------------------
    # 1. Initialize population
    # -----------------------------
    population = initialize_population(size=population_size)

    mutation_rate = initial_mutation_rate
    history: List[Dict[str, Any]] = []

    prev_avg = None
    generations = 0

    for gen in range(max_generations):
        generations = gen + 1  # human-readable generation count

        # -----------------------------
        # 2. Evaluate population
        # -----------------------------
        fitness_list, best_f, avg_f, worst_f = evaluate_population(population)

        # -----------------------------
        # 3. Compute improvement %
        # -----------------------------
        if prev_avg is None:
            improvement = None
        else:
            denom = prev_avg if abs(prev_avg) > 1e-9 else 1e-9
            improvement = ((avg_f - prev_avg) / abs(denom)) * 100.0  # <-- percent

        prev_avg = avg_f

        # -----------------------------
        # 4. Record metrics for this generation
        # -----------------------------
        history.append(
            {
                "generation": gen,
                "best": best_f,
                "avg": avg_f,
                "worst": worst_f,
                "improvement": improvement,
                "mutation_rate": mutation_rate,
            }
        )

        # -----------------------------
        # 5. Check stopping conditions
        # -----------------------------
        if improvement is not None and gen + 1 >= min_generations:
            # Assignment requirement:
            # "You must run at least 100 generations but you must also
            #  continue until the improvement in average fitness per generation
            #  is less than 1%."
            if improvement < 1.0:  # < 1%
                break

        # -----------------------------
        # 6. Build next generation
        # -----------------------------
        # (a) Parent selection using softmax probabilities
        probabilities = softmax(fitness_list)

        # We'll generate one child per pair to keep the new generation size ~ population_size.
        num_pairs = population_size

        parent_pairs = select_parents(population, probabilities, num_pairs)

        children = []

        for parent_a, parent_b in parent_pairs:
            # (b) Crossover
            if crossover_mode == "uniform":
                child = uniform_crossover(parent_a, parent_b)
            else:
                child = single_point_crossover(parent_a, parent_b)

            # (c) Mutation
            mutate(child, mutation_rate=mutation_rate)

            children.append(child)

        # (d) Elitism: carry over top N schedules unchanged
        # Sort population by fitness descending, keep elites
        # We reuse fitness_list and population aligned by index
        indexed = list(zip(population, fitness_list))
        indexed.sort(key=lambda x: x[1], reverse=True)

        elites = [sch for sch, _ in indexed[:elitism_count]]

        # Build the next generation
        # Ensure population size stays constant
        new_population = elites + children
        if len(new_population) > population_size:
            new_population = new_population[:population_size]
        elif len(new_population) < population_size:
            # If slightly short, just duplicate some children
            deficit = population_size - len(new_population)
            new_population.extend(children[:deficit])

        population = new_population

        # ------------------------------------------------
        # 7. (Optional) Mutation Rate Experimentation
        # ------------------------------------------------
        # The assignment says:
        #   "Once your program is running, watch what happens to the fitness
        #    score as generations increase, and then cut the mutation rate in half.
        #    As long as your results continue to improve, continue cutting the
        #    mutation rate in half until things appear to be stable."
        #
        # Instead of auto-adjusting here, we expose mutation_rate as a parameter
        # and record it in the history. In your experiments (and video), you can:
        #   - Run once with 0.01
        #   - Then again with 0.005, 0.0025, ...
        # and compare fitness curves.
        #
        # If you *want* automatic halving logic, you could add something like:
        #
        # if gen > 0 and gen % 50 == 0:
        #     mutation_rate = max(mutation_rate / 2.0, 1e-4)
        #
        # But for strict assignment interpretation, manual experimentation is fine.

    # ---------------------------------
    # End of GA loop
    # ---------------------------------

    # Identify final best schedule
    final_fitness_list, final_best, final_avg, final_worst = evaluate_population(population)
    best_index = max(range(len(population)), key=lambda i: final_fitness_list[i])
    best_schedule = population[best_index]

    result = {
        "best_schedule": best_schedule,
        "history": history,
        "final_mutation_rate": mutation_rate,
        "generations_run": generations,
    }
    return result
