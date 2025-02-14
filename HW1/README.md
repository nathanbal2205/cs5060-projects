# HW1: Optimal Stopping

Author: Nathan Bal

#### Instructions

*  At the end of the Python file, you'll find five different versions of the algorithm. To run a specific version, simply uncomment the relevant code section. Each function takes three inputs: the first controls the length of the candidate list, the second manages the number of simulations, and the third remains fixed. Adjust the first two inputs as needed for your analysis.

### Part 1: Determining the General Optimum (No Look-Back Strategy)

*  The optimal stopping algorithm was tested to find the best stopping point in a uniform distribution. I ran 1,000 simulations to identify which portion of the candidate list consistently produced the optimal value. Initially, I used 100 candidates selected from a pool of 1,000. Increasing the candidate size to 200 and pool to 5,000, and running 100 iterations of 1,000 simulations, improved result consistency. The mean stopping point stabilized at around 37%. These tests align with theoretical expectations, confirming the algorithm's reliability across different candidate sizes and scenarios.

*  The optimal stopping point, based on testing, consistently occurred around 37% of the candidate list. After reviewing this portion without making a selection, the algorithm selects the next candidate who exceeds the highest value from the first 37%. This strategy ensures the best chance of selecting the optimal candidate while minimizing the risk of passing over a better option later in the list.

Here is an example of running the uniform distribution program with 100 iterations. After about 38 iterations the ideal stopping point sits around 74 or 37%.
```
The mean after 1 tests: 88
The mean after 10 tests: 78.81818181818181
The mean after 20 tests: 78
The mean after 30 tests: 76.09677419354838
The mean after 40 tests: 74.46341463414635
The mean after 50 tests: 73.3529411764706
The mean after 60 tests: 73.57377049180327
The mean after 70 tests: 74.2394366197183
The mean after 80 tests: 73.37037037037037
The mean after 90 tests: 73.13186813186813
The mean after 100 tests: 73.94

----- Total Results from 100 tests -----
Mode: 70
Mean: 73.94
Percentage for Optimally Stopping the Search: 36.97%
```

### Part 2: Exploring Alternative Distributions

*   Switching to a normal distribution introduces skewness in candidate values. Candidates are more frequently clustered around the mean (50), with fewer extreme values. This skewness alters the distribution of the highest values. After running the simulation under similar values with candidate length at 200 and running the test for 100 iterations of 1,000 simulations the mean stopping point continues to slowly rise from 69 (34.5%) starting at test 21 converging at 72 (36%) at test 70. The recalibrated stopping pointing didn't seem to effect the results significantly but effected the iterations of testing required to find out result even with the clustering of values around the mean. The results converage close to the previously discovered 37% opitmal stopping point.

Here is an example of running the normal distribution program with 100 iterations. It took signigically more iterations to come to a similar result as the uniform distrbution.
```
The mean after 1 tests: 67
The mean after 10 tests: 67.72727272727273
The mean after 20 tests: 68.61904761904762
The mean after 30 tests: 69.80645161290323
The mean after 40 tests: 70.14634146341463
The mean after 50 tests: 71.47058823529412
The mean after 60 tests: 71.49180327868852
The mean after 70 tests: 72.15492957746478
The mean after 80 tests: 72.06172839506173
The mean after 90 tests: 72.43956043956044
The mean after 100 tests: 73.34

----- Total Results from 100 tests -----
Mode: 69
Mean: 73.34
Percentage for Optimally Stopping the Search: 36.67%
```

*    Switching to a Beta(2,7) distribution introduces a significant skew in candidate values. This distribution is right-skewed, meaning that most values cluster towards the lower end of the range, with fewer high values. This skewness affects the distribution of the highest values, leading to changes in the optimal stopping strategy. After running the simulation under similar values with candidate length at 200 and running the test for 100 iterations of 1,000 simulations the results seemed to quickly converage on about 72 (36%). This result is also not that far from the orginal optimal stop of 37% and the result was found with a lot fewer iterations.

