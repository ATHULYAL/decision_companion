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

Defined the core problem: build a system that can assist users in making complex decisions involving multiple criteria.

**Tool used:** ChatGPT

**Prompt:**
> I need to build a decision making companion that can make decisions like choosing a laptop under a budget, selecting the best candidate for a job role, deciding where to travel within constraints, picking an investment strategy, choosing a tech stack for a startup — without completely relying on AI.

**What I got:** General overview of approaches — rule-based systems, weighted scoring, AI-assisted recommendations.

**What I accepted:** The idea that a structured mathematical approach would be more transparent than a pure AI solution.

**What I rejected:** Suggestions to use a fully AI-driven pipeline — the task required explainable logic, not a black box.

---

## 14/02/2026 – LLM-Based Approach Consideration

**Tool used:** ChatGPT

**Prompt:**
> Should I consider building an LLM to understand the decision options and user preferences? Because sometimes we need to do web search to make decisions — users may not know about all the options.

**What I got:** A discussion about LLM capabilities for preference extraction and web search integration.

Problems identified with LLM approach:
- Heavy computational requirements
- Dependence on external AI services
- Lack of explainability
- Decisions not mathematically traceable

**Decision:** LLM approach rejected. System should be mathematically explainable.

**What I accepted:** The idea that web search could help users who don't know their options — kept as a future enhancement idea only.

---

## 15/02/2026 – Structured Input Model

Designed a structured decision input model — own thinking based on the previous day's conclusions, no AI tool used.

Decision problem represented as a matrix:
- Rows represent decision options
- Columns represent decision criteria

Example:

| Option | Cost | Performance | Weight |
|--------|------|-------------|--------|
| Laptop A | 7 | 8 | 6 |
| Laptop B | 6 | 9 | 5 |

**Why this approach:** Clear structure, mathematical processing possible, fully explainable decisions. This became the base architecture.

---

## 16/02/2026 – Algorithm Research

**Tool used:** Google

**Search query:** `decision making companions`

**What I found:** Various decision support tools, multi-criteria decision analysis frameworks, weighted scoring tools.

**What it influenced:** Confirmed that MCDA (Multi-Criteria Decision Analysis) is the right category of solution for this problem.

---

**Tool used:** Claude

**Prompt:**
> Compare all these algorithms and choose the best one for a decision making system.

**What I got:** Comparison of weighted sum model, AHP, TOPSIS, ELECTRE, VIKOR.

**What I accepted:** TOPSIS stood out — handles both benefit and cost criteria, mathematically grounded, output is intuitive to explain.

**What I rejected:** AHP (too complex for user input), ELECTRE (output hard to explain), weighted sum (too simplistic, does not handle cost vs benefit properly).

---

## 17/02/2026 – MCDA and TOPSIS Research

**Tool used:** Wikipedia

**Search query:** `MCDA`

**What I found:** Overview of Multi-Criteria Decision Analysis, list of methods, theoretical grounding. Confirmed TOPSIS as a well-established method within MCDA.

---

**Tool used:** GeeksForGeeks

**Search query:** `TOPSIS MCDA algorithm`

**What I found:** Step-by-step explanation of TOPSIS with a worked example.

**What I accepted:** The full algorithm — normalisation, weighted normalisation, ideal best and worst, distance calculation, closeness coefficient.

**What I modified:** Adapted the standard implementation to accept both benefit and cost criteria with user-specified types.

TOPSIS principle — best option is:
- Closest to the ideal solution
- Farthest from the worst solution

Reasons for choosing TOPSIS:
- Simple mathematics
- Efficient computation
- Clear ranking output
- Suitable for multiple criteria
- Interpretable results

---

## 18/02/2026 – Initial Implementation

**Tool used:** ChatGPT

**Prompt:**
> How about using TOPSIS algorithm for this project?

**What I got:** Confirmation that TOPSIS is suitable, explanation of its strengths for multi-criteria decision problems.

---

**Tool used:** Claude

**Prompt:**
> Can you generate a Python code where TOPSIS algorithm is used for making a decision — decision, options, and parameters, weight for each parameter, and parameter value for each option is asked from the user itself.

**What I got:** A working Python CLI script that collected user input and ran TOPSIS.

**What I accepted:** The core structure — input loop, TOPSIS calculation, ranked output.

**What I modified:** Weight input method (later changed from manual entry to priority-based), output formatting, error handling.

**Observation:** Users had difficulty assigning exact weight percentages. Most people can say "price matters most" but cannot say "price should be 37.5% of my decision." This led to the priority-based weight system in the next version.

---

## 19/02/2026 – Peer Review

Shared the working version with a peer for feedback.

**What came out of it:** Confirmed the usability issue with manual weight entry. Identified that the output needed a plain-language explanation, not just a ranked list with scores.

---

## 20/02/2026 – Automatic Weight Assignment

**Tool used:** Claude

