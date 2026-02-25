# # #!/usr/bin/env python3
# # """
# # Decision Companion System - Priority-Based (User-Friendly Version)
# # Users just rank criteria by priority, weights auto-assigned
# # """

# # import math


# # def get_float(prompt):
# #     """Get float input with error handling"""
# #     while True:
# #         try:
# #             return float(input(prompt))
# #         except ValueError:
# #             print("Please enter a valid number")


# # def get_int(prompt):
# #     """Get integer input with error handling"""
# #     while True:
# #         try:
# #             return int(input(prompt))
# #         except ValueError:
# #             print("Please enter a valid integer")


# # def calculate_priority_weights(num_criteria):
# #     """
# #     Calculate weights based on priority order using halving logic
    
# #     Priority 1: Gets 50% of remaining
# #     Priority 2: Gets 50% of what's left (25% of total)
# #     Priority 3: Gets 50% of what's left (12.5% of total)
# #     etc.
    
# #     Then normalize so they sum to 1.0
# #     """
# #     raw_weights = []
    
# #     for i in range(num_criteria):
# #         # Each priority gets half of previous
# #         raw_weight = 0.5 ** (i + 1)
# #         raw_weights.append(raw_weight)
    
# #     # Normalize to sum to 1.0
# #     total = sum(raw_weights)
# #     normalized_weights = [w / total for w in raw_weights]
    
# #     return normalized_weights


# # def normalize_matrix(options, criteria):
# #     """Normalize values using vector normalization"""
# #     normalized = {}
    
# #     for criterion_name in criteria.keys():
# #         sum_of_squares = sum(opt['values'][criterion_name] ** 2 for opt in options)
# #         denominator = math.sqrt(sum_of_squares)
        
# #         for option in options:
# #             if option['name'] not in normalized:
# #                 normalized[option['name']] = {}
            
# #             normalized[option['name']][criterion_name] = (
# #                 option['values'][criterion_name] / denominator if denominator != 0 else 0
# #             )
    
# #     return normalized


# # def apply_weights(normalized, criteria):
# #     """Apply weights to normalized values"""
# #     weighted = {}
    
# #     for option_name, criterion_values in normalized.items():
# #         weighted[option_name] = {}
# #         for criterion_name, criterion_data in criteria.items():
# #             weighted[option_name][criterion_name] = (
# #                 criterion_values[criterion_name] * criterion_data['weight']
# #             )
    
# #     return weighted


# # def find_ideal_solutions(weighted, criteria, options):
# #     """Find ideal best and worst solutions"""
# #     ideal_best = {}
# #     ideal_worst = {}
    
# #     for criterion_name, criterion_data in criteria.items():
# #         values = [weighted[opt['name']][criterion_name] for opt in options]
        
# #         if criterion_data['type'] == 'benefit':
# #             ideal_best[criterion_name] = max(values)
# #             ideal_worst[criterion_name] = min(values)
# #         else:  # cost
# #             ideal_best[criterion_name] = min(values)
# #             ideal_worst[criterion_name] = max(values)
    
# #     return ideal_best, ideal_worst


# # def calculate_distances(weighted, ideal_best, ideal_worst, options, criteria):
# #     """Calculate Euclidean distance from ideal solutions"""
# #     distances = {}
    
# #     for option in options:
# #         option_name = option['name']
        
# #         dist_best = math.sqrt(sum(
# #             (weighted[option_name][crit_name] - ideal_best[crit_name]) ** 2
# #             for crit_name in criteria.keys()
# #         ))
        
# #         dist_worst = math.sqrt(sum(
# #             (weighted[option_name][crit_name] - ideal_worst[crit_name]) ** 2
# #             for crit_name in criteria.keys()
# #         ))
        
# #         distances[option_name] = (dist_best, dist_worst)
    
# #     return distances


# # def calculate_scores(distances):
# #     """Calculate relative closeness scores"""
# #     scores = {}
    
# #     for option_name, (dist_best, dist_worst) in distances.items():
# #         denominator = dist_best + dist_worst
# #         scores[option_name] = dist_worst / denominator if denominator != 0 else 0
    
# #     return scores


