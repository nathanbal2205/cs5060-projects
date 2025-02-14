# HW4: Reinforcement Learning

Author: Nathan Bal

### Part 1: Modify the Reward Function
1.  Time-dependent Bonus:
    *   Encourages Longer Balancing: Adding a small reward proportional to the time step    motivates the agent to keep the pole upright for as long as possible.
    *   Smoother Reward Signal: This makes the reward function more continuous, improving gradient-based optimization.
    *   Potential Effects: The agent may prioritize strategies that extend survival time, even if the pole tilts slightly more than desired. Encourages exploration of more stable balancing strategies.

2.  Penalize more for Tilting:
    *   Exponential Tilt Penalty: By penalizing deviations from the upright position more severely, the agent is encouraged to minimize the angle of the pole.
    *   Balancing vs. Centering Trade-off: Penalizing tilting too harshly may lead to overly cautious behaviors, such as avoiding actions that could correct position for fear of tilting.
    *   Potential Effects: Improves stability of the pole but might cause less exploration of edge-case scenarios. Makes learning more challenging initially as the agent adjusts to stricter penalties.

### Part 2: Modify the Model Architecture
1.  Layer Normalization:
    *   Stability in Training: Layer normalization reduces fluctuations in the activation magnitudes, making training more predictable and improving gradient flow.
    *   Robustness Across Scenarios: Ensures consistent performance regardless of varying input scales or environments.
    *   Potential Effects: Faster convergence due to stabilized learning dynamics. Reduced sensitivity to hyperparameter tuning, such as learning rate or batch size.

2.  Increase First Layer Size:
    *   Higher Capacity for Representation: Larger initial layers enable the model to better capture complex features in the input state.
    *   More Flexibility for Learning: The model can accommodate more diverse strategies and adapt to varying reward signals.
    *   Potential Effects: Enhanced performance for more complex or noisy reward functions. Slightly increased computational cost and potential risk of overfitting without proper regularization.

### Performance Metrics
*   **Example Baseline Performace Metrics with Original Behavior:**
    The agent achieved an average reward of 61.1. The reward function was primarily based on the angle of the pole (penalizing tilt) without any additional bonuses, resulting in limited improvements during training.
    ```
        -----------------------------------------
    | rollout/                |             |
    |    ep_len_mean          | 61.1        |
    |    ep_rew_mean          | 61.1        |
    | time/                   |             |
    |    fps                  | 1583        |
    |    iterations           | 5           |
    |    time_elapsed         | 6           |
    |    total_timesteps      | 10240       |
    | train/                  |             |
    |    approx_kl            | 0.010364626 |
    |    clip_fraction        | 0.11        |
    |    clip_range           | 0.2         |
    |    entropy_loss         | -0.61       |
    |    explained_variance   | 0.319       |
    |    learning_rate        | 0.0003      |
    |    loss                 | 33          |
    |    n_updates            | 40          |
    |    policy_gradient_loss | -0.0229     |
    |    value_loss           | 64          |
    -----------------------------------------
    Average reward with custom reward function: 222.6
    ```

*   **Example Performace Metrics with just Modified Reward Function:**
    When applying the modified reward function, which includes a time-dependent bonus and a more aggressive tilt penalty, the agent’s average reward increased to 429.29. This significant improvement indicates that penalizing the tilt more harshly and rewarding longer balancing times leads to better overall performance. The agent took longer on average to balance the pole, with an episode length of 64.3, while the loss and value loss decreased, showing more stable training.
    ```
    ----------------------------------------
    | rollout/                |            |
    |    ep_len_mean          | 64.3       |
    |    ep_rew_mean          | 59.6       |
    | time/                   |            |
    |    fps                  | 1582       |
    |    iterations           | 5          |
    |    time_elapsed         | 6          |
    |    total_timesteps      | 10240      |
    | train/                  |            |
    |    approx_kl            | 0.00957237 |
    |    clip_fraction        | 0.0791     |
    |    clip_range           | 0.2        |
    |    entropy_loss         | -0.62      |
    |    explained_variance   | 0.389      |
    |    learning_rate        | 0.0003     |
    |    loss                 | 15.8       |
    |    n_updates            | 40         |
    |    policy_gradient_loss | -0.0159    |
    |    value_loss           | 52         |
    ----------------------------------------
    Average reward with custom reward function: 429.29
    ```

*   **Example Performace Metrics with just Modified Model Architecture:**
    Introducing the new model architecture featuring larger layers and normalization resulted in an even more noticeable improvement. The average reward increased to 495.4, suggesting that the increased model complexity helped the agent learn more effectively. The agent was able to achieve higher episode lengths (79.3) and showed better learning stability, evidenced by a lower loss value of 4.22 and a better explained variance of 0.736, indicating the model’s improved ability to capture and predict states.
    ```
    ----------------------------------------
    | rollout/                |            |
    |    ep_len_mean          | 79.3       |
    |    ep_rew_mean          | 79.3       |
    | time/                   |            |
    |    fps                  | 1158       |
    |    iterations           | 5          |
    |    time_elapsed         | 8          |
    |    total_timesteps      | 10240      |
    | train/                  |            |
    |    approx_kl            | 0.03538806 |
    |    clip_fraction        | 0.238      |
    |    clip_range           | 0.2        |
    |    entropy_loss         | -0.537     |
    |    explained_variance   | 0.736      |
    |    learning_rate        | 0.0003     |
    |    loss                 | 4.22       |
    |    n_updates            | 40         |
    |    policy_gradient_loss | -0.00633   |
    |    value_loss           | 12.3       |
    ----------------------------------------
    Average reward with custom reward function: 495.4
    ```

*   **Example Performace Metrics with Modified Reward Function and Model Architecture:**
    Combining both the modified reward function and the more complex model architecture led to the highest performance, with an average reward of 537.2. The agent was able to balance the pole for longer periods (episode length of 75) and produced more consistent results, demonstrating that both adjustments contributed synergistically to improved learning. The entropy loss and explained variance suggest that the model was both more stable and better at exploring the environment, while the reward penalties helped it avoid poor policies.
    ```
    -----------------------------------------
    | rollout/                |             |
    |    ep_len_mean          | 75          |
    |    ep_rew_mean          | 71          |
    | time/                   |             |
    |    fps                  | 1132        |
    |    iterations           | 5           |
    |    time_elapsed         | 9           |
    |    total_timesteps      | 10240       |
    | train/                  |             |
    |    approx_kl            | 0.022894498 |
    |    clip_fraction        | 0.242       |
    |    clip_range           | 0.2         |
    |    entropy_loss         | -0.552      |
    |    explained_variance   | 0.655       |
    |    learning_rate        | 0.0003      |
    |    loss                 | 5.33        |
    |    n_updates            | 40          |
    |    policy_gradient_loss | -0.00583    |
    |    value_loss           | 16.3        |
    -----------------------------------------
    Average reward with custom reward function: 537.1975036592485
    ```