**Prompt:**
> Instead of asking weight from the users, let's ask them to enter parameters in order and assign weight by first dividing ½ then 0.5/2 like that.

**What I got:** Modified code using halving weights — priority 1 gets 50%, priority 2 gets 25%, priority 3 gets 12.5%, normalised to sum to 1.

**What I accepted:** The concept of deriving weights from priority order rather than asking for them directly.

**What I later changed:** The halving method is not mathematically grounded. Replaced with ROC (Rank Order Centroid) weights in the next version.

---

## 21/02/2026 – ROC Weighting and Bug Fixing

**Tool used:** Gemini

**Prompt:**
> [Pasted code] Does this code have any potential bugs? If so, explain and regenerate.

**What I got:** Identified issues with input validation, edge cases in normalisation when all values are equal, missing error handling for non-numeric input.

**What I accepted:** Input validation improvements, edge case handling for zero division in normalisation.

**What I rejected:** Some suggested refactoring that over-complicated the structure without adding value.

---

**Tool used:** Claude

**Prompt:**
> [Pasted new code] Does this code have any bugs? If so, explain and regenerate.

**What I got:** Fix for criterion type validation (only accept "1" or "2"), improved normalisation safety.

---

**Activity:** Replaced halving weights with ROC (Rank Order Centroid) weights.

ROC formula:
```
Wr = (1/n) × (1/r + 1/(r+1) + ... + 1/n)
```

Advantages:
- Mathematically valid and peer-reviewed method
- No manual weight input required
- Weights always sum to 1
- Better distribution than halving

ROC became the final weighting method.

---

## 22/02/2026 – Decision Explanation and Web App

**Tool used:** Claude

**Prompt:**
> Can you again modify the logic so that reasoning for why this option is selected is shown — by comparing the criteria of the top option with the ideal case and explaining which feature had the most influence.

**What I got:** An `explain_winner()` function that found the criterion with the smallest gap from ideal and wrote a plain-language sentence.

**What I accepted:** The gap-based reasoning approach — closest to ideal on the most important criterion becomes the explanation.

**What I modified later:** Original reasoning had a bug where it converted raw values to labels — fixed in a later version.

---

**Tool used:** Claude

**Prompt:**
> [Pasted new code] Make it into a Flask application with app.py and index.html.

**What I got:** Full Flask web application with a multi-step form — criteria input, options input, results display.

**What I accepted:** The Flask structure and the step-by-step form flow.

---

**Tool used:** Gemini

**Prompt:**
> [Pasted code] Is this code production ready?

**What I got:** Feedback on missing error handling, debug mode left on, no input sanitisation, no loading state for the form.

**What I accepted:** Turned off Flask debug mode, added basic input sanitisation and form validation.

**What I rejected:** Suggestion to add a database — not needed for this project scope, adds unnecessary complexity.

---

## 23/02/2026 – Dynamic Criteria Handling

**Tool used:** ChatGPT

**Prompt:**
> [Pasted code] Modify the code so that it can handle criteria which may tend to change in the future — like risk during decisions such as which stock to buy.

**What I got:** Suggestion to add a dynamic/uncertain flag per criterion and use simulation to handle uncertainty.

**What I accepted:** The concept of marking criteria as dynamic and running multiple iterations.

**What I modified:** The specific simulation approach — refined in the next session to use Gaussian noise with a shared market shift and individual option nudge.

---

## 24/02/2026 – Monte Carlo Simulation

**Tool used:** Gemini

**Prompt:**
> [Pasted code] Modify code so that it can handle criteria that change in the future — like risk to select a tech stack for a startup.

**What I got:** Another version of uncertainty handling with value clamping to stay within 1–9 scale during simulation.

**What I accepted:** The clamping logic — `max(1, min(9, value + shift))`.

---

**Tool used:** Gemini

**Search query:** `What is Monte Carlo algorithm`

**What I found:** Explanation of Monte Carlo simulation — running many random iterations to understand the range of possible outcomes and find the most robust result.

**What it influenced:** Confirmed Monte Carlo as the right name and right approach. System now runs 1000 TOPSIS iterations with randomly varied dynamic criteria values and reports how often each option wins as a confidence percentage.

---

**Tool used:** Claude

**Prompt:**
> [Pasted code] Is this logic good for future criteria handling or buggy? If so explain and modify.

**What I got:** Identified Bug — simulation was mutating the original options list. Fixed by building a separate `float_options` list before simulation and never touching the original.

---

**Tool used:** Gemini

**Prompt:**
> [Pasted modified code] Is this good or a red flag?

**What I got:** Confirmed the fix was correct. Also flagged that `explain_winner` was being called multiple times, running TOPSIS repeatedly instead of once. Fixed to run TOPSIS once and reuse the result for all explanations.

---

## 25/02/2026 – Strength and Weakness Analysis

**Tool used:** Claude

**Prompt:**
> Please show weakness and strength of each option at the end by comparing options with ideal case.