# # def analyze_decision(options, criteria):
# #     """Run complete TOPSIS analysis"""
# #     normalized = normalize_matrix(options, criteria)
# #     weighted = apply_weights(normalized, criteria)
# #     ideal_best, ideal_worst = find_ideal_solutions(weighted, criteria, options)
# #     distances = calculate_distances(weighted, ideal_best, ideal_worst, options, criteria)
# #     scores = calculate_scores(distances)
    
# #     ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
# #     return ranked, scores


# # def print_results(ranked, scores, options, criteria):
# #     """Print analysis results"""
# #     print("\n" + "="*70)
# #     print("DECISION ANALYSIS RESULTS")
# #     print("="*70)
    
# #     best_name = ranked[0][0]
# #     best_score = ranked[0][1]
    
# #     print(f"\n🏆 RECOMMENDED OPTION: {best_name}")
# #     print(f"   Score: {best_score:.4f} ({best_score*100:.2f}%)")
    
# #     best_option = next(opt for opt in options if opt['name'] == best_name)
    
# #     print(f"\n{'─'*70}")
# #     print("WHY THIS OPTION:")
# #     print(f"{'─'*70}")
    
# #     # Show criteria in priority order (as entered by user)
# #     criterion_list = list(criteria.items())
    
# #     for i, (crit_name, crit_data) in enumerate(criterion_list, 1):
# #         value = best_option['values'][crit_name]
# #         weight_pct = crit_data['weight'] * 100
# #         type_str = "↑ Higher is better" if crit_data['type'] == 'benefit' else "↓ Lower is better"
        
# #         all_values = [opt['values'][crit_name] for opt in options]
# #         if crit_data['type'] == 'benefit':
# #             sorted_values = sorted(all_values, reverse=True)
# #         else:
# #             sorted_values = sorted(all_values)
# #         rank = sorted_values.index(value) + 1
        
# #         print(f"\n• Priority #{i}: {crit_name} (Auto-weight: {weight_pct:.1f}%, {type_str})")
# #         print(f"  Value: {value:.2f} | Rank: #{rank} of {len(options)}")
    
# #     print(f"\n{'─'*70}")
# #     print("COMPLETE RANKING:")
# #     print(f"{'─'*70}\n")
    
# #     for i, (name, score) in enumerate(ranked, 1):
# #         print(f"{i}. {name:<30} Score: {score:.4f} ({score*100:.2f}%)")
    
# #     print("\n" + "="*70 + "\n")


# # def main():
# #     """Main execution"""
# #     print("\n" + "="*70)
# #     print("DECISION COMPANION SYSTEM")
# #     print("="*70)
# #     print("\n✨ Simple Priority-Based Decision Making")
# #     print("   Just rank what matters most to you - we handle the rest!")
    
# #     decision = input("\n📋 What decision are you making?\n> ").strip()
    
# #     # Get options
# #     print(f"\n{'='*70}")
# #     print("STEP 1: DEFINE OPTIONS")
# #     print("="*70)
# #     num_options = get_int("\nHow many options to compare? ")
    
# #     options = []
# #     for i in range(num_options):
# #         name = input(f"Option {i+1} name: ").strip()
# #         options.append({'name': name, 'values': {}})
    
# #     # Get criteria IN PRIORITY ORDER
# #     print(f"\n{'='*70}")
# #     print("STEP 2: DEFINE CRITERIA (In Priority Order)")
# #     print("="*70)
# #     print("\n⭐ IMPORTANT: Enter criteria from MOST to LEAST important")
# #     print("   Example: 1st = Performance, 2nd = Price, 3rd = Battery")
# #     print("\n💡 Weights will be assigned automatically:")
# #     print("   Priority 1 gets 50% importance")
# #     print("   Priority 2 gets 25% importance")
# #     print("   Priority 3 gets 12.5% importance")
# #     print("   And so on...\n")
    
# #     num_criteria = get_int("How many criteria? ")
    
# #     # Calculate weights automatically
# #     weights = calculate_priority_weights(num_criteria)
    
# #     criteria = {}
    
# #     print("\n" + "─"*70)
# #     for i in range(num_criteria):
# #         print(f"\n--- Priority #{i+1} Criterion (Auto-weight: {weights[i]*100:.1f}%) ---")
# #         name = input("Name: ").strip()
        
