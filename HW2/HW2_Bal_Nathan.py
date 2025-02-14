import scipy
import numpy as np
import matplotlib.pyplot as plt
import random

def get_probabilities(drift=0):
    probs = [
        np.random.normal(0, 5),
        np.random.normal(-0.5, 12),
        np.random.normal(2, 3.9),
        np.random.normal(-0.5, 7),
        np.random.normal(-1.2, 8),
        np.random.normal(-3, 7),
        np.random.normal(-10, 20),
        np.random.normal(-0.5, 1),
        np.random.normal(-1, 2),
        np.random.normal(1, 6),
        np.random.normal(0.7, 4),
        np.random.normal(-6, 11),
        np.random.normal(-7, 1),
        np.random.normal(-0.5, 2),
        np.random.normal(-6.5, 1),
        np.random.normal(-3, 6),
        np.random.normal(0, 8),
        np.random.normal(2, 3.9),
        np.random.normal(-9, 12),
        np.random.normal(-1, 6),
        np.random.normal(-4.5, 8)
    ]
    return probs

def get_dynamics_probabilities(step, drift=-0.001):
    probs = [
        np.random.normal(0 + drift * step, 5),    # Bandit 0 (will get a shift at step 3000)
        np.random.normal(-0.5 + drift * step, 12),
        np.random.normal(2 + drift * step, 3.9),  # Bandit 2 (will get a shift at step 3000)
        np.random.normal(-0.5 + drift * step, 7),
        np.random.normal(-1.2 + drift * step, 8),
        np.random.normal(-3 + drift * step, 7),
        np.random.normal(-10 + drift * step, 20),
        np.random.normal(-0.5 + drift * step, 1), # Bandit 7 (special case, shifts at step 3000)
        np.random.normal(-1 + drift * step, 2),
        np.random.normal(1 + drift * step, 6),
        np.random.normal(0.7 + drift * step, 4),
        np.random.normal(-6 + drift * step, 11),
        np.random.normal(-7 + drift * step, 1),
        np.random.normal(-0.5 + drift * step, 2),
        np.random.normal(-6.5 + drift * step, 1),
        np.random.normal(-3 + drift * step, 6),
        np.random.normal(0 + drift * step, 8),
        np.random.normal(2 + drift * step, 3.9),
        np.random.normal(-9 + drift * step, 12),  # Bandit 18 (will shift at step 3000)
        np.random.normal(-1 + drift * step, 6),
        np.random.normal(-4.5 + drift * step, 8)
    ]

    if step == 3000:
        probs[0] += 7
        probs[2] += 3
        probs[7] += 1
        if np.abs(probs[7]) > 3 * 1:
            probs[7] = 50
        probs[18] += 2 

    return probs

def linear_quench(t, total_steps): 
    return max(0, 1 - t / total_steps)

def asymptotic_quench(t, total_steps): 
    return 1 / (1 + 0.01 * t)

def heavy_asymptotic_quench(t, total_steps): 
    return 1 / (1 + 0.0001 * t**2)

def epsilon_greedy_exclude_best(choices, epsilon, current_best):
    if np.random.random() < epsilon:
        return np.random.choice([i for i in range(len(choices)) if i != current_best])
    else:
        return current_best
    
def weighted_exploration(choices, epsilon, counts):
    if np.random.random() < epsilon:
        unexplored_probs = 1 / (counts + 1)  # Higher probability for less explored choices
        return np.random.choice(len(choices), p=unexplored_probs / unexplored_probs.sum())
    else:
        return np.argmax(choices)

def run_thompson_sampling(n_steps, n_actions, restart_at_3000=False, is_dynamic=False):
    alpha = np.ones(n_actions)
    beta = np.ones(n_actions)
    
    average_rewards = [0]
    total_reward = 0

    for step in range(n_steps):
        if restart_at_3000 and step == 3000:
            alpha = np.ones(n_actions)
            beta = np.ones(n_actions)

        sampled_beta = [np.random.beta(alpha[a], beta[a]) for a in range(n_actions)]
        action = np.argmax(sampled_beta)
        
        if is_dynamic:
            probs = get_dynamics_probabilities(step)
        else:
            probs = get_probabilities()
        reward = probs[action]
        
        # Update the Beta distribution parameters based on reward
        if reward > 0:
            alpha[action] += 1  # Increase alpha for successes
        else:
            beta[action] += 1   # Increase beta for failures
        
        total_reward += reward
        average_rewards.append(total_reward / (step + 1))
    
    return average_rewards

