from flask import Flask, render_template, request, jsonify
import math
import random
import copy
from collections import Counter

app = Flask(__name__)


class DecisionEngine:
    def __init__(self):
        self.qualitative_map = {
            "very low": 1, "low": 3, "medium": 5,
            "high": 7, "very high": 9
        }
        self.value_label_map = {
            1: "very low", 2: "very low",
            3: "low",      4: "low",
            5: "medium",   6: "medium",
            7: "high",     8: "high",
            9: "very high"
        }

    def value_to_label(self, value):
        rounded = max(1, min(9, round(float(value))))
        return self.value_label_map.get(rounded, "medium")

    def calculate_roc_weights(self, num_criteria):
        """Standard ROC weights for strict priority order."""
        weights = []
        for i in range(1, num_criteria + 1):
            weight = sum(1.0 / j for j in range(i, num_criteria + 1)) / num_criteria
            weights.append(weight)
        return weights

    def calculate_roc_weights_with_ties(self, priorities):
        """
        ROC weights that handle tied priorities.

        Tied criteria occupy the same positions in the ordering.
        Their weights are averaged so tied criteria are treated equally.

        Example: priorities = [1, 1, 2]
          - Positions 1 and 2 are both occupied by the tied pair.
          - Each tied criterion gets avg(ROC_weight_1, ROC_weight_2).
          - The third criterion gets ROC_weight_3 normally.
        """
        n = len(priorities)
        base_weights = self.calculate_roc_weights(n)

        sorted_unique = sorted(set(priorities))

        slot_cursor = 0
        priority_to_slots = {}
        for p in sorted_unique:
            count = priorities.count(p)
            priority_to_slots[p] = list(range(slot_cursor, slot_cursor + count))
            slot_cursor += count

        priority_to_weight = {
            p: sum(base_weights[s] for s in slots) / len(slots)
            for p, slots in priority_to_slots.items()
        }

        return [priority_to_weight[p] for p in priorities]

    def _to_float(self, value):
        if value is None: return 5.0
        if isinstance(value, str):
            try:
                return float(value.strip())
            except ValueError:
                return float(self.qualitative_map.get(value.lower().strip(), 5.0))
        try:
            return float(value)
        except (ValueError, TypeError):
            return 5.0

    def run_topsis(self, options, criteria):
        norm_matrix = {}
        for crit in criteria:
            c_id = crit['id']
            sq_sum = sum(opt['values'][c_id] ** 2 for opt in options)
            denominator = math.sqrt(sq_sum) if sq_sum > 0 else 1
            for opt in options:
                norm_matrix.setdefault(opt['name'], {})
                norm_matrix[opt['name']][c_id] = (opt['values'][c_id] / denominator) * crit['weight']

        ideal_best, ideal_worst = {}, {}
        for crit in criteria:
            c_id = crit['id']
            vals = [norm_matrix[o['name']][c_id] for o in options]
            if crit['type'] == 'benefit':
                ideal_best[c_id], ideal_worst[c_id] = max(vals), min(vals)
            else:
                ideal_best[c_id], ideal_worst[c_id] = min(vals), max(vals)

        results = []
        for opt in options:
            name = opt['name']
            d_best  = math.sqrt(sum((norm_matrix[name][c['id']] - ideal_best[c['id']]) ** 2 for c in criteria))
            d_worst = math.sqrt(sum((norm_matrix[name][c['id']] - ideal_worst[c['id']]) ** 2 for c in criteria))
            score = d_worst / (d_best + d_worst) if (d_best + d_worst) > 0 else 0.5
            results.append({"name": name, "score": score})

        return sorted(results, key=lambda x: x['score'], reverse=True), ideal_best, ideal_worst, norm_matrix

    def simulate_decision(self, options, criteria, iterations=1000):
        win_counts = {opt['name']: 0 for opt in options}

        float_options = [
            {
                "name": opt['name'],
                "values": {c['id']: self._to_float(opt['values'].get(c['id'])) for c in criteria}
            }
            for opt in options
        ]

        for _ in range(iterations):
            shared_shift = {c['id']: random.gauss(0, 1.2) for c in criteria if c.get('dynamic')}
            sim_options = []
            for opt in float_options:
                temp_vals = opt['values'].copy()
                for c_id, shift in shared_shift.items():
                    temp_vals[c_id] = max(1, min(9, temp_vals[c_id] + shift + random.gauss(0, 0.3)))
                sim_options.append({"name": opt['name'], "values": temp_vals})

            pass_results, _, _, _ = self.run_topsis(sim_options, criteria)
            win_counts[pass_results[0]['name']] += 1

        return sorted(
            [{"name": n, "confidence": round((c / iterations) * 100, 2)} for n, c in win_counts.items()],
            key=lambda x: x['confidence'], reverse=True
        )

    def explain_all(self, options, criteria):
        results, ideal_best, ideal_worst, norm_matrix = self.run_topsis(options, criteria)

        ideal_raw = {}
        worst_raw = {}
        for crit in criteria:
            c_id = crit['id']
            raw_vals = [opt['values'][c_id] for opt in options]
            if crit['type'] == 'benefit':
                ideal_raw[c_id] = max(raw_vals)
                worst_raw[c_id] = min(raw_vals)
            else:
                ideal_raw[c_id] = min(raw_vals)
                worst_raw[c_id] = max(raw_vals)

        all_explanations = {}

        for opt in options:
            opt_name = opt['name']
            opt_norm = norm_matrix[opt_name]
            explanation = []

            for crit in criteria:
                c_id      = crit['id']
                actual    = opt['values'][c_id]
                ideal_val = ideal_raw[c_id]
                worst_val = worst_raw[c_id]

                raw_range = abs(ideal_val - worst_val)
                gap_pct   = abs(actual - ideal_val) / raw_range * 100 if raw_range > 0 else 0.0

                all_vals = [norm_matrix[o['name']][c_id] for o in options]
                wv       = opt_norm[c_id]
                is_best  = (wv == max(all_vals) if crit['type'] == 'benefit' else wv == min(all_vals))

                explanation.append({
                    "name":     crit['name'],
                    "actual":   actual,
                    "gap_pct":  round(gap_pct, 1),
                    "is_best":  is_best,
                    "type":     crit['type'],
                    "weight":   crit['weight'],
                    "priority": crit.get('priority', 1),
                    "tied":     crit.get('tied', False),
                })

            explanation.sort(key=lambda x: x['gap_pct'])
            all_explanations[opt_name] = explanation

        return all_explanations, results


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json

        decision_goal = data.get('goal', 'Decision')
        criteria_data = data.get('criteria', [])
        options_data  = data.get('options', [])

        if not criteria_data or not options_data:
            return jsonify({'error': 'Please provide both criteria and options'}), 400

        engine = DecisionEngine()

        # Extract priorities — default to position order if not provided
        priorities = [int(c.get('priority', i + 1)) for i, c in enumerate(criteria_data)]
        priority_counts = Counter(priorities)

        # Assign weights using tied-aware ROC
        weights = engine.calculate_roc_weights_with_ties(priorities)

        criteria = []
        for i, crit in enumerate(criteria_data):
            criteria.append({
                'id':       f'c{i}',
                'name':     crit['name'],
                'type':     crit['type'],
                'dynamic':  crit.get('dynamic', False),
                'priority': priorities[i],
                'tied':     priority_counts[priorities[i]] > 1,
                'weight':   weights[i]
            })

        options = []
        for opt in options_data:
            option_values = {}
            for i, value in enumerate(opt['values']):
                option_values[f'c{i}'] = engine._to_float(value)
            options.append({'name': opt['name'], 'values': option_values})

        original_options = copy.deepcopy(options)

        simulation_results = engine.simulate_decision(options, criteria, iterations=1000)
        all_explanations, topsis_results = engine.explain_all(original_options, criteria)

        # Winner reasoning
        winner_name = simulation_results[0]['name']
        winner_expl = all_explanations[winner_name]
        best_crit   = min(winner_expl, key=lambda e: (e['gap_pct'], -e['weight']))
        value_label = engine.value_to_label(best_crit['actual'])
        reasoning   = (
            f"'{winner_name}' is selected due to its {value_label} "
            f"{best_crit['name']}."
        )

        # Per-option breakdown
        option_breakdown = []
        for opt in original_options:
            opt_name   = opt['name']
            expl       = all_explanations[opt_name]
            confidence = next(r['confidence'] for r in simulation_results if r['name'] == opt_name)
            rank       = next(i + 1 for i, r in enumerate(simulation_results) if r['name'] == opt_name)

            opt_best_crit = min(expl, key=lambda e: (e['gap_pct'], -e['weight']))
            opt_val_label = engine.value_to_label(opt_best_crit['actual'])
            opt_sentence  = (
                f"'{opt_name}' is notable for its {opt_val_label} "
                f"{opt_best_crit['name']}."
            )

            strengths  = [e['name'] for e in expl if e['gap_pct'] <= 40]
            weaknesses = [e['name'] for e in expl if e['gap_pct'] > 40]

            option_breakdown.append({
                "name":           opt_name,
                "rank":           rank,
                "confidence":     confidence,
                "selection_note": opt_sentence,
                "strengths":      strengths,
                "weaknesses":     weaknesses,
            })

        return jsonify({
            'success':            True,
            'goal':               decision_goal,
            'criteria': [
                {
                    'name':     c['name'],
                    'type':     c['type'],
                    'dynamic':  c['dynamic'],
                    'priority': c['priority'],
                    'tied':     c['tied'],
                    'weight':   round(c['weight'] * 100, 2)
                }
                for c in criteria
            ],
            'simulation_results': simulation_results,
            'topsis_results': [
                {'rank': i+1, 'name': r['name'], 'score': round(r['score'] * 100, 2)}
                for i, r in enumerate(topsis_results)
            ],
            'reasoning':        reasoning,
            'option_breakdown': option_breakdown,
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)