# #         print("Type: 1 = Benefit (higher is better), 2 = Cost (lower is better)")
# #         type_choice = input("Choose (1/2): ").strip()
# #         crit_type = 'benefit' if type_choice == '1' else 'cost'
        
# #         criteria[name] = {
# #             'weight': weights[i],
# #             'type': crit_type,
# #             'priority': i + 1
# #         }
    
# #     # Show assigned weights
# #     print(f"\n{'─'*70}")
# #     print("📊 AUTO-ASSIGNED WEIGHTS:")
# #     print(f"{'─'*70}")
# #     total_check = 0
# #     for crit_name, crit_data in criteria.items():
# #         print(f"  • {crit_name:<25} {crit_data['weight']*100:>6.2f}% (Priority #{crit_data['priority']})")
# #         total_check += crit_data['weight']
# #     print(f"{'─'*70}")
# #     print(f"  {'Total:':<25} {total_check*100:>6.2f}%")
    
# #     # Get values for each option
# #     print(f"\n{'='*70}")
# #     print("STEP 3: ENTER VALUES")
# #     print("="*70)
# #     print("\nEnter the value for each option on each criterion\n")
    
# #     for option in options:
# #         print(f"--- {option['name']} ---")
# #         for crit_name in criteria.keys():
# #             value = get_float(f"  {crit_name}: ")
# #             option['values'][crit_name] = value
# #         print()
    
# #     # Analyze
# #     print("="*70)
# #     print("ANALYZING...")
# #     print("="*70)
    
# #     ranked, scores = analyze_decision(options, criteria)
    
# #     # Display results
# #     print_results(ranked, scores, options, criteria)
    
# #     print("Thank you for using Decision Companion System!\n")


# # if __name__ == "__main__":
# #     try:
# #         main()
# #     except KeyboardInterrupt:
# #         print("\n\n❌ Cancelled by user\n")
# #     except Exception as e:
# #         print(f"\n\n❌ Error: {e}\n")

#weights using roc
# #!/usr/bin/env python3
# # import math

# # class DecisionEngine:
# #     def __init__(self):
# #         self.qualitative_map = {
# #             "very low": 1, "low": 3, "medium": 5, 
# #             "high": 7, "very high": 9
# #         }

# #     def calculate_roc_weights(self, num_criteria):
# #         """Calculates weights based on priority rank using ROC."""
# #         weights = []
# #         for i in range(1, num_criteria + 1):
# #             weight = sum(1.0 / j for j in range(i, num_criteria + 1)) / num_criteria
# #             weights.append(weight)
# #         return weights

# #     def _to_float(self, value):
# #         if isinstance(value, str):
# #             val = value.lower().strip()
# #             return float(self.qualitative_map.get(val, 5))
# #         try:
# #             return float(value)
# #         except (ValueError, TypeError):
# #             return 0.0

# #     def run_topsis(self, options, criteria):
# #         if not options or not criteria:
# #             return {"error": "Insufficient data"}

# #         # 1. Normalization
# #         norm_matrix = {}
# #         for crit in criteria:
# #             c_id = crit['id']
# #             sq_sum = sum(self._to_float(opt['values'].get(c_id, 0))**2 for opt in options)
# #             denominator = math.sqrt(sq_sum)
            
# #             for opt in options:
# #                 name = opt['name']
# #                 if name not in norm_matrix: norm_matrix[name] = {}
# #                 val = self._to_float(opt['values'].get(c_id, 0))
# #                 norm_matrix[name][c_id] = (val / denominator) if denominator != 0 else 0

# #         # 2. Weighted Matrix
# #         weighted_matrix = {}
# #         for opt_name, scores in norm_matrix.items():
# #             weighted_matrix[opt_name] = {
# #                 c_id: scores[c_id] * next(c['weight'] for c in criteria if c['id'] == c_id)
# #                 for c_id in scores
# #             }

# #         # 3. Ideal Solutions
# #         ideal_best, ideal_worst = {}, {}
# #         for crit in criteria:
# #             c_id = crit['id']
# #             v_list = [weighted_matrix[opt['name']][c_id] for opt in options]
# #             if crit['type'] == 'benefit':
# #                 ideal_best[c_id], ideal_worst[c_id] = max(v_list), min(v_list)
# #             else:
# #                 ideal_best[c_id], ideal_worst[c_id] = min(v_list), max(v_list)

