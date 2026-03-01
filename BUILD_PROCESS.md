# Build Process — Decision Companion System

This is the journey I went through while building this project — the ideas I had, the changes I made, and the problems I ran into along the way.

---

## The First Idea — An AI Chatbot

My first idea was to build a **conversational AI chatbot** where the system would:

- Chat with the user to understand what decision they are trying to make
- Figure out the criteria and their importance from the conversation
- Search the web to find options if the user did not provide them
- Weigh everything automatically and recommend the best choice

A flowchart was drawn for this idea and saved in the diagrams directory.

Using AI was allowed — but the task was not looking for a fully black box system where AI does everything invisibly. What was actually being evaluated was **system design** — how I structure the logic, how I break the problem into components, and how I make the decision process transparent and explainable.

A pure AI chatbot would hide all of that. The reasoning would be inside the model with no clear structure to show. So I moved away from that idea and built a system where every step is **explicit and traceable** — the weights are calculated by a known formula, the ranking follows a defined algorithm, and the explanation comes from real gap calculations, not a language model guessing.

AI was still kept as an optional enhancement idea (for input parsing and web search), but the core decision engine was built to be fully mathematical and transparent.

---

## Version 1 — Simple Priority-Based TOPSIS with Halving Weights

**What changed:** Built the first working version of the system.

The user would enter criteria in order from most to least important. Weights were assigned automatically using a **halving logic:**

- Priority 1 gets 50% of total weight
- Priority 2 gets 25%
- Priority 3 gets 12.5%
- And so on...

Then these were normalised to sum to 1.

The system then ran **TOPSIS** (Technique for Order Preference by Similarity to Ideal Solution) to rank the options. TOPSIS works by finding an imaginary "ideal best" and "ideal worst" option and scoring each real option by how close it is to the ideal.

**Output:** A ranked list of options with a score.

**Problem with this version:** The halving weight method is simple but not mathematically well-grounded. Also, all values had to be entered as numbers — no words like "High" or "Low" were accepted yet.

---

## Version 2 — Switched to ROC Weights + Qualitative Input

**What changed:** Two important upgrades.

**1. Replaced halving weights with ROC (Rank Order Centroid) weights.**

ROC is a recognised method for assigning weights from priority rankings. The formula is:

```
Wr = (1/n) × (1/r + 1/(r+1) + ... + 1/n)
```

This gives a more mathematically fair distribution than simple halving.

**2. Added qualitative input.**

Users could now type words instead of numbers:

| Word      | Number |
|-----------|--------|
| Very Low  | 1      |
| Low       | 3      |
| Medium    | 5      |
| High      | 7      |
| Very High | 9      |

Raw numbers were still accepted as well.

**Output:** Same ranked list but with fairer weights and friendlier input.

---

## Version 3 — Added "Why It Won" Explanation

**What changed:** After the ranking, the system now tells the user **why** the top option won.

The logic was: find the criteria where the winner's value was closest to the ideal (smallest gap), and use the most important one (highest weight as tiebreak) to write a sentence like:

> *'Laptop A' is the best option due to its low price and high performance.*

The values shown in the sentence came from the original user input so the explanation made sense in plain language.

**Why this mattered:** A ranked list alone is not helpful. Users need to understand the reason behind the recommendation to trust it.

---

## Version 4 — Added Monte Carlo Simulation for Uncertain Criteria

**What changed:** Some criteria in real life are uncertain — prices change, conditions vary. A new feature was added to handle this.

When entering criteria, the user can now mark any criterion as **dynamic** (uncertain). The system then runs **1,000 simulations** where those criteria values are randomly varied each time using Gaussian noise:

- A shared shift is applied to all options for the same criterion: `N(0, 1.2)`  
- A small individual noise is added per option: `N(0, 0.3)`
- Values are clamped to stay in the 1–9 range

Each simulation runs full TOPSIS and records the winner. At the end, confidence is calculated:

```
Confidence = (times this option won) / 1000 × 100%
```

The option with the highest confidence is the most **robust** choice — it holds up even when conditions change.

**Bugs fixed in this version:**

- **Bug 1:** `explain_winner` was being called multiple times, running TOPSIS repeatedly. Fixed by running TOPSIS once and reusing the result for all options.
- **Bug 2:** The "ideal" value shown to the user was the internal normalised TOPSIS number, which is meaningless. Fixed to show the actual best raw value across all options.
- **Bug 3:** The simulation was mutating the original options list. Fixed by building a separate `float_options` list and never touching the original.
- **Bug 4:** The criterion type input (benefit/cost) accepted anything. Fixed to only accept exactly "1" or "2".

---

## Version 5 — Added Strength and Weakness Breakdown for Every Option

**What changed:** The results section was expanded to show a full **strength and weakness profile for every option**, not just the winner.

For each option, every criterion is checked against the ideal value. The gap percentage is calculated:

