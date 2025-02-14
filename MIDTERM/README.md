# CS 5060 Midterm Exam

### By: Nathan Bal

## Question 1: Algorithm Pseudocode
### Optimal Stopping Problem

**Input:**
*   len_candidates: Number of candidates (integer).
*   num_simulations: Number of simulations to run (integer).

**Output:**
*   The probability of success at that stopping position.

**Pseudocode:**
```
function run_experiment(len_candidates, num_simulations):
    Initialize an empty list to store the results of each simulation

    Step 1: Calculate the stopping threshold (observation phase) as:
        stop_position = int(len_candidates * 0.37)
        // This means we observe the first 37% of candidates without selecting

    for each simulation in num_simulations:
        Step 2: Generate a list of 'len_candidates' random candidates using a uniform distribution
        Step 3: Identify the 'optimal_candidate' as the maximum value in the candidate list

        Step 4: Implement the optimal stopping rule:
            - First, observe the first stop position candidates but do not select any
            - After the observation phase, select the first candidate that is better than all previously observed candidates
            - If this candidate is the optimal candidate, record a successful stop in success results

        Step 5: Record whether the optimal candidate was selected after stopping

    Step 6: After all simulations, calculate and print:
        - The probability of success (i.e., how often the optimal candidate was selected) as:
            success_probability = (sum of success_results) / num_simulations * 100
        - Print the optimal stopping success probability

end function
```

### Multi-Armed Bandit Problem

**Input:**
*   epsilon: The probability of exploring (a float between 0 and 1).
*   n_steps: Total number of steps to perform (an integer).
*   n_actions: Number of available actions (an integer, representing different bandits).

**Output:**
*   average_rewards: A list containing the average cumulative reward at each step.

**Pseudocode:**
```
function run_epsilon_greedy(epsilon, n_steps, n_actions):
    
    Step 1: Initialize Q-values for each action to zero
        Q_values = array of zeros with size n_actions
        // These Q-values represent the estimated reward for each action

    Step 2: Initialize a count array N to track the number of times each action has been selected
        N = array of zeros with size n_actions

    Step 3: Initialize a list to store the average cumulative rewards after each step
        average_rewards = [0] // Start with an initial reward of 0
        total_reward = 0

    for each step in range from 0 to n_steps - 1:
        Step 4: Decide whether to explore or exploit:
            If a random number is greater than epsilon (exploit):
                Select the action with the highest Q-value (greedy action)
            Else (explore):
                Select a random action uniformly from all actions

        Step 5: Receive a reward for the selected action:
            reward = get_reward_for_action(action)
            // Assume a function get_reward_for_action(action) that returns the reward for the selected action

        Step 6: Update Q-values using the reward from the selected action:
            Increment the count N[action] for the chosen action
            Update the Q_value for the chosen action using the formula:
                Q_value[action] = Q_value[action] + (1/N[action]) * (reward - Q_value[action])
                // this formula ensures that the Q-value reflects the running average of      rewards for the action, becoming more accurate over time as more data (rewards) are collected.

        Step 7: Update total reward:
            total_reward = total_reward + reward

        Step 8: Calculate the new average reward and append it to the list:
            average_rewards.append(total_reward / (step + 1))

    Step 9: After all steps are completed, return the list of average rewards:
        return average_rewards

end function
```

### Option Valuation

**Input:**
*   initial_price: The starting price of the underlying asset (a float).
*   strike_price: The strike price of the option (a float).
*   drift: The expected return rate (a float, often the risk-free interest rate).
*   volatility: The standard deviation of returns, indicating how much the price can vary (a float).
*   dt: The time step for each simulation (a small float, e.g., 0.01).
*   T: The time to maturity of the option (a float, e.g., 1 year).
*   paths: The number of simulated price paths (an integer, e.g., 10,000).
*   risk_free_rate: The risk-free rate for discounting the payoff (a float, e.g., 0.05).

**Output:**
*   option_value: The estimated value of the option (a float).

