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

* (m) = number of options
* (n) = number of criteria
* (x_{ij}) = value of option i for criterion j

---

## Step 3 — ROC Weight Calculation

Criteria weights are calculated automatically using **Rank Order Centroid (ROC)**.

If there are **n criteria**, weight for criterion with rank **r** is:

[
W_r =
\frac{1}{n}
\sum_{i=r}^{n}
\frac{1}{i}
]

Where:

* (n) = number of criteria
* (r) = rank
* (W_r) = weight

Properties:

* Higher rank → Higher weight
* All weights sum to 1

---

## Step 4 — Normalization

Criteria may have different scales. Normalization removes scale differences.

Vector normalization is used:

[
r_{ij} =
\frac{x_{ij}}
{\sqrt{\sum_{i=1}^{m} x_{ij}^{2}}}
]

Where:

* (x_{ij}) = original value
* (r_{ij}) = normalized value

---

## Step 5 — Weighted Normalized Matrix

Normalized values are multiplied by ROC weights.

[
v_{ij} = w_j \times r_{ij}
]

Where:

* (w_j) = ROC weight
* (r_{ij}) = normalized value

Matrix:

[
V =
\begin{bmatrix}
v_{11} & v_{12} & ... & v_{1n} \
v_{21} & v_{22} & ... & v_{2n} \
... & ... & ... & ... \
v_{m1} & v_{m2} & ... & v_{mn}
\end{bmatrix}
]

---

## Step 6 — Ideal Best and Ideal Worst

TOPSIS defines two reference points.

### Ideal Best

[
A^+ =
\left(
\max v_{ij}
\right)
]

Best value for each criterion.

---

### Ideal Worst

[
A^- =
\left(
\min v_{ij}
\right)
]

Worst value for each criterion.

---

## Step 7 — Distance Calculation

Euclidean distance is used.

### Distance from Ideal Best

[
D_i^+ =
\sqrt{
\sum_{j=1}^{n}
(v_{ij} - A_j^+)^2
}
]

---

### Distance from Ideal Worst

[
D_i^- =
\sqrt{
\sum_{j=1}^{n}
(v_{ij} - A_j^-)^2
}
]

---

## Step 8 — Closeness Score

Each option receives a score:

[
C_i =
\frac{D_i^-}
{D_i^+ + D_i^-}
]

Where:

* (C_i) = closeness score
* (0 \le C_i \le 1)

Higher value indicates better option.

---

## Step 9 — Ranking

Options are ranked based on closeness score.

[
C_1, C_2, ..., C_m
]

Highest score = Best option.

---

## Step 10 — Monte Carlo Simulation

Some criteria may change in the future.

Monte Carlo simulation is used to test decision stability.

Selected criteria values are varied randomly.

For a criterion value:

[
x_{ij}
]

Modified value:

[
x_{ij}' = x_{ij} + \Delta
]

Where:

[
\Delta \sim RandomVariation
]

This produces multiple simulated scenarios.

For each simulation:

1. Criteria values modified
2. TOPSIS repeated
3. Best option recorded

If simulation count = (N)

[
P(option_i) =
\frac{\text{Times option i selected}}{N}
]

Option with highest probability is considered **most robust.**

This is a **Monte Carlo sensitivity analysis approach.**

---

## Step 11 — Key Criteria Identification

For the selected option:

Difference from ideal best:

[
Diff_j =
|v_{best,j} - A_j^+|
]

Small difference → Important criterion.

These criteria explain why the option was selected.

---

## Step 12 — Strength and Weakness Analysis

Each option is compared with the ideal solution.

Strength:

[
|v_{ij} - A_j^+| \text{ small}
]

Weakness:

[
|v_{ij} - A_j^+| \text{ large}
]

This explains performance of each option.

---

## Online Version

[https://deccampanionhost.vercel.app/](https://deccampanionhost.vercel.app/)

---

## Run Locally

### Clone Repository

```
git clone https://github.com/ATHULYAL/decision_companion
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

Automatic criteria weight calculation.

### TOPSIS

Multi-criteria ranking algorithm.

### Monte Carlo Simulation

Decision stability analysis under uncertainty.

---

## Features

* Mathematical decision making
* Automatic weighting
* Multi-criteria comparison
* Decision explanation
* Strength and weakness analysis
* Future uncertainty handling
* CLI interface
* Web interface

---