**What I got:** A strength/weakness breakdown using gap percentage.

Method:
```
gap% = |actual value − ideal value| / range × 100
```

Classification:
- Strength — gap% ≤ 40% (close to ideal)
- Weakness — gap% > 40% (far from ideal)

**What I accepted:** The gap threshold approach and the output format showing [+] for strengths and [-] for weaknesses.

---

**Tool used:** Claude

**Prompt:**
> Modify logic in app.py and index.html.

**What I got:** Updated Flask web app with strength/weakness section in the results page.

---

## 26/02/2026 – Deployment and Tied Priority Support

**Tool used:** ChatGPT

**Search query:** `Best platform to host a Flask app without a database for free`

**What I found:** Render, Railway, Vercel, PythonAnywhere, Fly.io.

**What I accepted:** Vercel — free, fast setup, supports Python.

---

**Tool used:** ChatGPT

**Prompt:**
> Step by step instruction to host this Flask code and HTML code in Vercel.

**What I got:** Instructions for creating `vercel.json`, structuring the project, deploying via Vercel CLI.

**Deployed at:** https://deccampanionhost.vercel.app/

---

**Tool used:** ChatGPT

**Prompt:**
> [Pasted code] Modify the code so that it could handle criteria with the same priority — like sometimes academics and placements while selecting a college.

**What I got:** A version of tied priority handling using grouped averaging.

**What I accepted:** The concept. Implemented the ROC weight averaging logic myself across tied slots.

---

**Tool used:** Claude

**Prompt:**
> Convert modified code to existing app.py and existing index.html.

**What I got:** The tied priority logic integrated cleanly into the full Flask application.

---

## 01/03/2026 – Reasoning Logic Fix

**Tool used:** Claude

**Prompt:**
> Modify reasoning logic so that it could handle this test case — laptop criteria: performance, price. Options: Acer, Asus. Both have high performance and Acer is expensive but reasoning is still showing due to high weight on performance. So improve logic.

**Problem identified:** Old reasoning picked the smallest gap criterion even when two options were tied on it. If both had "high performance," the system would still say "selected due to performance" — which is misleading because performance was not what separated the winner.

**What I got:** A `find_differentiating_crit()` function:
- Step 1: Find criteria where the winner's gap is strictly smaller than ALL other options
- Step 2: Among those, pick the highest-weight one
- Step 3: Fall back to lowest gap / highest weight if no unique differentiator exists

**Also fixed in this session:** Raw value display bug — stopped converting user values to labels, stored the exact string the user typed in a `raw_values_map` and used it directly in the reasoning sentence.

**Result:**
> *'Acer' is selected due to its price of 1000.*

Not performance (tied), but price (the thing that actually separated the options).

---

## Final System

The final system includes:

- Structured decision input (words or numbers accepted)
- ROC weight calculation with tied priority support
- TOPSIS ranking
- Monte Carlo simulation for uncertain criteria (1000 iterations)
- Decision explanation using differentiating criterion logic
- Strength and weakness analysis per option
- Web interface deployed on Vercel
- CLI interface

---

## Summary — AI Tools Used

| Tool | How it was used |
|------|----------------|
| ChatGPT | Initial problem framing, TOPSIS validation, dynamic criteria concept, deployment instructions, tied priority concept |
| Claude | Code generation, bug analysis, Flask conversion, strength/weakness feature, reasoning logic improvements |
| Gemini | Bug review, production readiness check, Monte Carlo confirmation, simulation bug fixes |
| Wikipedia | MCDA theoretical background |
| GeeksForGeeks | TOPSIS algorithm step-by-step reference |
| Google | Initial landscape research on decision companion tools |

---

## What I Accepted, Rejected, and Modified from AI

| Decision | What happened |
|----------|--------------|
| LLM-based approach | **Rejected** — hides system design, not what was being evaluated |
| Halving weights | **Accepted then replaced** — simple but not mathematically grounded, replaced with ROC |
| TOPSIS from Claude | **Accepted with modifications** — core algorithm kept, input and output adapted |
| Manual weight entry | **Rejected** — replaced with priority-based entry, far more intuitive |
| ChatGPT's dynamic criteria handling | **Accepted concept, modified implementation** — refined to Gaussian noise with shared shift |
| Gemini's production readiness feedback | **Partially accepted** — took validation and debug mode fixes, rejected database suggestion |
| Database for Flask app | **Rejected** — unnecessary complexity for this scope |
| Claude's gap-based reasoning | **Accepted then improved** — original had label conversion bug, fixed with raw value map |
| Differentiating criterion logic | **Accepted fully** — correctly solved the tied-criteria reasoning problem |

---

## Research Contribution

This project demonstrates that a **decision companion system can be developed using mathematical decision models without relying on large AI systems.**

The system integrates:

- Rank Order Centroid weighting
- TOPSIS ranking
- Monte Carlo sensitivity analysis

into a unified, transparent, and explainable decision-support framework.
