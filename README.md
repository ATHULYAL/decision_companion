# Decision Companion System

## Overview

The **Decision Companion System** is a mathematical decision-support system that helps users choose the best option among multiple alternatives. The system uses **multi-criteria decision-making algorithms** to evaluate options objectively and consistently.

The decision process is based on:

* Rank Order Centroid (ROC) Weighting
* TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
* Monte Carlo Simulation (Sensitivity Analysis)

The system produces:

* Ranked decision options
* Best option selection
* Decision-driving criteria
* Strength and weakness analysis
* Robustness analysis under uncertainty

---

## Problem Statement

Human decision-making becomes difficult when multiple options must be compared across several criteria. Users often struggle to assign correct weights or evaluate trade-offs consistently.

This project builds a system that makes decisions using **mathematical calculations instead of subjective judgement.**

The system:

1. Accepts decision options and criteria
2. Automatically assigns weights
3. Applies decision algorithms
4. Evaluates uncertainty
5. Explains the decision logically

---

## System Architecture

### Step 1 — User Input

The user provides:

* Decision options
* Decision criteria
* Criteria priority order
* Criterion values for each option

Example:

Options:

* Option A
* Option B
* Option C

Criteria:

* Cost
* Quality
* Location

Priority Order:

1. Cost
2. Quality
3. Location

Note: Two or more criteria can share the same priority number. They will receive equal weight automatically.

---

## Step 2 — Qualitative to Numerical Conversion

Qualitative values are converted into numerical scores.

| Qualitative Value | Numeric Score |
| ----------------- | ------------- |
| Very Low          | 1             |
| Low               | 3             |
| Medium            | 5             |
| High              | 7             |
| Very High         | 9             |

This produces the **decision matrix**

| Option | C1  | C2  | C3  |
| ------ | --- | --- | --- |
| A      | x11 | x12 | x13 |
| B      | x21 | x22 | x23 |
| C      | x31 | x32 | x33 |

Where:

* m = number of options
* n = number of criteria
* xij = value of option i for criterion j

---

## Step 3 — ROC Weight Calculation

Criteria weights are calculated automatically using **Rank Order Centroid (ROC).**

Weight for criterion with rank **r**:

```
Wr = (1/n) × (1/r + 1/(r+1) + ... + 1/n)
```

Where:

* n = number of criteria
* r = rank
* Wr = weight

Properties:

* Higher rank → Higher weight
* All weights sum to 1

---

### Tied Priority Handling

If two or more criteria share the same priority rank, they occupy the same positions in the ordering. Their weights are averaged across those positions so all tied criteria receive equal weight.

Example:

Criteria: Quality (Priority 1), Distance (Priority 1), Cost (Priority 2)

Base ROC weights for 3 criteria: W1, W2, W3

Quality and Distance are both at rank 1, so they share positions 1 and 2:

```
Tied weight = (W1 + W2) / 2
```

Cost is at rank 2 and occupies position 3 normally:

```
Cost weight = W3
```

Result:

| Criterion | Priority | Weight |
| --------- | -------- | ------ |
| Quality   | 1 (tied) | 44.44% |
| Distance  | 1 (tied) | 44.44% |
| Cost      | 2        | 11.11% |

All weights still sum to 1.

---

## Step 4 — Normalization

Criteria may have different scales. Normalization removes scale differences.

Vector normalization:

```
rij = xij / sqrt(x1j² + x2j² + ... + xmj²)
```

Where:

* xij = original value
* rij = normalized value

---

## Step 5 — Weighted Normalized Matrix

Normalized values are multiplied by ROC weights.

```
vij = wj × rij
```

Where:

* wj = ROC weight
* rij = normalized value

---

## Step 6 — Ideal Best and Ideal Worst

TOPSIS defines two reference points.

### Ideal Best

```
A+ = max(v1j, v2j, ..., vmj)
```

Best value for each criterion.

---

### Ideal Worst

```
A- = min(v1j, v2j, ..., vmj)
```

Worst value for each criterion.

---

## Step 7 — Distance Calculation

Euclidean distance is used.

Distance from Ideal Best:

```
Di+ = sqrt( Σ (vij − Aj+)² )
```

Distance from Ideal Worst:

```
Di- = sqrt( Σ (vij − Aj-)² )
```

---

## Step 8 — Closeness Score

Each option receives a score:

```
Ci = Di- / (Di+ + Di-)
```

Where:

* Ci = closeness score
* 0 ≤ Ci ≤ 1

Higher value indicates better option.

---

## Step 9 — Ranking

Options are ranked based on closeness score.

```
C1, C2, ..., Cm
```

Highest score = Best option.

---

## Step 10 — Monte Carlo Simulation

Some criteria may change in the future.

Monte Carlo simulation is used to test decision stability.

Selected criteria values are varied randomly.

For a criterion value:

```
xij
```

Modified value:

```
xij' = xij + Δ
```

Where:

```
Δ = random variation
```

For each simulation:

1. Criteria values modified
2. TOPSIS repeated
3. Best option recorded

If simulation count = N

```
P(option i) = Selection Count / N
```

Option with highest probability is considered **most robust.**

This is a **Monte Carlo sensitivity analysis approach.**

---

## Step 11 — Key Criteria Identification

For the selected option:

```
Diffj = | vbest,j − Aj+ |
```

Small difference → Important criterion.

These criteria explain why the option was selected.

---

## Step 12 — Strength and Weakness Analysis

Each option is compared with the ideal solution.

Strength:

```
|vij − Aj+| is small
```

Weakness:

```
|vij − Aj+| is large
```

---

## Online Version

https://deccampanionhost.vercel.app/

---

## Run Locally

### Clone Repository

```
git clone https://github.com/ATHULYAL/decision_companion
cd source code
```


---

### Create Virtual Environment

Windows:

```
python -m venv venv
venv\Scripts\activate
```

Linux / Mac:

```
python3 -m venv venv
source venv/bin/activate
```

---

### Install Requirements

```
pip install -r requirements.txt
```

---

### Run CLI Version

```
python demo.py
```

---

### Run Web Application

```
python app.py
```

Open browser:

```
http://127.0.0.1:5000
```

---

## Algorithms Used

### Rank Order Centroid (ROC)

Automatic criteria weight calculation with support for tied priorities.

### TOPSIS

Multi-criteria ranking algorithm.

### Monte Carlo Simulation

Decision stability analysis under uncertainty.

---

## Features

* Mathematical decision making
* Automatic weighting
* Tied priority criteria handling (equal weight sharing)
* Multi-criteria comparison
* Decision explanation
* Strength and weakness analysis
* Future uncertainty handling
* CLI interface
* Web interface

---