**Pseudocode:**
```
function calculate_option_value(initial_price, strike_price, drift, volatility, dt, T, paths, risk_free_rate):

    Step 1: Initialize an empty list to store price paths
        price_paths = []

    Step 2: Generate multiple stock price paths using Brownian motion
        for each path in range from 0 to paths - 1:
            current_price = initial_price   // Set the initial stock price
            total_time = T                  // Time to maturity
            prices = []                     // List to store simulated prices for this path

            while total_time > 0:
                Step 2.1: Generate a random price movement using Brownian motion:
                    dWt = random_normal(0, sqrt(dt))  // Generate a random number from standard normal distribution
                    dYt = drift * dt + volatility * dWt  // Calculate the price change based on drift and volatility

                Step 2.2: Update the stock price:
                    current_price = current_price + dYt  // Adjust the stock price by the price change
                    prices.append(current_price)         // Store the updated price

                Step 2.3: Update time:
                    total_time = total_time - dt  // Decrease remaining time by the time step

            Step 2.4: Store the generated price path:
                price_paths.append(prices)

    Step 3: Calculate the payoff for each path
        call_payoffs = []  // List to store the payoffs for each path
        ec = European_Call_Payoff(strike_price)  // Create a European call option with the given strike price

        for each price_path in price_paths:
            Step 3.1: Get the final stock price at maturity:
                final_price = price_path[-1]  // The last price in the price path

            Step 3.2: Calculate the option payoff at maturity:
                payoff = ec.get_payoff(final_price)  // Payoff for the European call option
                // The payoff for a European call option represents the amount an investor would receive if they exercised the option at expiration. It is calculated as the maximum of zero or the difference between the final stock price and the strike price.

            Step 3.3: Discount the payoff to present value:
                discounted_payoff = payoff / (1 + risk_free_rate)  // Apply discount factor using the risk-free rate
                // The payoff at maturity represents the amount you would receive if you exercised the option. To find its value today, we discount it back to the present using the risk-free rate. This means we are accounting for the time value of money, as receiving money now is worth more than receiving the same amount in the future.

            Step 3.4: Store the discounted payoff:
                call_payoffs.append(discounted_payoff)

    Step 4: Calculate the average discounted payoff (option value)
        option_value = average(call_payoffs)  // The average of all the discounted payoffs

    Step 5: Return the calculated option value
        return option_value

end function
```

### Insurance Algorithm

**Input:**
*   customer_pool_sizes: List of different customer pool sizes to test
*   claim_probability: Probability that a customer will file a claim
*   claim_severity: Distribution of claim amounts like normal or exponential functions to generate the claim amount for each customer.
*   administrative_costs: Fixed costs for managing the insurance policy per customer
*   base_risk_margin: The base profit margin for covering risks
*   simulation_runs: Number of simulations to run for calculating expected costs

**Output:**
*   Graph showing the relationship between customer pool size and the average premium.