Here is an example of running the beta(2,7) distribution program with 100 iterations. It took signigically less iterations to come to a similar result as the uniform distrbution.
```
The mean after 1 beta tests: 79
The mean after 10 beta tests: 71.54545454545455
The mean after 20 beta tests: 72.71428571428571
The mean after 30 beta tests: 73.12903225806451
The mean after 40 beta tests: 72.46341463414635
The mean after 50 beta tests: 72
The mean after 60 beta tests: 72.1639344262295
The mean after 70 beta tests: 71.33802816901408
The mean after 80 beta tests: 71.39506172839506
The mean after 90 beta tests: 72.10989010989012

----- Total Results from 100 tests -----
Mode: 72
Mean: 71.8
Percentage for Optimally Stopping the Search: 35.9%
```

### Part 3: Maximizing Benefit in Investment Decisions

*   The optimal stopping strategy is now modified to account for evaluation costs, where each additional evaluation reduces the final reward by one point. This adjustment shifts the focus from simply selecting the highest number to balancing the trade-off between the number of evaluations and the potential reward. As a result, determining the most optimal stopping point becomes a matter of maximizing net gains rather than just identifying the highest value.

*   We begin by applying the algorithm to a uniform distribution of values ranging from 1 to 99, assessing how this distribution influences the optimal stopping point and the overall outcomes. After thoroughly testing the algorithm, we observed a significant reduction in the optimal stopping point compared to the traditional problem. This result aligns with expectations, as candidates appearing early often yield a higher net gain due to lower evaluation costs, making it advantageous to stop sooner. From the results, we can see a noticeable sharp increase in net gain around an evaluation point of 4.27, followed by a rapid decline. This indicates that the optimal stopping point becomes much more defined compared to the original problem, where the lack of evaluation costs allowed for more flexibility in waiting for higher values. The introduction of costs creates a clearer trade-off, emphasizing the importance of stopping earlier when a strong candidate is encountered.

Here is an example of running the uniform distribution program with 100,000 iterations.
```
The mean after 0 invest tests: 2
The mean after 10000 invest tests: 4.268473152684732
The mean after 20000 invest tests: 4.2780360981950905
The mean after 30000 invest tests: 4.280223992533582
The mean after 40000 invest tests: 4.2707182320441985
The mean after 50000 invest tests: 4.277654446911062
The mean after 60000 invest tests: 4.284728587856869
The mean after 70000 invest tests: 4.28281024556792
The mean after 80000 invest tests: 4.279084011449857
The mean after 90000 invest tests: 4.272963633737403

----- Total Results from 100000 tests -----
Mean: 4.27084
Percentage for Optimally Stopping the Search: 4.27%
```

*   Similar to the transition from a uniform to a normal distribution in the classic optimal stopping problem, using a normal distribution for the candidate list initially leads to a higher mean stopping point. However, as testing progresses, the mean converges more quickly, settling at around 4.43. This value is slightly higher than seen with a uniform distribution but remains relatively close. This behavior demonstrates that while the normal distribution affects the stopping strategy differently at first, it ultimately aligns with the patterns observed under a uniform distribution.

Here is an example of running the normal distribution program with 100,000 iterations.
```
The mean after 10000 invest tests: 4.4273
The mean after 20000 invest tests: 4.43605
The mean after 30000 invest tests: 4.4135
The mean after 40000 invest tests: 4.419975
The mean after 50000 invest tests: 4.41986
The mean after 60000 invest tests: 4.41175
The mean after 70000 invest tests: 4.412671428571429
The mean after 80000 invest tests: 4.4265625
The mean after 90000 invest tests: 4.430188888888889

----- Total Results from 100000 tests -----
Median: 3
Mean: 4.431844318443185
Percentage for Optimally Stopping the Search: 4.43%
```