import random
import statistics
import matplotlib.pyplot as plt
import numpy as np


def run_experiment(len_candidates, num_simulations, distribution_type):
    experiment_results = []

    for tests in range(num_simulations):
        if distribution_type == 'uniform':
            candidates = random.sample(range(0,5000), len_candidates)
        elif distribution_type == 'normal':
            candidates = np.random.normal(50, 10, len_candidates)
        elif distribution_type == 'beta':
            candidates = np.random.beta(2, 7, len_candidates)        
        optimal_solution_found_count = {str(i): 0 for i in range(1, len_candidates)}

        for _ in range(1000):
            candidates = np.random.beta(2, 7, len_candidates)   # beta distribution with alpha 2 and beta 7
            optimal_candidate = max(candidates)

            # This is the optimal stopping algorithm
            for i in range(1, len_candidates):
                for candidate in candidates[i:-1]:
                    if candidate > max(candidates[0:i]):
                        if candidate == optimal_candidate:
                            optimal_solution_found_count[str(i)] += 1
                        
                        break
        max_candidate = max(optimal_solution_found_count, key=optimal_solution_found_count.get)
        experiment_results.append(int(max_candidate))
        if tests % (num_simulations/10) == 0:
            print(f"The mean after {tests} tests: {statistics.mean(experiment_results)}")


    x, y = zip(*optimal_solution_found_count.items())

    print(f"\n----- Total Results from {num_simulations} tests -----")
    print(f"Mode: {statistics.mode(experiment_results)}")
    print(f"Mean: {statistics.mean(experiment_results)}")
    print(f"Percentage for Optimal Stopping the Search: {(statistics.mean(experiment_results))/len_candidates * 100}%")
    plt.plot(x,y)
    plt.show()

def simulate_investments(len_candidates, num_simulations, distribution_type):
    experiment_results = []
    result_plot = {i: 0 for i in range(100)}

    for tests in range(1, num_simulations):
        if distribution_type == 'uniform':
            candidates = np.random.uniform(1, 99, len_candidates)
        elif distribution_type == 'normal':
            candidates = np.random.normal(50, 10, len_candidates)
            candidates = np.clip(candidates, 1, 99)
        
        best_reward = 0
        best_threshold = 0

        for threshold in range(1, len_candidates):
            for candidate in candidates[threshold:-1]:
                    if candidate > max(candidates[0:threshold]):
                        reward = candidate - threshold
                        if reward > best_reward:
                            best_reward = reward
                            best_threshold = threshold

                        break

        experiment_results.append(best_threshold)
        result_plot[best_threshold] += 1
        if tests % (num_simulations/10) == 0:
            print(f"The mean after {tests} invest tests: {statistics.mean(experiment_results)}")
    
    print(f"\n----- Total Results from {num_simulations} tests -----")
    print(f"Median: {statistics.median(experiment_results)}")
    print(f"Mean: {statistics.mean(experiment_results)}")
    print(f"Percentage for Optimal Stopping the Search: {(statistics.mean(experiment_results))/len_candidates * 100}%")

    x = list(result_plot.keys())
    y = list(result_plot.values())
    plt.plot(x,y)
    plt.show()

    


# Run the experiment for part one using a uniform distribution 
# run_experiment(200, 10, 'uniform')

# Run the experiment for part one using a normal distribution with mean 50 and sd 10
# run_experiment(200, 10, 'normal')

# Run the experiment for part one using a beta distribution with alpha 2 and beta 7
# run_experiment(200, 10, 'beta')

# Run the investment experiment for part one using a uniform distribution between 1 to 99
# simulate_investments(100,1000, 'uniform')

# Run the investment experiment for part one using a normal distribution with mean 50 and sd 10
simulate_investments(100,1000, 'normal')