**Pseudocode:**
```
function calculate_insurance_premium_with_graph(claim_probability, claim_severity, administrative_costs, base_risk_margin, simulation_runs, customer_pool_sizes):

    Step 1: Initialize an empty list to store average premiums for each pool size
        premiums = []

    Step 2: Loop through each customer pool size
        for each num_customers in customer_pool_sizes:
        
            Step 3: Initialize a variable to store the total expected cost for this pool size
                total_expected_cost = 0

            Step 4: Run multiple simulations to model the expected payouts for this pool size
                for each simulation in range from 0 to simulation_runs - 1:
                    simulated_cost = 0  // Initialize the simulated cost for this run

                    for each customer in range from 0 to num_customers - 1:
                        Step 4.1: Determine if the customer files a claim using the claim probability
                            random_value = random_uniform(0, 1)  // Generate a random number between 0 and 1
                            if random_value < claim_probability:  // Customer files a claim
                                Step 4.2: Calculate the severity of the claim
                                    claim_amount = claim_severity()  // Generate claim amount based on the distribution

                                Step 4.3: Add the claim amount to the simulated cost
                                    simulated_cost += claim_amount

                        Step 4.4: Add administrative costs for each customer
                            simulated_cost += administrative_costs * num_customers  // Add fixed costs for all customers

                        Step 4.5: Add the simulated cost to the total expected cost
                            total_expected_cost += simulated_cost

            Step 5: Calculate the average expected cost per customer
                average_expected_cost = total_expected_cost / (simulation_runs * num_customers)

            Step 6: Adjust the risk margin based on the number of customers:
                risk_margin = base_risk_margin / sqrt(num_customers)
                // The risk margin decreases as the number of customers increases
                // This reflects the reduced risk for larger pools.

            Step 7: Calculate the premium for this customer pool size by adding the risk margin to the average cost
                premium = average_expected_cost * (1 + risk_margin)

            Step 8: Append the calculated premium to the premiums list
                premiums.append(premium)

    Step 9: Plot the graph of customer pool sizes vs. average premium
        x_values = customer_pool_sizes  // X-axis: Pool sizes
        y_values = premiums  // Y-axis: Corresponding premiums

        plot(x_values, y_values)  // Plot the graph showing how premium changes with pool size
        label_x_axis("Number of Customers")  // Label the x-axis
        label_y_axis("Average Premium per Customer")  // Label the y-axis
        title("Premium vs. Customer Pool Size")  // Title of the graph

end function
```

## Question 2 Impact of Randomness on Algorithms:
### Optimal Stopping Problem
When testing the Optimal Stopping algorithm with different random distributions (uniform, normal, and beta), the distribution had only a minor impact on the optimal stopping point, which still hovered around 37% after enough trials. For the normal distribution, the mean stopping point rose slightly but eventually converged to the optimal stopping point. With the beta distribution (skewed), convergence occurred more quickly, although early trials were skewed. While the initial data can be affected by the shape of the distribution and the randomness, over time the average stopping point stabilizes near 37%.

In the case of a bimodal distribution (as shown in Figure 1), where one peak is much larger than the other, the algorithm may struggle in early trials, as it could falsely treat the larger peak as the "optimal" range. This could lead to more variance in early decisions, but as with other distributions, the stopping point would likely still converge over time as more data is observed. The shape of the distribution can impact the speed of convergence but not the final result. Over the long term, the randomness of different distributions does not significantly alter the final outcome, as the algorithm adjusts and balances between both peaks with sufficient data.

### Multi-Armed Bandit Problem
When using the Multi-Armed Bandit algorithm with different random distributions (uniform, normal, and beta), the decision-making process and the exploration-exploitation balance need to be adjusted based on the distribution of rewards. For a uniform distribution, where all rewards have an equal probability, the exploration-exploitation balance can remain more neutral since each arm offers a similar chance of any reward within the range. For normal distributions, rewards are more likely to cluster around the mean, so the algorithm may need to increase exploration to ensure arms with potentially higher rewards (in the tails) are discovered. In the case of beta distributions with skew, the exploration-exploitation strategy needs to account for the skew; if the distribution skews toward low rewards, the algorithm may need to decrease exploration and exploit more quickly, whereas a skew toward higher rewards could justify more exploration to avoid missing better arms.

For a bimodal distribution (as in Figure 1), where one peak is much larger than the other, the algorithm might initially exploit the larger peak. To better balance this, more exploration might be necessary to prevent over-exploitation of suboptimal arms and to discover potential higher rewards in the smaller peak. Adjusting the exploration-exploitation trade-off for such complex distributions is key to efficiently identifying the optimal arm. The randomness inherent in different distributions can be predicted with sufficient data, allowing for a more refined understanding of the distribution's structure and improving the algorithm's performance over time.

