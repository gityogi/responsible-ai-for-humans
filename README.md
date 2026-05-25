# CLEAR-AU Framework
### Citizen Lens for Ethical AI Review — Australia

> **"Judge your AI before it judges you."**

[![Licence: CC BY-NC 4.0](https://img.shields.io/badge/Licence-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Fairlearn](https://img.shields.io/badge/Fairlearn-0.12+-green.svg)](https://fairlearn.org)
[![AIF360](https://img.shields.io/badge/AIF360-0.6+-orange.svg)](https://aif360.mybluemix.net)

---

## What is CLEAR-AU?

AI is already making decisions about everyday Australians — in welfare assessments, loan approvals, healthcare triage, and more. Most people don't know when an algorithm is involved, whether its decision was fair, or what they can do about it.

**CLEAR-AU is a citizen-facing framework that changes that.**

It bridges the gap between technical responsible AI tools and the everyday Australians most affected by algorithmic decisions — grounded in Australian policy, demonstrated with real open-source tooling, and built for people, not engineers.

This repository contains the full technical demonstration from the accompanying white paper, including a synthetic dataset, bias detection using Microsoft Fairlearn, and bias mitigation using IBM AIF360.

---

## The CLEAR-AU Framework

CLEAR-AU operates as a **continuous three-layer cycle**:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   COMPREHEND          EVALUATE           RESPOND    │
│   the Lens    ──▶    with Account-  ──▶  with       │
│                       ability            Rights     │
│       ▲                                    │        │
│       └────────────────────────────────────┘        │
│                   (continuous cycle)                │
└─────────────────────────────────────────────────────┘
```

| Layer | Question | Tools | AU Policy |
|-------|----------|-------|-----------|
| **Comprehend the Lens** | Is an AI making decisions about me? What data is it using? | — | OAIC Privacy Guidance |
| **Evaluate with Accountability** | Is the decision fair and explainable? | Fairlearn, AIF360, PyRIT | DTA Policy, VAISS |
| **Respond with Rights** | What can I do about it under Australian law? | — | Privacy Act, OAIC, Ombudsman |

---

## Why Australia?

Australia has a unique and urgent context for responsible AI:

- **Robodebt** — 470,000+ Australians received unlawful automated debt notices. The Royal Commission (2023) found the scheme was mathematically flawed, legally invalid, and perpetuated through deliberate concealment of legal advice.
- **National AI Plan (2025)** — Australia's AI roadmap prioritises economic growth but remains light on citizen-facing enforcement mechanisms.
- **Privacy Act 1988** — OAIC has confirmed it applies to AI systems handling personal data — but most Australians don't know how to use it.

CLEAR-AU exists because institutional frameworks aren't enough. Everyday citizens need tools too.

---

## Repository Structure

```
responsible-ai-for-humans/
├── README.md                    ← You are here
├── LICENCE                      ← CC BY-NC 4.0
├── generate_dataset.py          ← Synthetic Centrelink dataset generator
├── clear_au_demo.py             ← Fairlearn + AIF360 bias analysis
└── centrelink_synthetic.csv     ← Pre-generated synthetic dataset (1,000 rows)
```

---

## Quick Start

### Requirements
```bash
python -m pip install fairlearn aif360 scikit-learn pandas numpy --only-binary :all:
```

### Step 1 — Generate the synthetic dataset
```bash
python generate_dataset.py
```

Expected output:
```
✅ Dataset generated: centrelink_synthetic.csv
   Total records: 1000

📊 Rejection rates by region:
region_type
Regional    0.613
Remote      0.680
Urban       0.432

📊 Rejection rates by age group:
age_group
18-44    0.378
45-70    0.651
```

### Step 2 — Run the CLEAR-AU bias analysis
```bash
python clear_au_demo.py
```

Expected key results:
```
Urban→Remote disparity ratio: 1.58x  ⚠️ FAIRNESS VIOLATION DETECTED
Post-mitigation disparity ratio: 1.00x  ✅ Within acceptable threshold
```

---

## What the Demo Shows

The synthetic dataset models an automated welfare eligibility system with **two deliberate bias signals** consistent with documented vulnerabilities in Australian welfare administration:

1. **Geographic bias** — Remote applicants rejected at 1.58x the rate of Urban applicants with equivalent income profiles
2. **Age bias** — Applicants aged 45+ rejected at significantly higher rates than younger cohorts

**Fairlearn** detects these disparities. **AIF360** eliminates them.

The key finding: *bias of this magnitude is not inevitable — it is remediable using freely available open-source tools.*

### Results Summary

| Metric | Pre-Mitigation | Post-Mitigation |
|--------|---------------|-----------------|
| Urban rejection rate | 34.0% | 53.7% |
| Remote rejection rate | 53.8% | 53.8% |
| **Disparity ratio** | **1.58x** ⚠️ | **1.00x** ✅ |
| Disparate impact score | 0.651 | 1.000 |

---

## Mapping to CLEAR-AU

| Layer | This Demo |
|-------|-----------|
| **Comprehend** | Automated Logistic Regression model identified as decision-maker; features: age, income, region, income source |
| **Evaluate** | Fairlearn detects 1.58x geographic disparity; AIF360 Reweighing confirms bias is fully remediable |
| **Respond** | Findings establish grounds for OAIC complaint under Privacy Act 1988, internal review request, Commonwealth Ombudsman escalation |

---

## White Paper

The full academic white paper accompanying this repository is available on Zenodo:

> **CLEAR-AU Framework: Citizen Lens for Ethical AI Review — Australia**
> DOI: *[to be updated after Zenodo upload]*

The paper covers:
- Australian policy landscape (National AI Plan, VAISS, DTA Policy, OAIC)
- Literature review of global RAI frameworks
- CLEAR-AU Framework formal definition
- Full technical demonstration with reproducible results
- Discussion, limitations, and future work

---

## Your Rights as an Australian Citizen

If you believe an AI system has made an unfair decision about you:

1. **Ask** the organisation whether an automated system was involved in the decision
2. **Request** a human review of the decision
3. **Lodge a complaint** with the [Office of the Australian Information Commissioner (OAIC)](https://www.oaic.gov.au) under the Privacy Act 1988
4. **Escalate** to the [Commonwealth Ombudsman](https://www.ombudsman.gov.au) for government agency decisions
5. **Seek legal advice** if the decision caused significant financial or personal harm

---

## Tools Used

| Tool | Purpose | Licence |
|------|---------|---------|
| [Microsoft Fairlearn](https://fairlearn.org) | Bias detection and fairness metrics | MIT |
| [IBM AIF360](https://aif360.mybluemix.net) | Bias mitigation algorithms | Apache 2.0 |
| [Microsoft PyRIT](https://github.com/microsoft/pyrit) | Generative AI risk probing | MIT |
| [scikit-learn](https://scikit-learn.org) | Logistic Regression classifier | BSD |

---

## Australian Policy References

- [National AI Plan (DISR, 2025)](https://www.industry.gov.au/ai)
- [Guidance for AI Adoption / VAISS (2025)](https://www.industry.gov.au/science-technology-and-innovation/technology/artificial-intelligence)
- [DTA Policy for Responsible AI in Government (2024)](https://www.digital.gov.au/ai/ai-in-government-policy)
- [OAIC Privacy and AI Guidance](https://www.oaic.gov.au/privacy/privacy-guidance-for-organisations-and-government-agencies/guidance-for-organisations/artificial-intelligence)
- [Royal Commission into the Robodebt Scheme (2023)](https://robodebt.royalcommission.gov.au)

---

## Licence

This work is licensed under [Creative Commons Attribution Non-Commercial 4.0 International (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to share and adapt this material for non-commercial purposes, provided you give appropriate credit to the original author.

**© 2025 Rishabh Kumar (@gityogi) | @askaimate**

---

## Author

Built by **Rishabh Kumar** — AI Engineer, ServiceNow Architect, and creator of [@askaimate](https://www.instagram.com/askaimate) — an Australian channel dedicated to making AI understandable for everyday people.

*"Most responsible AI tools are built for engineers. This one is built for everyone else."*

---

## Citation

If you use CLEAR-AU in your research or work, please cite:

```
Kumar, R. (2025). CLEAR-AU Framework: Citizen Lens for Ethical AI Review — Australia.
Zenodo. DOI: [to be updated]
```
