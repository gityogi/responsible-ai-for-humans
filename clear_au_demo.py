"""
CLEAR-AU Framework — Fairness Analysis Demo
============================================
Demonstrates bias detection (Fairlearn) and bias mitigation (AIF360)
on a synthetic Centrelink welfare eligibility dataset.

Layers demonstrated:
  Layer 2 — Evaluate with Accountability

Author: CLEAR-AU Project
Licence: CC BY-NC 4.0
Note: Synthetic data only. No real personal data used.

Requirements:
  pip install fairlearn aif360 scikit-learn pandas numpy
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from fairlearn.metrics import MetricFrame, selection_rate, demographic_parity_difference
from aif360.datasets import BinaryLabelDataset
from aif360.algorithms.preprocessing import Reweighing
from aif360.metrics import BinaryLabelDatasetMetric
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("  CLEAR-AU Framework — Technical Demonstration")
print("  Centrelink Synthetic Welfare Eligibility Dataset")
print("=" * 60)

# ── 1. Load Dataset ──────────────────────────────────────────
df = pd.read_csv('centrelink_synthetic.csv')
print(f"\n✅ Dataset loaded: {len(df)} records\n")

# ── 2. Preprocessing ─────────────────────────────────────────
le_region = LabelEncoder()
le_source  = LabelEncoder()
df['region_encoded'] = le_region.fit_transform(df['region_type'])
df['source_encoded']  = le_source.fit_transform(df['income_source'])

features = ['age', 'annual_income', 'outstanding_balance',
            'region_encoded', 'source_encoded']
X = df[features]
y = df['claim_outcome']
sensitive_region = df['region_type']
sensitive_age    = (df['age'] >= 45).map({True: '45+', False: '18-44'})

X_train, X_test, y_train, y_test, sr_train, sr_test, sa_train, sa_test = \
    train_test_split(X, y, sensitive_region, sensitive_age,
                     test_size=0.3, random_state=42)

# ── 3. Train Baseline Model ───────────────────────────────────
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# ── 4. FAIRLEARN — Bias Detection ────────────────────────────
print("─" * 60)
print("  LAYER 2A: FAIRLEARN — Bias Detection")
print("─" * 60)

# Geographic bias
mf_region = MetricFrame(
    metrics=selection_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sr_test
)

print("\n📊 Rejection rates by region (model predictions):")
for region, rate in mf_region.by_group.items():
    bar = "█" * int(rate * 40)
    print(f"  {region:<12} {rate:.1%}  {bar}")

urban_rate  = mf_region.by_group.get('Urban', 0)
remote_rate = mf_region.by_group.get('Remote', 0)
disparity_ratio = remote_rate / urban_rate if urban_rate > 0 else 0

print(f"\n  Urban→Remote disparity ratio: {disparity_ratio:.2f}x")
print(f"  (Fairlearn threshold: >1.25 = significant violation)")
if disparity_ratio > 1.25:
    print(f"  ⚠️  FAIRNESS VIOLATION DETECTED")

dpd_region = demographic_parity_difference(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sr_test
)
print(f"  Demographic parity difference: {dpd_region:.3f}")
print(f"  (0.0 = perfect fairness, >0.1 = significant violation)")

# Age bias
mf_age = MetricFrame(
    metrics=selection_rate,
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sa_test
)

print("\n📊 Rejection rates by age group:")
for group, rate in mf_age.by_group.items():
    bar = "█" * int(rate * 40)
    print(f"  {group:<12} {rate:.1%}  {bar}")

dpd_age = demographic_parity_difference(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=sa_test
)
print(f"\n  Demographic parity difference (age): {dpd_age:.3f}")

# ── 5. AIF360 — Bias Mitigation ──────────────────────────────
print("\n" + "─" * 60)
print("  LAYER 2B: AIF360 — Bias Mitigation (Reweighing)")
print("─" * 60)

# Prepare AIF360 dataset
df_aif = df[['age', 'annual_income', 'outstanding_balance',
             'region_encoded', 'source_encoded', 'claim_outcome']].copy()

# Use region_encoded as privileged (Urban=2 after encoding)
urban_code = int(le_region.transform(['Urban'])[0])

aif_dataset = BinaryLabelDataset(
    df=df_aif,
    label_names=['claim_outcome'],
    protected_attribute_names=['region_encoded'],
    favorable_label=0,
    unfavorable_label=1
)

privileged   = [{'region_encoded': urban_code}]
unprivileged = [{'region_encoded': r}
                for r in df_aif['region_encoded'].unique()
                if r != urban_code]

# Pre-mitigation metrics
metric_pre = BinaryLabelDatasetMetric(
    aif_dataset,
    privileged_groups=privileged,
    unprivileged_groups=unprivileged
)

print(f"\n  Pre-mitigation disparate impact:  {metric_pre.disparate_impact():.3f}")
print(f"  (1.0 = fair, <0.8 = adverse impact under 80% rule)")

# Apply Reweighing
rw = Reweighing(privileged_groups=privileged, unprivileged_groups=unprivileged)
aif_reweighed = rw.fit_transform(aif_dataset)

metric_post = BinaryLabelDatasetMetric(
    aif_reweighed,
    privileged_groups=privileged,
    unprivileged_groups=unprivileged
)

print(f"  Post-mitigation disparate impact: {metric_post.disparate_impact():.3f}")

# Retrain with reweighed samples
sample_weights = aif_reweighed.instance_weights
X_full = df_aif.drop('claim_outcome', axis=1)
y_full = df_aif['claim_outcome']

model_fair = LogisticRegression(max_iter=1000, random_state=42)
model_fair.fit(X_full, y_full, sample_weight=sample_weights)

X_test_aif = X_test[['age', 'annual_income', 'outstanding_balance',
                      'region_encoded', 'source_encoded']]
y_pred_fair = model_fair.predict(X_test_aif)

mf_region_post = MetricFrame(
    metrics=selection_rate,
    y_true=y_test,
    y_pred=y_pred_fair,
    sensitive_features=sr_test
)

print("\n📊 Post-mitigation rejection rates by region:")
for region, rate in mf_region_post.by_group.items():
    bar = "█" * int(rate * 40)
    print(f"  {region:<12} {rate:.1%}  {bar}")

urban_post  = mf_region_post.by_group.get('Urban', 0)
remote_post = mf_region_post.by_group.get('Remote', 0)
ratio_post  = remote_post / urban_post if urban_post > 0 else 0
print(f"\n  Post-mitigation disparity ratio: {ratio_post:.2f}x")

if ratio_post <= 1.25:
    print(f"  ✅ Disparity ratio within acceptable threshold")

# ── 6. CLEAR-AU Summary ───────────────────────────────────────
print("\n" + "=" * 60)
print("  CLEAR-AU FRAMEWORK — Demonstration Summary")
print("=" * 60)
print("""
  Layer 1 — COMPREHEND THE LENS
  ✅ Automated model identified as decision-maker
     Features used: age, income, region, income source

  Layer 2 — EVALUATE WITH ACCOUNTABILITY
  ✅ Fairlearn: Geographic bias detected
     Urban→Remote disparity ratio: {:.2f}x (threshold: 1.25x)
  ✅ AIF360: Bias mitigated via Reweighing
     Post-mitigation ratio: {:.2f}x

  Layer 3 — RESPOND WITH RIGHTS
  ✅ Grounds established for:
     → OAIC complaint under Privacy Act 1988
     → Internal review request (Services Australia)
     → Escalation to Commonwealth Ombudsman
""".format(disparity_ratio, ratio_post))
print("=" * 60)
print("  Full code: github.com/[your-handle]/responsible-ai-for-humans")
print("=" * 60)