### Option Valuation
The randomness in the Option Valuation algorithm significantly impacts the simulated price paths generated by different random distributions (uniform, normal, and beta). Using a uniform distribution results in a wider spread of potential price paths, as increments are more evenly distributed across the entire range of possible values, allowing for greater variability over time. The normal distribution, particularly when modeling with Brownian motion, creates paths that generally vary around the initial price, with most paths remaining close to it while a few diverge significantly. This clustering behavior in the normal distribution can limit the extremes of price movements. In a beta distribution, values are strictly bounded between 0 and 1. When using this distribution for price estimation, the generated increments will always be non-negative. The price estimate will consistently increase, as there are no negative random values to allow for potential decreases in the price paths.

A distribution that leans more toward positive values will result in simulated paths that consistently increase, while one skewed toward negative values could cause paths to decline more frequently. In the case of a bimodal distribution (as shown in Figure 1), where one peak is significantly taller than the other, the algorithm's behavior may be affected by the way price paths gravitate toward the dominant peak. If the larger hump were on the negative side and the smaller hump on the positive side, the algorithm could face a higher likelihood of generating paths that lead to losses, potentially underestimating risk and leading to poor investment decisions. In such scenarios, the algorithm might become overly reliant on the smaller positive peak, thereby ignoring the greater risk represented by the larger negative peak, further complicating the valuation process and emphasizing the importance of understanding the distribution’s shape and location in predicting price movements. randomness in these distributions can significantly affect short-term outcomes, but the long-term behavior of the algorithm remains predictable once the distribution's nature is fully recognized and accounted for.

### Insurance Algorithm
The performance of the Insurance Algorithm is significantly influenced by randomness, which manifests through different random distributions (uniform, normal, and beta with skew). When using a uniform distribution, each customer has an equal probability of filing a claim, leading to more predictable costs across simulations. This uniformity results in relatively stable premiums as the pool size increases. In contrast, a normal distribution creates variability in claim amounts that tends to cluster around the mean, which can lead to larger payouts than expected in certain simulations, thereby inflating premiums. With a beta distribution that is skewed, the likelihood of severe claims can vary greatly; if skewed toward higher severities, it could lead to unexpectedly high costs, necessitating higher premiums to cover the increased risk.

In the case of a bimodal distribution (as shown in Figure 1), where one peak is significantly taller than the other, the algorithm's performance may be further complicated. If the larger peak represents higher claim amounts, the algorithm could underestimate potential payouts, leading to inadequate premium pricing. Conversely, if the larger peak is associated with lower claims, the algorithm may overestimate the average cost, potentially setting premiums too high. The bimodal nature introduces uncertainty in predicting customer behavior and the associated financial risk, emphasizing the importance of understanding the shape and location of the distribution. This awareness allows insurers to adjust their risk assessments and premium calculations accordingly, ensuring they remain competitive while covering potential claims.

## Question 3: Nature of the Algorithms:
### Topology in the Optimal Stop Algorithm: 
In the Optimal Stop Algorithm, the state-space or decision topology evolves as a sequence of possible states, where each state represents a decision point over time. As decisions are made, they influence the transitions to future states, creating a dynamic system that reflects the impact of past choices. The topology represents a set of possible paths and as the system progresses, fewer options may remain available. The key challenge is identifying when continuing yields diminishing returns, making it optimal to stop. This evolving structure helps navigate the decision-making process by balancing the potential rewards of stopping versus continuing.

### Explore/Exploit Trade-offs in Multi-Armed Bandits:
Different strategies manage the explore/exploit trade-off in distinct ways. The epsilon-greedy method randomly explores by choosing a non-optimal action with probability epsilon while exploiting the current best option the rest of the time. It balances exploration and exploitation by adjusting epsilon, typically decreasing it over time. Thompson sampling maintains a probability distribution over its potential rewards, which reflects both the observed outcomes and the uncertainty about those outcomes. In each step, it samples a reward estimate from the posterior distribution of each action, then selects the action with the highest sampled reward. This probabilistic approach naturally encourages exploration when uncertainty is high, as actions with less observed data and therefore wider, less certain distributions are more likely to be sampled. As more data is collected, the distributions become narrower and more precise, leading to more exploitation of the best-performing action. Thus, while epsilon-greedy relies on a simple, tunable parameter, Thompson sampling adapts more flexibly to different conditions.