# #         # 4. Scoring
# #         results = []
# #         for opt in options:
# #             name = opt['name']
# #             d_best = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_best[c['id']])**2 for c in criteria))
# #             d_worst = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_worst[c['id']])**2 for c in criteria))
            
# #             total_dist = d_best + d_worst
# #             performance_score = (d_worst / total_dist) if total_dist != 0 else 0.5
            
# #             results.append({"name": name, "score": round(performance_score, 4)})

# #         return sorted(results, key=lambda x: x['score'], reverse=True)

# # def get_input(prompt, type_=str):
# #     while True:
# #         try:
# #             val = input(prompt).strip()
# #             if not val: continue
# #             return type_(val)
# #         except ValueError:
# #             print(f"Invalid input. Please enter a {type_.__name__}.")

# # def main():
# #     engine = DecisionEngine()
# #     print("\n--- DECISION COMPANION SYSTEM ---")
# #     goal = input("What are you deciding? (e.g., Best Laptop): ")

# #     # 1. Gather Criteria
# #     print("\nSTEP 1: Define Criteria (Ranked from Most Important to Least)")
# #     num_crit = get_input("How many criteria? ", int)
# #     criteria = []
# #     for i in range(num_crit):
# #         print(f"\nPriority #{i+1}:")
# #         name = get_input("  Name (e.g., Price): ")
# #         c_type = get_input("  Type (1 for Benefit/Higher is better, 2 for Cost/Lower is better): ")
# #         criteria.append({
# #             "id": f"c{i}", 
# #             "name": name, 
# #             "type": "benefit" if c_type == "1" else "cost"
# #         })

# #     # Auto-assign ROC weights
# #     weights = engine.calculate_roc_weights(num_crit)
# #     for i, crit in enumerate(criteria):
# #         crit['weight'] = weights[i]

# #     # 2. Gather Options
# #     print("\nSTEP 2: Define Options")
# #     num_opts = get_input("How many options to compare? ", int)
# #     options = []
# #     for i in range(num_opts):
# #         opt_name = get_input(f"  Name for Option {i+1}: ")
# #         opt_values = {}
# #         print(f"  Enter values for {opt_name} (use numbers or 'High', 'Medium', 'Low'):")
# #         for crit in criteria:
# #             val = get_input(f"    {crit['name']}: ")
# #             opt_values[crit['id']] = val
# #         options.append({"name": opt_name, "values": opt_values})

# #     # 3. Calculate and Display
# #     print("\n--- RESULTS ---")
# #     results = engine.run_topsis(options, criteria)
    
# #     for i, res in enumerate(results, 1):
# #         status = "🏆 RECOMMENDED" if i == 1 else f"Rank {i}"
# #         print(f"{status}: {res['name']} (Match Score: {res['score']*100:.2f}%)")

# # if __name__ == "__main__":
# #     main()

# mentions why option is selected
# import math

# class DecisionEngine:
#     def __init__(self):
#         self.qualitative_map = {
#             "very low": 1, "low": 3, "medium": 5, 
#             "high": 7, "very high": 9
#         }

#     def calculate_roc_weights(self, num_criteria):
#         """Calculates weights based on priority rank using ROC."""
#         weights = []
#         for i in range(1, num_criteria + 1):
#             weight = sum(1.0 / j for j in range(i, num_criteria + 1)) / num_criteria
#             weights.append(weight)
#         return weights

#     def _to_float(self, value):
#         if isinstance(value, str):
#             val = value.lower().strip()
#             return float(self.qualitative_map.get(val, 5))
#         try:
#             return float(value)
#         except (ValueError, TypeError):
#             return 0.0

#     def run_topsis(self, options, criteria):
#         if not options or not criteria:
#             return {"error": "Insufficient data"}

#         # 1. Normalization
#         norm_matrix = {}
#         for crit in criteria:
#             c_id = crit['id']
#             sq_sum = sum(self._to_float(opt['values'].get(c_id, 0))**2 for opt in options)
#             denominator = math.sqrt(sq_sum)
            
