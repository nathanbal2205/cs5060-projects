import pandas as pd
import numpy as np

df = pd.read_csv("insurance_data.csv")

# --- Part 1: The basic insurance rate with 11 % profit margin with standard deviation and volatility ---
average_cost = df['charges'].mean()
standard_deviation = df['charges'].std()

profit_margin = 0.11
insurance_rate = average_cost * (1 + profit_margin)
coefficient_of_variation = (standard_deviation / average_cost) * 100

print(f"Insurance Rate (after 11% profit margin): ${insurance_rate:.2f}")
print(f"Standard Deviation of the Portfolio: ${standard_deviation:.2f}")
print(f"Volatility of the Portfolio (Coefficient of Variation): {coefficient_of_variation:.2f}%\n")

#  --- Part 2: Calculate the tiered insurance rate ---
age_group_costs = {
    '18-22': [],
    '23-30': [],
    '31-48': [],
    '49+': []
}

for index, row in df.iterrows():
    age = row['age']
    charges = row['charges']
    if 18 <= age <= 22:
        age_group_costs['18-22'].append(charges)
    elif 23 <= age <= 30:
        age_group_costs['23-30'].append(charges)
    elif 31 <= age <= 48:
        age_group_costs['31-48'].append(charges)
    elif age >= 49:
        age_group_costs['49+'].append(charges)

for age_range in age_group_costs:
    charge_list = age_group_costs[age_range]
    average_cost = np.mean(charge_list)
    standard_deviation = np.std(charge_list, ddof=1)

    profit_margin = 0.11
    insurance_rate = average_cost * (1 + profit_margin)
    coefficient_of_variation = (standard_deviation / average_cost) * 100

    print(f"Data for Age Group: {age_range}")
    print(f"Insurance Rate (after 11% profit margin): ${insurance_rate:.2f}")
    print(f"Standard Deviation of the Portfolio: ${standard_deviation:.2f}")
    print(f"Volatility of the Portfolio (Coefficient of Variation): {coefficient_of_variation:.2f}%\n")

# --- Part 3: Calculate the tiered insurance rate and compare sex and age ---
# Calculate insurance rates for both age and sex groups
age_sex_group_costs = {
    '18-22_male': [],
    '18-22_female': [],
    '23-30_male': [],
    '23-30_female': [],
    '31-48_male': [],
    '31-48_female': [],
    '49+_male': [],
    '49+_female': []
}

for index, row in df.iterrows():
    age = row['age']
    sex = row['sex']
    charges = row['charges']
    
    if 18 <= age <= 22:
        age_sex_group_costs[f'18-22_{sex}'].append(charges)
    elif 23 <= age <= 30:
        age_sex_group_costs[f'23-30_{sex}'].append(charges)
    elif 31 <= age <= 48:
        age_sex_group_costs[f'31-48_{sex}'].append(charges)
    elif age >= 49:
        age_sex_group_costs[f'49+_{sex}'].append(charges)

for group in age_sex_group_costs:
    charge_list = age_sex_group_costs[group]
    
    if len(charge_list) > 0:
        average_cost = np.mean(charge_list)
        standard_deviation = np.std(charge_list, ddof=1)

        profit_margin = 0.11
        insurance_rate = average_cost * (1 + profit_margin)
        coefficient_of_variation = (standard_deviation / average_cost) * 100

        print(f"Data for Age-Sex Group: {group}")
        print(f"Insurance Rate (after 11% profit margin): ${insurance_rate:.2f}")
        print(f"Standard Deviation of the Portfolio: ${standard_deviation:.2f}")
        print(f"Volatility of the Portfolio (Coefficient of Variation): {coefficient_of_variation:.2f}%\n")

# Calculate the insurance rates by sex only (ignoring age)
sex_group_costs = {
    'male': [],
    'female': []
}

for index, row in df.iterrows():
    sex = row['sex']
    charges = row['charges']
    sex_group_costs[sex].append(charges)

for sex in sex_group_costs:
    charge_list = sex_group_costs[sex]
    
    if len(charge_list) > 0: 
        average_cost = np.mean(charge_list)
        standard_deviation = np.std(charge_list, ddof=1)

        profit_margin = 0.11
        insurance_rate = average_cost * (1 + profit_margin)
        coefficient_of_variation = (standard_deviation / average_cost) * 100

        print(f"Data for Sex Group: {sex}")
        print(f"Insurance Rate (after 11% profit margin): ${insurance_rate:.2f}")
        print(f"Standard Deviation of the Portfolio: ${standard_deviation:.2f}")
        print(f"Volatility of the Portfolio (Coefficient of Variation): {coefficient_of_variation:.2f}%\n")