```
gap% = |actual value − ideal value| / range × 100
```

Then classified:

- **Strength** — gap% ≤ 40% (this option is close to ideal on this criterion)
- **Weakness** — gap% > 40% (this option falls far from ideal on this criterion)

The breakdown is shown for every option in the results, not just the winner. This means the user can see exactly where each option is strong and where it falls short — making it easier to understand trade-offs.

Example output:

```
  [#1] Asus  (72.3% confidence)
  Notable for: price of 100
  ────────────────────────────────────────
    Strengths:
      [+] price          value=100   ideal=100   gap=0.0%
      [+] performance    value=5.0   ideal=7.0   gap=28.6%
    Weaknesses:
      [-] battery        value=3.0   ideal=7.0   gap=57.1%
```

**Why this mattered:** Knowing the winner is not enough. Users need to know the full picture — what they are gaining and what they are giving up with each choice.

---

## Version 6 — Added Tied Priority Support

**What changed:** Previously, every criterion needed a unique priority number (1, 2, 3...). In real decisions, two criteria can be equally important.

Tied priority support was added so that if two criteria are both given priority 1, they automatically share equal weight.

The logic:

1. Sort priorities to find which slot positions each group occupies
2. Average the ROC weights across those positions
3. All tied criteria get the same averaged weight

Example — priorities `[1, 1, 2]`:

| Criterion | Priority | Weight  |
|-----------|----------|---------|
| Quality   | 1 (tied) | 44.44%  |
| Distance  | 1 (tied) | 44.44%  |
| Cost      | 2        | 11.11%  |

All weights still sum to 100%.

The UI was also updated to show a `(tied)` badge next to criteria that share a priority.

---

## Version 6 — Fixed the Reasoning Bug (Raw Value Display)

**What changed:** A bug was found where the "why it won" sentence showed misleading information.

**The problem:** When the winner had `price = 100`, the old code converted that to a 1–9 label using `value_to_label()`. Because 100 was clamped to 9, it became "very high price" — which is completely wrong for a cost criterion where lower is better.

**The fix:** Stop converting values to labels. Instead, store the exact string the user typed (`"100"`, `"high"`, `"medium"`, etc.) in a `raw_values_map` before any conversion happens. Use that original string directly in the reasoning sentence.

Result:
> *'Asus' is selected due to its price of 100.*

Exactly what the user entered, no interpretation.

**Also added:** `"id"` field to each explanation entry so the raw value can be looked up by criterion ID.

---

## Version 7 — Added Differentiating Criterion Logic

**What changed:** The old reasoning just picked the winner's criterion with the smallest gap. But what if two options both have "High" performance? The old logic would still say the winner won "due to its performance" even though it was tied.

A smarter function called `find_differentiating_crit()` was added:

**Step 1:** Find criteria where the winner's gap is **strictly smaller than ALL other options** — meaning the winner is genuinely better on that criterion, not just tied at ideal.

**Step 2:** If multiple such criteria exist, pick the one with the highest weight (most important).

**Step 3:** If no unique differentiating criterion exists (everything is tied), fall back to lowest gap / highest weight as before.

This means the reasoning sentence now points to something that actually separates the winner from the competition.

Example — both options have the same performance, but different prices:
> *'Acer' is selected due to its price of 1000.*

Not performance (tied), but price (genuinely better).

---

## Final State — What the System Does Now

The current system, in simple terms:

1. **User enters** a decision goal, criteria with priorities (ties allowed), whether each criterion is dynamic, and option values (words or numbers)
2. **ROC weights** are calculated automatically, with tied criteria sharing equal weight
3. **Values are converted** from words to numbers if needed, and raw user strings are saved for display
4. **TOPSIS** ranks all options by how close they are to the ideal solution
5. **Monte Carlo simulation** runs 1,000 times with random variation on dynamic criteria to find the most robust winner
6. **Explanation engine** finds the criterion that genuinely differentiates the winner from all others and writes a plain-language sentence using the original user value
7. **Strength and weakness breakdown** shows each option's gap from ideal per criterion — gap ≤ 40% is a strength, gap > 40% is a weakness

The system is available as both a **CLI script** (`demo.py`) and a **web application** (`app.py`).

---

## Summary of Changes

| Version | What Was Added or Fixed |
|---------|------------------------|
| 1 | Basic TOPSIS with halving weights, numeric input only |
| 2 | ROC weights, qualitative word input (High / Low etc.) |
| 3 | "Why it won" explanation sentence |
| 4 | Monte Carlo simulation for dynamic criteria, 4 bug fixes |
| 5 | Strength and weakness breakdown for every option (gap% ≤ 40% = strength) |
| 6 | Tied priority support — equal weight sharing |
| 7 | Reasoning bug fix — show raw user value, not a converted label |
| 8 | Differentiating criterion logic — find what actually separates the winner |