#             for opt in options:
#                 name = opt['name']
#                 if name not in norm_matrix: norm_matrix[name] = {}
#                 val = self._to_float(opt['values'].get(c_id, 0))
#                 norm_matrix[name][c_id] = (val / denominator) if denominator != 0 else 0

#         # 2. Weighted Matrix
#         weighted_matrix = {}
#         for opt_name, scores in norm_matrix.items():
#             weighted_matrix[opt_name] = {
#                 c_id: scores[c_id] * next(c['weight'] for c in criteria if c['id'] == c_id)
#                 for c_id in scores
#             }

#         # 3. Ideal Solutions
#         ideal_best, ideal_worst = {}, {}
        
#         for crit in criteria:
#             c_id = crit['id']
#             v_list = [weighted_matrix[opt['name']][c_id] for opt in options]
            
#             if crit['type'] == 'benefit':
#                 ideal_best[c_id] = max(v_list)
#                 ideal_worst[c_id] = min(v_list)
#             else:
#                 ideal_best[c_id] = min(v_list)
#                 ideal_worst[c_id] = max(v_list)

#         # 4. Scoring
#         results = []
#         for opt in options:
#             name = opt['name']
#             d_best = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_best[c['id']])**2 for c in criteria))
#             d_worst = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_worst[c['id']])**2 for c in criteria))
            
#             total_dist = d_best + d_worst
#             performance_score = (d_worst / total_dist) if total_dist != 0 else 0.5
            
#             results.append({
#                 "name": name,
#                 "score": round(performance_score, 4),
#                 "weighted_values": weighted_matrix[name],
#                 "original_values": opt['values']  # Keep original user inputs
#             })

#         # Sort by score
#         results = sorted(results, key=lambda x: x['score'], reverse=True)
        
#         return results, ideal_best, weighted_matrix, criteria

#     def generate_reasoning(self, top_option, ideal_best, weighted_matrix, criteria, all_options):
#         """Generate reasoning statement with original user values"""
#         matching_criteria = []
#         threshold = 0.05  # Within 5% considered matching
        
#         for crit in criteria:
#             c_id = crit['id']
#             option_weighted = top_option['weighted_values'][c_id]
#             ideal_value = ideal_best[c_id]
            
#             # Check if this option matches ideal
#             if ideal_value != 0:
#                 diff_pct = abs(option_weighted - ideal_value) / abs(ideal_value)
#             else:
#                 diff_pct = abs(option_weighted - ideal_value)
            
#             if diff_pct <= threshold:
#                 # This criterion matches ideal - get the original user input
#                 original_input = top_option['original_values'][c_id]
                
#                 matching_criteria.append({
#                     'name': crit['name'],
#                     'value': original_input,  # The actual value user entered
#                     'type': crit['type'],
#                     'weight': crit['weight']
#                 })
        
#         # Sort by weight (most important first)
#         matching_criteria.sort(key=lambda x: x['weight'], reverse=True)
        
#         return matching_criteria

# def get_input(prompt, type_=str):
#     while True:
#         try:
#             val = input(prompt).strip()
#             if not val: continue
#             return type_(val)
#         except ValueError:
#             print(f"Invalid input. Please enter a {type_.__name__}.")

# def main():
#     engine = DecisionEngine()
#     print("\n" + "="*70)
#     print("DECISION COMPANION SYSTEM")
#     print("="*70)
#     goal = input("\nWhat are you deciding? (e.g., Best Laptop): ")

#     # 1. Gather Criteria
#     print("\n" + "="*70)
#     print("STEP 1: Define Criteria (Ranked from Most Important to Least)")
#     print("="*70)
#     num_crit = get_input("How many criteria? ", int)
#     criteria = []
#     for i in range(num_crit):
#         print(f"\nPriority #{i+1}:")
#         name = get_input("  Name (e.g., Price, Processor, Cost): ")
#         c_type = get_input("  Type (1 for Benefit/Higher is better, 2 for Cost/Lower is better): ")
#         criteria.append({
#             "id": f"c{i}", 
#             "name": name, 
#             "type": "benefit" if c_type == "1" else "cost"
#         })

#     # Auto-assign ROC weights
#     weights = engine.calculate_roc_weights(num_crit)
#     for i, crit in enumerate(criteria):
#         crit['weight'] = weights[i]

