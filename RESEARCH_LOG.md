# Research Log – Decision Companion System

## Project Title
Decision Companion System – Mathematical Decision Support Framework

---

## Objective

To build a decision-making companion system capable of solving real-world decision problems such as:

- Choosing a laptop under a budget
- Selecting the best candidate for a job role
- Deciding where to travel within constraints
- Picking an investment strategy
- Choosing a technology stack for a startup

The goal was to design a system that makes decisions using **mathematical methods instead of relying completely on AI models.**

---

## 14/02/2026 – Problem Definition

Defined the core problem:

Build a system that can assist users in making complex decisions involving multiple criteria.

Initial idea:

Create a decision-making companion that works independently of AI-based decision systems.

Example decision scenarios were identified:

- Laptop selection
- Job candidate selection
- Travel planning
- Investment decisions
- Technology stack selection

---

## 14/02/2026 – LLM-Based Approach Consideration

Considered building a Large Language Model based decision assistant.

Idea:

- Use LLM to understand user preferences
- Use web search to gather decision information
- Automatically extract criteria

Problems identified:

- Heavy computational requirements
- Dependence on external AI services
- Lack of explainability
- Non-mathematical decisions

Decision:

LLM approach rejected.

System should be mathematically explainable.

---

## 15/02/2026 – Structured Input Model

Designed a structured decision input model.

Decision problem represented as a matrix:

- Rows represent decision options
- Columns represent decision criteria

Example:

| Option | Cost | Performance | Weight |
|-------|------|-------------|--------|
| Laptop A | 7 | 8 | 6 |
| Laptop B | 6 | 9 | 5 |

Advantages:

- Clear structure
- Mathematical processing possible
- Easy implementation
- Fully explainable decisions

This became the base architecture.

---

## 16/02/2026 – Algorithm Research

Studied decision companion systems and decision algorithms.

Topics researched:

- Decision support systems
- Multi-Criteria Decision Analysis (MCDA)
- Optimization based decision methods

Goal:

Select the best algorithm for decision-making.

---

## 17/02/2026 – MCDA Selection

Selected Multi-Criteria Decision Analysis (MCDA) as the main framework.

MCDA allows:

- Comparison of multiple options
- Multiple evaluation criteria
- Mathematical decision analysis

MCDA commonly used in:

- Engineering
- Economics
- Resource allocation
- Planning systems

---

## 17/02/2026 – TOPSIS Algorithm Research

Studied the TOPSIS algorithm.

TOPSIS principle:

Best option is:

- Closest to ideal solution
- Farthest from worst solution

Reasons for choosing TOPSIS:

- Simple mathematics
- Efficient computation
- Clear ranking
- Suitable for multiple criteria
- Interpretable results

Decision:

TOPSIS selected as main decision algorithm.

---

## 18/02/2026 – Initial Implementation

Implemented first version of the system.

Features:

- User-defined options
- User-defined criteria
- User-defined weights
- TOPSIS ranking

Observation:

Users had difficulty assigning weights correctly.

---

## 20/02/2026 – Automatic Weight Assignment

Replaced manual weights with automatic weights.

Users now provide:

- Criteria priority order

Initial idea:

Weight assignment using:

1/2, 1/4, 1/8 pattern.

Later replaced with a better method.

---

## 21/02/2026 – ROC Weighting Implementation

Implemented Rank Order Centroid (ROC) weighting.

ROC formula:

Wr = (1/n) × (1/r + 1/(r+1) + ... + 1/n)

Advantages:

- Mathematically valid
- No manual weight input required
- Weights sum to 1
- Better distribution

ROC became final weighting method.

---

## 21/02/2026 – Code Validation

Performed multiple code validation cycles.

Checked for:

- Logical errors
- Weight calculation errors
- Ranking correctness
- Numerical issues

Refined the implementation.

---

## 22/02/2026 – Decision Explanation Logic

Added decision explanation capability.

System modified to explain:

- Why the best option was selected
- Which criteria influenced the decision

Method:

Compare selected option with ideal solution.

---

## 22/02/2026 – Web Application Development

Converted CLI system into a web application.

Technologies used:

- Flask backend
- HTML frontend

Files created:

- app.py
- index.html

Improved usability.

---

## 23/02/2026 – Future Criteria Handling

Identified limitation:

Some criteria change over time.

Examples:

- Investment risk
- Salary growth
- Market conditions
- Technology trends

Solution:

Monte Carlo simulation introduced.

---

## 24/02/2026 – Monte Carlo Improvements

Improved Monte Carlo logic.

System now:

- Randomly varies selected criteria
- Repeats TOPSIS
- Records best option

Purpose:

Evaluate decision stability under uncertainty.

---

## 25/02/2026 – Strength and Weakness Analysis

Added option analysis feature.

System now shows:

- Strengths of each option
- Weaknesses of each option

Method:

Compare each option with ideal solution.

Improved decision transparency.

---

## 26/02/2026 – Deployment

Deployed web application.

Platform:

Vercel

Live system:

https://deccampanionhost.vercel.app/

---

## Final System

The final system includes:

- Structured decision input
- ROC weight calculation
- TOPSIS ranking
- Monte Carlo simulation
- Decision explanation
- Strength and weakness analysis
- Web interface
- CLI interface

---

## Research Contribution

This project demonstrates that a **decision companion system can be developed using mathematical decision models without relying on large AI systems.**

The system integrates:

- Rank Order Centroid weighting
- TOPSIS ranking
- Monte Carlo sensitivity analysis

into a unified decision-support framework.

---