### Option Valuation Model:
In an option valuation model, several key assumptions drift, volatility, time to expiration, and risk-free rate significantly affect the option's value. Higher volatility can lead to a greater predicted option price, as it increases the likelihood of significant movements in the underlying asset's price, whether upwards or downwards. Similarly, a longer time to expiration alters the option's value by providing more opportunities for price fluctuations, potentially resulting in a larger deviation from the actual price. While the drift, or expected return, has a lesser impact on pricing, it can still influence the direction of price movements. Additionally, an increase in the risk-free rate tends to raise the value of call options while lowering the value of put options. Under extreme assumptions such as very high volatility or prolonged time to expiration the option's value can become disproportionately large. Conversely, extreme risk-free rates or unrealistic drift assumptions may distort the model's accuracy.

### Effective Insurance Product Design:
Effective insurance product design requires careful consideration of various factors, including risk assessment, customer demographics, and claim probabilities. A thorough understanding of uncertainty and risk modeling is important, as it informs how insurers evaluate potential payouts and set appropriate premiums. When uncertainty and risk are high, pricing must be higher to account for the increased likelihood that predictions may be wrong, thereby ensuring that the insurer remains financially viable. By employing probabilistic risk models, insurers can estimate the likelihood and severity of claims more accurately, allowing them to price their products competitively while ensuring financial sustainability. Analyze historical claims, customer behavior, and market trends can lead to more tailored products that meet specific customer needs. A well-designed insurance product balances adequate coverage and affordability while effectively managing the inherent uncertainties associated with insuring against potential risks.

## Question 4: Insurance Value of Subdivision
### PART 1:
The basic insurance rate for this population, considering zero deductible policies and an 11% profit margin, is $1,970.90. The standard deviation of the portfolio is $6,326.25, indicating very high volatility and significant risk associated with the variability of insurance claims. The coefficient of variation (CV), calculated as the ratio of the standard deviation to the mean, is approximately 356.29%, further highlighting that the claims are extremely volatile relative to the average claim amount. Here is the output:
```
Insurance Rate (after 11% profit margin): $1970.90
Standard Deviation of the Portfolio: $6326.25
Volatility of the Portfolio (Coefficient of Variation): 356.29%
```

### PART 2:
The results show tiered insurance rates for the population, broken down by age groups, with an 11% profit margin. Each age group has its own corresponding insurance rate, standard deviation, and volatility, reflecting the variability of claims within that group. Younger groups have lower rates and higer volatility, while older groups exhibit higher rates and lower variability in claims. The standard deviations and coefficient of variation provide insight into the level of risk and claim variability associated with each age group. Here is the output:
```
Data for Age Group: 18-22
Insurance Rate (after 11% profit margin): $1250.77
Standard Deviation of the Portfolio: $5085.02
Volatility of the Portfolio (Coefficient of Variation): 451.27%

Data for Age Group: 23-30
Insurance Rate (after 11% profit margin): $1543.10
Standard Deviation of the Portfolio: $5501.75
Volatility of the Portfolio (Coefficient of Variation): 395.76%

Data for Age Group: 31-48
Insurance Rate (after 11% profit margin): $1963.76
Standard Deviation of the Portfolio: $6271.64
Volatility of the Portfolio (Coefficient of Variation): 354.50%

Data for Age Group: 49+
Insurance Rate (after 11% profit margin): $2591.06
Standard Deviation of the Portfolio: $7279.25
Volatility of the Portfolio (Coefficient of Variation): 311.84%
```