def run_epsilon_greedy(epsilon, n_steps, n_actions, exploration_strategy=None, is_dynamic=False):
    Q_values = np.zeros(n_actions)
    N = np.zeros(n_actions)
    average_rewards = [0]
    total_reward = 0

    for step in range(n_steps):
        if is_dynamic:
            probs = get_dynamics_probabilities(step)
        else:
            probs = get_probabilities()

        if random.random() > epsilon:
            action = np.argmax(Q_values)
        else:
            if exploration_strategy == 'exclude_best':
                action = epsilon_greedy_exclude_best(Q_values, epsilon, np.argmax(Q_values))
            elif exploration_strategy == 'weighted_exploration':
                action = weighted_exploration(Q_values, epsilon, N)
            else:
                action = np.random.randint(n_actions)

        reward = probs[action]
        N[action] += 1
        Q_values[action] += ((1/N[action] * (reward - Q_values[action])))

        total_reward += reward
        average_rewards.append(total_reward/(step + 1))
    
    return average_rewards

def run_epsilon_greedy_quenching(quenching_strategy, n_steps, n_actions):
    Q_values = np.zeros(n_actions)
    N = np.zeros(n_actions)
    average_rewards = [0]
    total_reward = 0

    for step in range(n_steps):
        epsilon = quenching_strategy(step, n_steps)
        probs = get_probabilities()
        if random.random() > epsilon:
            action = np.argmax(Q_values)
        else:
            action = np.random.randint(n_actions)

        reward = probs[action]
        N[action] += 1
        Q_values[action] += (1 / N[action]) * (reward - Q_values[action])

        total_reward += reward
        average_rewards.append(total_reward / (step + 1))
    
    return average_rewards

# Part 1: Test epsilon values of 0.01, 0.05, 0.1, 0.4
epsilons = [0.01, 0.05, 0.1, 0.4]
n_steps = 10000
n_actions = 21
for epsilon in epsilons:
    average_rewards = run_epsilon_greedy(epsilon, n_steps, n_actions)
    plt.plot(average_rewards, label=f'epsilon={epsilon}')

# # Part 1: Run Thompson sampling method with the best epsilon-greedy result (0.05)
# n_steps = 10000
# n_actions = 21
# average_rewards_thompson = run_thompson_sampling(n_steps, n_actions)
# plt.plot(average_rewards_thompson, label='Thompson Sampling')
# average_rewards = run_epsilon_greedy(0.05, n_steps, n_actions)
# plt.plot(average_rewards, label=f'epsilon={0.05}')

# # Part 2: Epsilon Quenching Functions
# n_steps = 10000
# n_actions = 21
# strategies = {
#     'Linear Quenching': linear_quench,
#     'Asymptotic Quenching': asymptotic_quench,
#     'Heavy Asymptotic Quenching': heavy_asymptotic_quench
# }
# for label, strategy in strategies.items():
#     average_rewards = run_epsilon_greedy_quenching(strategy, n_steps, n_actions)
#     plt.plot(average_rewards, label=label)
# average_rewards = run_epsilon_greedy(0.05, n_steps, n_actions)
# plt.plot(average_rewards, label=f'epsilon={0.05}')

# # Part 2: Modifying Exploration Strategy
# n_steps = 10000
# n_actions = 21
# average_rewards_weighted_exploration = run_epsilon_greedy(0.05, n_steps, n_actions, exploration_strategy='weighted_exploration')
# plt.plot(average_rewards_weighted_exploration, label='Weighted Exploration Strategy')
# average_rewards_exclude_best = run_epsilon_greedy(0.05, n_steps, n_actions, exploration_strategy='exclude_best')
# plt.plot(average_rewards_exclude_best, label='Exclude Best Strategy')
# average_rewards_standard = run_epsilon_greedy(0.05, n_steps, n_actions)
# plt.plot(average_rewards_standard, label='Standard Epsilon-Greedy (epsilon=0.05)')

# # Part 3: Moving Bandits – Simulating Market Dynamics
# n_steps = 10000
# n_actions = 21
# average_rewards_eg = run_epsilon_greedy(0.05, n_steps, n_actions, is_dynamic=True)
# plt.plot(average_rewards_eg, label='Epsilon-Greedy (epsilon=0.05)')
# average_rewards_ts = run_thompson_sampling(n_steps, n_actions, is_dynamic=True)
# plt.plot(average_rewards_ts, label='Thompson Sampling (No Reset)')
# average_rewards_ts_reset = run_thompson_sampling(n_steps, n_actions, restart_at_3000=True, is_dynamic=True)
# plt.plot(average_rewards_ts_reset, label='Thompson Sampling (Reset at 3000)')
# average_rewards_standard = run_epsilon_greedy(0.05, n_steps, n_actions, is_dynamic=True, exploration_strategy='exclude_best')
# plt.plot(average_rewards_standard, label='Exclude Best Epsilon-Greedy (epsilon=0.05)')
# average_rewards_standard = run_epsilon_greedy(0.05, n_steps, n_actions, is_dynamic=True, exploration_strategy='weighted_exploration')
# plt.plot(average_rewards_standard, label='Weighted Exploration Epsilon-Greedy (epsilon=0.05)')

# This is needed for every part to display the plot
plt.xlabel("Steps")
plt.ylabel("Average Reward")
plt.legend()
plt.grid(True)
plt.show()