"""
CLEAR-AU Framework — Synthetic Dataset Generator
=================================================
Generates a synthetic Centrelink welfare eligibility dataset
with deliberate geographic and age-based bias for demonstration purposes.

Author: CLEAR-AU Project
Licence: CC BY-NC 4.0
Note: This dataset is entirely synthetic. No real personal data was used.
"""

import pandas as pd
import numpy as np

# Reproducibility
np.random.seed(42)
n = 1000

# --- Base Features ---
region_type = np.random.choice(
    ['Urban', 'Regional', 'Remote'],
    n, p=[0.60, 0.30, 0.10]
)

age = np.random.randint(18, 70, n)

annual_income = np.random.normal(45000, 15000, n).clip(10000, 120000)

income_source = np.random.choice(
    ['Employment', 'Casual', 'Centrelink'],
    n, p=[0.50, 0.30, 0.20]
)

outstanding_balance = np.random.exponential(2000, n).clip(0, 20000)

# Generate realistic postcodes by region
def generate_postcode(region):
    if region == 'Urban':
        return np.random.choice(['2000', '3000', '4000', '5000', '6000'])
    elif region == 'Regional':
        return np.random.choice(['2640', '3500', '4700', '5700', '6700'])
    else:
        return np.random.choice(['0872', '4825', '6442', '5440', '4380'])

postcode = [generate_postcode(r) for r in region_type]

# --- Introduce Deliberate Bias ---
# Geographic bias: Remote +35%, Regional +15%
# Age bias: 45+ applicants +25%
base_rejection = 0.30

rejection_prob = np.where(region_type == 'Remote',  base_rejection + 0.35,
                 np.where(region_type == 'Regional', base_rejection + 0.15,
                 base_rejection))

rejection_prob = np.where(age >= 45,
                 rejection_prob + 0.25,
                 rejection_prob).clip(0, 1)

claim_outcome = np.random.binomial(1, rejection_prob)

# --- Build DataFrame ---
df = pd.DataFrame({
    'applicant_id':       [f'AU{str(i).zfill(5)}' for i in range(n)],
    'age':                age,
    'postcode':           postcode,
    'region_type':        region_type,
    'annual_income':      annual_income.round(2),
    'income_source':      income_source,
    'outstanding_balance': outstanding_balance.round(2),
    'claim_outcome':      claim_outcome  # 1 = Rejected, 0 = Approved
})

# --- Save ---
df.to_csv('centrelink_synthetic.csv', index=False)
print("✅ Dataset generated: centrelink_synthetic.csv")
print(f"   Total records: {len(df)}")
print(f"\n📊 Rejection rates by region:")
print(df.groupby('region_type')['claim_outcome'].mean().round(3).to_string())
print(f"\n📊 Rejection rates by age group:")
df['age_group'] = pd.cut(df['age'], bins=[17, 44, 70], labels=['18-44', '45-70'])
print(df.groupby('age_group', observed=True)['claim_outcome'].mean().round(3).to_string())