#     print("\n" + "-"*70)
#     print("AUTO-ASSIGNED WEIGHTS (Based on Priority):")
#     print("-"*70)
#     for i, crit in enumerate(criteria):
#         print(f"  Priority #{i+1}: {crit['name']:<20} {crit['weight']*100:>6.2f}%")

#     # 2. Gather Options
#     print("\n" + "="*70)
#     print("STEP 2: Define Options")
#     print("="*70)
#     num_opts = get_input("How many options to compare? ", int)
#     options = []
#     for i in range(num_opts):
#         opt_name = get_input(f"\nName for Option {i+1}: ")
#         opt_values = {}
#         print(f"Enter values for '{opt_name}' (use numbers or 'High', 'Medium', 'Low'):")
#         for crit in criteria:
#             val = get_input(f"  {crit['name']}: ")
#             opt_values[crit['id']] = val
#         options.append({"name": opt_name, "values": opt_values})

#     # 3. Calculate and Display
#     print("\n" + "="*70)
#     print("ANALYZING...")
#     print("="*70)
    
#     results, ideal_best, weighted_matrix, criteria_list = engine.run_topsis(options, criteria)
    
#     # Show ranking
#     print("\n" + "="*70)
#     print("RESULTS:")
#     print("="*70)
#     for i, res in enumerate(results, 1):
#         if i == 1:
#             print(f"🏆 {res['name']:<30} Score: {res['score']*100:>6.2f}%")
#         else:
#             print(f"{i}.  {res['name']:<30} Score: {res['score']*100:>6.2f}%")
    
#     # Generate and show reasoning
#     if results:
#         top_option = results[0]
#         matching_criteria = engine.generate_reasoning(
#             top_option, ideal_best, weighted_matrix, criteria_list, results
#         )
        
#         print("\n" + "="*70)
#         print("WHY THIS OPTION WON:")
#         print("="*70)
        
#         if matching_criteria:
#             # Build the statement
#             option_name = top_option['name']
            
#             # Create pairs of "adjective + criterion"
#             criterion_phrases = []
#             for mc in matching_criteria:
#                 value_str = str(mc['value'])
#                 criterion_name = mc['name'].lower()
                
#                 # Build the phrase
#                 phrase = f"{value_str} {criterion_name}"
#                 criterion_phrases.append(phrase)
            
#             # Format the statement
#             if len(criterion_phrases) == 1:
#                 statement = f"'{option_name}' is the best option due to its {criterion_phrases[0]}."
#             elif len(criterion_phrases) == 2:
#                 statement = f"'{option_name}' is the best option due to its {criterion_phrases[0]} and {criterion_phrases[1]}."
#             else:
#                 # Three or more criteria
#                 all_but_last = ", ".join(criterion_phrases[:-1])
#                 statement = f"'{option_name}' is the best option due to its {all_but_last}, and {criterion_phrases[-1]}."
            
#             print(f"\n{statement}")
#             print("\nThese criteria match or are very close to the ideal solution.")
            
#         else:
#             print(f"\n'{top_option['name']}' is the best overall option based on")
#             print("the weighted combination of all criteria.")
    
#     print("\n" + "="*70)
#     print("Thank you for using Decision Companion System!")
#     print("="*70 + "\n")

# if __name__ == "__main__":
#     main()

#future change in criteria monte carlo approach
#!/usr/bin/env python3
import math
import random
import copy