### PART 3:
The results provide a comparison of insurance rates, standard deviations, and volatility across different age and sex groups. Each section displays the insurance rate with an 11% profit margin, along with the associated standard deviation and volatility for that particular group. The data is broken down by age-sex combinations (e.g., 18-22 males, 31-48 females) and by sex alone (male, female). This allows for an examination of how both age and sex impact the overall insurance costs and variability in the portfolio. Here is the output:
```
Data for Age-Sex Group: 18-22_male
Insurance Rate (after 11% profit margin): $1431.71
Standard Deviation of the Portfolio: $5692.36
Volatility of the Portfolio (Coefficient of Variation): 441.33%

Data for Age-Sex Group: 18-22_female
Insurance Rate (after 11% profit margin): $1072.87
Standard Deviation of the Portfolio: $4404.70
Volatility of the Portfolio (Coefficient of Variation): 455.71%

Data for Age-Sex Group: 23-30_male
Insurance Rate (after 11% profit margin): $1635.86
Standard Deviation of the Portfolio: $5984.67
Volatility of the Portfolio (Coefficient of Variation): 406.08%

Data for Age-Sex Group: 23-30_female
Insurance Rate (after 11% profit margin): $1443.16
Standard Deviation of the Portfolio: $4930.98
Volatility of the Portfolio (Coefficient of Variation): 379.26%

Data for Age-Sex Group: 31-48_male
Insurance Rate (after 11% profit margin): $2085.39
Standard Deviation of the Portfolio: $6592.38
Volatility of the Portfolio (Coefficient of Variation): 350.90%

Data for Age-Sex Group: 31-48_female
Insurance Rate (after 11% profit margin): $1841.52
Standard Deviation of the Portfolio: $5931.64
Volatility of the Portfolio (Coefficient of Variation): 357.54%

Data for Age-Sex Group: 49+_male
Insurance Rate (after 11% profit margin): $2639.35
Standard Deviation of the Portfolio: $7633.29
Volatility of the Portfolio (Coefficient of Variation): 321.02%

Data for Age-Sex Group: 49+_female
Insurance Rate (after 11% profit margin): $2541.61
Standard Deviation of the Portfolio: $6900.09
Volatility of the Portfolio (Coefficient of Variation): 301.35%

Data for Sex Group: male
Insurance Rate (after 11% profit margin): $2075.01
Standard Deviation of the Portfolio: $6716.15
Volatility of the Portfolio (Coefficient of Variation): 359.27%

Data for Sex Group: female
Insurance Rate (after 11% profit margin): $1864.80
Standard Deviation of the Portfolio: $5901.66
Volatility of the Portfolio (Coefficient of Variation): 351.29%
```

### PART 4:
The risk for the portfolio changes significantly when breaking the insurance product into smaller groups, such as age or sex categories. By subdividing the population, the coefficient of variation provides deeper insight beyond the standard deviation. While the standard deviation measures the absolute risk within each group, the CV reveals the relative volatility of each group by comparing the standard deviation to the average cost. This reflects how breaking the population into subgroups provides a better understanding of relative risk, with younger groups displaying much higher volatility compared to their average cost.

Subdividing the insurance product into groups based on age and sex offers significant benefits. It allows for more precise risk assessment and pricing by reflecting the specific volatility of claims within each demographic. For example, younger individuals have lower average rates but higher relative volatility, suggesting their claims are less predictable. Older individuals, while having higher claim rates and standard deviations, show a lower CV, indicating their claims are relatively more predictable compared to the mean. By understanding the CV, insurers can manage risk more effectively and charge rates that are competitive yet reflect the true volatility and risk associated with each demographic.

If the insurer could accurately predict who will make claims and who will not, the insurance pricing could be further tailored. In this scenario, the annual insurance rate for claimants would increase significantly to reflect their expected higher costs. Non-claimants, on the other hand, would likely see much lower rates. For claimants, the rate would approach their expected expenses plus the 11% profit margin. This would significantly reduce risk for the insurer, as the variability in claims would be reduced by more accurately pricing policies based on expected claims rather than averaging risk across all policyholders.

The annual rate for known claimants would rise considerably compared to the average rate for the overall population. Since claimants generate higher costs, their rates would need to cover these expected claims plus the profit margin. This increase would be substantial due to the more precise assessment of their higher-risk profile. Volatile and unpredictable claims within specific groups would prompt the insurer to price policies more accurately, ensuring that risk is properly mitigated in high variance cases.