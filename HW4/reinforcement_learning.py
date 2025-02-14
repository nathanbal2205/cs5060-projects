import gym
from stable_baselines3 import PPO

import numpy as np
from gym import RewardWrapper

from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
import torch as th
from torch import nn
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.utils import set_random_seed

class CustomCartPoleReward(RewardWrapper):
    def __init__(self, env):
        super(CustomCartPoleReward, self).__init__(env)

    def reward(self, reward):
        x, x_dot, theta, theta_dot = self.env.state

        # New Behavior
        time_bonus = 0.01       # time-dependent bonus
        tilt_penalty = np.exp(abs(theta)) - 1       # penalize more for tilting
        new_reward = reward + time_bonus - tilt_penalty

        # Orignial Behavior
        # new_reward = reward - np.abs(theta)

        return new_reward

class CustomMLP(BaseFeaturesExtractor):
    def __init__(self, observation_space, features_dim=128):
        # Define the custom architecture
        super(CustomMLP, self).__init__(observation_space, features_dim)

        # New Behavior
        self.network = nn.Sequential(
            nn.Linear(observation_space.shape[0], 256), nn.ReLU(),  # Increased first layer size
            nn.LayerNorm(256),  # Layer normalization
            nn.Linear(256, 256), nn.ReLU(),  
            nn.Dropout(0.1),
             nn.LayerNorm(256),  # Layer normalization
            nn.Linear(256, features_dim)
        )

        # Original Behavior
        # self.network = nn.Sequential(
        #     nn.Linear(observation_space.shape[0], 128), nn.ReLU(),
        #     nn.Linear(128, 128), nn.ReLU(),
        #     nn.Linear(128, features_dim)
        # )

    def forward(self, x):
        return self.network(x)

# Custom Behavior
env = CustomCartPoleReward(gym.make("CartPole-v1"))

# Baseline Original Behavior
# env = gym.make("CartPole-v1")

# Custom Behavior
model = PPO("MlpPolicy", env, policy_kwargs=dict(
    activation_fn=th.nn.ReLU, 
    net_arch=[128, 128], 
    features_extractor_class=CustomMLP
), verbose=1)

# Baseline Orignial Behavior
# model = PPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=10000)

custom_rewards = []
episodes = 10

for episode in range(episodes):
    state, _ = env.reset()
    done = False
    episode_reward = 0
    steps = 0

    while not done:
        action, _ = model.predict(state, deterministic=True)
        state, reward, done, _, _ = env.step(action)
        episode_reward += reward

        if steps % 100000 == 0:
            print(f"Step - State: {state}, Reward: {reward}, Done: {done}")

        steps += 1

    custom_rewards.append(episode_reward)

avg_custom_reward = sum(custom_rewards) / episodes
print(f"Average reward with custom reward function: {avg_custom_reward}")