class DecisionEngine:
    def __init__(self):
        self.qualitative_map = {
            "very low": 1, "low": 3, "medium": 5, "high": 7, "very high": 9
        }

    def calculate_roc_weights(self, num_criteria):
        weights = []
        for i in range(1, num_criteria + 1):
            weight = sum(1.0 / j for j in range(i, num_criteria + 1)) / num_criteria
            weights.append(weight)
        return weights

    def _to_float(self, value):
        if value is None: return 5.0
        if isinstance(value, str):
            # Try numeric first, then qualitative label
            try:
                return float(value.strip())
            except ValueError:
                return float(self.qualitative_map.get(value.lower().strip(), 5.0))
        return float(value)

    def run_topsis(self, options, criteria):
        # Normalise + weight
        norm_matrix = {}
        for crit in criteria:
            c_id = crit['id']
            sq_sum = sum(opt['values'][c_id] ** 2 for opt in options)
            denominator = math.sqrt(sq_sum) if sq_sum > 0 else 1
            for opt in options:
                norm_matrix.setdefault(opt['name'], {})
                norm_matrix[opt['name']][c_id] = (opt['values'][c_id] / denominator) * crit['weight']

        # Ideal best and worst
        ideal_best, ideal_worst = {}, {}
        for crit in criteria:
            c_id = crit['id']
            vals = [norm_matrix[o['name']][c_id] for o in options]
            if crit['type'] == 'benefit':
                ideal_best[c_id], ideal_worst[c_id] = max(vals), min(vals)
            else:
                ideal_best[c_id], ideal_worst[c_id] = min(vals), max(vals)

        # Score
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

        # BUG 3 FIX: build float_options as a NEW list, never mutate the passed-in options
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
        """
        BUG 1 FIX: Run TOPSIS exactly ONCE and build explanations for ALL options
        from that single pass. Previously explain_winner was called N+1 times.

        BUG 2 FIX: ideal shown to user is the best raw value on the 1-9 scale,
        not the internal normalised TOPSIS number which is meaningless to users.
        """
        results, ideal_best, ideal_worst, norm_matrix = self.run_topsis(options, criteria)

        # Build ideal in original scale (best actual value per criterion across all options)
        ideal_raw = {}
        for crit in criteria:
            c_id = crit['id']
            raw_vals = [opt['values'][c_id] for opt in options]
            if crit['type'] == 'benefit':
                ideal_raw[c_id] = max(raw_vals)   # best = highest
            else:
                ideal_raw[c_id] = min(raw_vals)   # best = lowest

        all_explanations = {}

        for opt in options:
            opt_name = opt['name']
            opt_norm = norm_matrix[opt_name]
            explanation = []

            for crit in criteria:
                c_id       = crit['id']
                actual     = opt['values'][c_id]
                ib         = ideal_best[c_id]
                iw         = ideal_worst[c_id]
                wv         = opt_norm[c_id]
                ideal_range = abs(ib - iw)

                gap_pct = abs(wv - ib) / ideal_range * 100 if ideal_range > 0 else 0.0

                all_vals = [norm_matrix[o['name']][c_id] for o in options]
                is_best  = (wv == max(all_vals) if crit['type'] == 'benefit' else wv == min(all_vals))

                explanation.append({
                    "name":      crit['name'],
                    "actual":    actual,
                    "ideal_raw": ideal_raw[c_id],   # BUG 2 FIX: real scale value
                    "gap_pct":   round(gap_pct, 1),
                    "is_best":   is_best,
                    "type":      crit['type'],
                    "weight":    crit['weight'],
                })

            explanation.sort(key=lambda x: x['gap_pct'])
            all_explanations[opt_name] = explanation

        return all_explanations


# ── Input Helpers ─────────────────────────────────────────────────────────────

def get_input(prompt, type_=str):
    while True:
        try:
            val = input(prompt).strip()
            if not val:
                continue
            return type_(val)
        except ValueError:
            print(f"  ⚠  Please enter a valid {type_.__name__}.")

def get_criterion_type(prompt):
    # BUG 4 FIX: only accept exactly "1" or "2", loop until valid
    while True:
        val = input(prompt).strip()
        if val == "1": return "benefit"
        if val == "2": return "cost"
        print("  ⚠  Please enter 1 or 2.")


# ── Main ──────────────────────────────────────────────────────────────────────

