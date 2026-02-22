# app.py
from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

class DecisionEngine:
    def __init__(self):
        self.qualitative_map = {
            "very low": 1, "low": 3, "medium": 5, 
            "high": 7, "very high": 9
        }

    def calculate_roc_weights(self, num_criteria):
        """Calculates weights based on priority rank using ROC."""
        weights = []
        for i in range(1, num_criteria + 1):
            weight = sum(1.0 / j for j in range(i, num_criteria + 1)) / num_criteria
            weights.append(weight)
        return weights

    def _to_float(self, value):
        if isinstance(value, str):
            val = value.lower().strip()
            return float(self.qualitative_map.get(val, 5))
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def run_topsis(self, options, criteria):
        if not options or not criteria:
            return {"error": "Insufficient data"}

        # 1. Normalization
        norm_matrix = {}
        for crit in criteria:
            c_id = crit['id']
            sq_sum = sum(self._to_float(opt['values'].get(c_id, 0))**2 for opt in options)
            denominator = math.sqrt(sq_sum)
            
            for opt in options:
                name = opt['name']
                if name not in norm_matrix: norm_matrix[name] = {}
                val = self._to_float(opt['values'].get(c_id, 0))
                norm_matrix[name][c_id] = (val / denominator) if denominator != 0 else 0

        # 2. Weighted Matrix
        weighted_matrix = {}
        for opt_name, scores in norm_matrix.items():
            weighted_matrix[opt_name] = {
                c_id: scores[c_id] * next(c['weight'] for c in criteria if c['id'] == c_id)
                for c_id in scores
            }

        # 3. Ideal Solutions
        ideal_best, ideal_worst = {}, {}
        
        for crit in criteria:
            c_id = crit['id']
            v_list = [weighted_matrix[opt['name']][c_id] for opt in options]
            
            if crit['type'] == 'benefit':
                ideal_best[c_id] = max(v_list)
                ideal_worst[c_id] = min(v_list)
            else:
                ideal_best[c_id] = min(v_list)
                ideal_worst[c_id] = max(v_list)

        # 4. Scoring
        results = []
        for opt in options:
            name = opt['name']
            d_best = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_best[c['id']])**2 for c in criteria))
            d_worst = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_worst[c['id']])**2 for c in criteria))
            
            total_dist = d_best + d_worst
            performance_score = (d_worst / total_dist) if total_dist != 0 else 0.5
            
            results.append({
                "name": name,
                "score": round(performance_score, 4),
                "weighted_values": weighted_matrix[name],
                "original_values": opt['values']
            })

        # Sort by score
        results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        return results, ideal_best, weighted_matrix, criteria

    def generate_reasoning(self, top_option, ideal_best, weighted_matrix, criteria):
        """Generate reasoning statement with original user values"""
        matching_criteria = []
        threshold = 0.05
        
        for crit in criteria:
            c_id = crit['id']
            option_weighted = top_option['weighted_values'][c_id]
            ideal_value = ideal_best[c_id]
            
            if ideal_value != 0:
                diff_pct = abs(option_weighted - ideal_value) / abs(ideal_value)
            else:
                diff_pct = abs(option_weighted - ideal_value)
            
            if diff_pct <= threshold:
                original_input = top_option['original_values'][c_id]
                
                matching_criteria.append({
                    'name': crit['name'],
                    'value': original_input,
                    'type': crit['type'],
                    'weight': crit['weight']
                })
        
        matching_criteria.sort(key=lambda x: x['weight'], reverse=True)
        
        return matching_criteria


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        
        # Extract data
        decision_goal = data.get('goal', 'Decision')
        criteria_data = data.get('criteria', [])
        options_data = data.get('options', [])
        
        if not criteria_data or not options_data:
            return jsonify({'error': 'Please provide both criteria and options'}), 400
        
        # Initialize engine
        engine = DecisionEngine()
        
        # Calculate ROC weights
        num_criteria = len(criteria_data)
        weights = engine.calculate_roc_weights(num_criteria)
        
        # Prepare criteria with weights
        criteria = []
        for i, crit in enumerate(criteria_data):
            criteria.append({
                'id': f'c{i}',
                'name': crit['name'],
                'type': crit['type'],
                'weight': weights[i]
            })
        
        # Prepare options
        options = []
        for opt in options_data:
            option_values = {}
            for i, value in enumerate(opt['values']):
                option_values[f'c{i}'] = value
            
            options.append({
                'name': opt['name'],
                'values': option_values
            })
        
        # Run TOPSIS
        results, ideal_best, weighted_matrix, criteria_list = engine.run_topsis(options, criteria)
        
        # Generate reasoning
        reasoning_text = ""
        matching_criteria = []
        
        if results:
            top_option = results[0]
            matching_criteria = engine.generate_reasoning(
                top_option, ideal_best, weighted_matrix, criteria_list
            )
            
            if matching_criteria:
                option_name = top_option['name']
                criterion_phrases = []
                
                for mc in matching_criteria:
                    value_str = str(mc['value'])
                    criterion_name = mc['name'].lower()
                    phrase = f"{value_str} {criterion_name}"
                    criterion_phrases.append(phrase)
                
                if len(criterion_phrases) == 1:
                    reasoning_text = f"'{option_name}' is the best option due to its {criterion_phrases[0]}."
                elif len(criterion_phrases) == 2:
                    reasoning_text = f"'{option_name}' is the best option due to its {criterion_phrases[0]} and {criterion_phrases[1]}."
                else:
                    all_but_last = ", ".join(criterion_phrases[:-1])
                    reasoning_text = f"'{option_name}' is the best option due to its {all_but_last}, and {criterion_phrases[-1]}."
            else:
                reasoning_text = f"'{top_option['name']}' is the best overall option based on the weighted combination of all criteria."
        
        # Prepare response
        response = {
            'success': True,
            'goal': decision_goal,
            'criteria': [
                {
                    'name': c['name'],
                    'type': c['type'],
                    'weight': round(c['weight'] * 100, 2)
                }
                for c in criteria
            ],
            'results': [
                {
                    'rank': i + 1,
                    'name': r['name'],
                    'score': round(r['score'] * 100, 2)
                }
                for i, r in enumerate(results)
            ],
            'reasoning': reasoning_text,
            'matching_criteria': [
                {
                    'name': mc['name'],
                    'value': mc['value']
                }
                for mc in matching_criteria
            ]
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)