def interactive_cli():
    engine = DecisionEngine()
    print("\n" + "=" * 60)
    print("  DECISION COMPANION SYSTEM")
    print("=" * 60)

    decision_goal = input("\nWhat decision are you making? ")

    # 1. Criteria
    print("\n" + "-" * 60)
    print("  CRITERIA  (most → least important)")
    print("-" * 60)
    num_crit = get_input("\nHow many criteria? ", int)
    criteria_list = []

    for i in range(num_crit):
        print(f"\n  Criterion #{i+1}:")
        name       = get_input("    Name: ")
        c_type     = get_criterion_type("    Type  1=Benefit (↑ better)  2=Cost (↓ better): ")
        is_dynamic = input("    Dynamic/uncertain? (y/n): ").lower().strip() == 'y'
        criteria_list.append({
            "id":      f"c{i}",
            "name":    name,
            "type":    c_type,
            "dynamic": is_dynamic
        })

    weights = engine.calculate_roc_weights(num_crit)
    for i, c in enumerate(criteria_list):
        c['weight'] = weights[i]

    print("\n  Weights assigned:")
    for c in criteria_list:
        tag = "  🔄 dynamic" if c['dynamic'] else ""
        print(f"    {c['name']:<24} {c['weight']*100:.2f}%{tag}")

    # 2. Options
    print("\n" + "-" * 60)
    print("  OPTIONS")
    print("  Use numbers (1-9) or: Very Low / Low / Medium / High / Very High")
    print("-" * 60)
    num_opts = get_input("\nHow many options? ", int)
    options_list = []

    for j in range(num_opts):
        opt_name = get_input(f"\n  Option {j+1} name: ")
        opt_values = {}
        for c in criteria_list:
            val = get_input(f"    {c['name']}: ")
            opt_values[c['id']] = val
        options_list.append({"name": opt_name, "values": opt_values})

    # 3. Convert to floats then deepcopy BEFORE simulation
    for opt in options_list:
        opt['values'] = {c['id']: engine._to_float(opt['values'].get(c['id'])) for c in criteria_list}
    original_options = copy.deepcopy(options_list)

    # 4. Simulate
    print(f"\n  Simulating 1,000 futures for: {decision_goal}...")
    results = engine.simulate_decision(options_list, criteria_list)

    # 5. Results
    print("\n" + "=" * 60)
    print("  SIMULATION RESULTS")
    print("=" * 60)
    for r in results:
        bar  = "█" * int(r['confidence'] / 2)
        star = "🏆" if r == results[0] else "  "
        print(f"  {star} {r['name']:<20} {r['confidence']:>6.2f}%  {bar}")

    # 6. Why it won + full breakdown — BUG 1 FIX: single TOPSIS call for everything
    winner = results[0]['name']
    all_explanations = engine.explain_all(original_options, criteria_list)
    winner_explanation = all_explanations[winner]

    print("\n" + "=" * 60)
    print(f"  WHY '{winner}' WON")
    print("=" * 60)
    print("  Comparing winner's values against the ideal case:\n")

    # Single sentence using best criterion (smallest gap, highest weight as tiebreak)
    best = min(winner_explanation, key=lambda e: (e['gap_pct'], -e['weight']))
    print(f"  '{winner}' is selected due to its {best['name']} "
          f"(value={best['actual']:.1f}) being closest to the ideal "
          f"(ideal={best['ideal_raw']:.1f}, gap={best['gap_pct']:.1f}%).")

    # Full breakdown for all options
    print("\n" + "=" * 60)
    print("  OPTION BREAKDOWN")
    print("=" * 60)

    for opt in original_options:
        opt_name   = opt['name']
        expl       = all_explanations[opt_name]
        strengths  = [e for e in expl if e['gap_pct'] <= 40]
        weaknesses = [e for e in expl if e['gap_pct'] >  40]

        rank       = next(i+1 for i, r in enumerate(results) if r['name'] == opt_name)
        confidence = next(r['confidence'] for r in results if r['name'] == opt_name)
        marker     = "🏆" if rank == 1 else f"#{rank}"

        print(f"\n  {marker} {opt_name}  ({confidence:.1f}% confidence)")
        print(f"  {'─' * 40}")

        if strengths:
            print("    Strengths:")
            for e in strengths:
                print(f"      ✅ {e['name']:<20} value={e['actual']:.1f}  "
                      f"ideal={e['ideal_raw']:.1f}  gap={e['gap_pct']:.1f}%")

        if weaknesses:
            print("    Weaknesses:")
            for e in weaknesses:
                print(f"      ❌ {e['name']:<20} value={e['actual']:.1f}  "
                      f"ideal={e['ideal_raw']:.1f}  gap={e['gap_pct']:.1f}%")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        interactive_cli()
    except KeyboardInterrupt:
        print("\n\n  Cancelled.\n")