# #!/usr/bin/env python3
# """
# Decision Companion System - Priority-Based (User-Friendly Version)
# Users just rank criteria by priority, weights auto-assigned
# """

# import math


# def get_float(prompt):
#     """Get float input with error handling"""
#     while True:
#         try:
#             return float(input(prompt))
#         except ValueError:
#             print("Please enter a valid number")


# def get_int(prompt):
#     """Get integer input with error handling"""
#     while True:
#         try:
#             return int(input(prompt))
#         except ValueError:
#             print("Please enter a valid integer")


# def calculate_priority_weights(num_criteria):
#     """
#     Calculate weights based on priority order using halving logic
    
#     Priority 1: Gets 50% of remaining
#     Priority 2: Gets 50% of what's left (25% of total)
#     Priority 3: Gets 50% of what's left (12.5% of total)
#     etc.
    
#     Then normalize so they sum to 1.0
#     """
#     raw_weights = []
    
#     for i in range(num_criteria):
#         # Each priority gets half of previous
#         raw_weight = 0.5 ** (i + 1)
#         raw_weights.append(raw_weight)
    
#     # Normalize to sum to 1.0
#     total = sum(raw_weights)
#     normalized_weights = [w / total for w in raw_weights]
    
#     return normalized_weights


# def normalize_matrix(options, criteria):
#     """Normalize values using vector normalization"""
#     normalized = {}
    
#     for criterion_name in criteria.keys():
#         sum_of_squares = sum(opt['values'][criterion_name] ** 2 for opt in options)
#         denominator = math.sqrt(sum_of_squares)
        
#         for option in options:
#             if option['name'] not in normalized:
#                 normalized[option['name']] = {}
            
#             normalized[option['name']][criterion_name] = (
#                 option['values'][criterion_name] / denominator if denominator != 0 else 0
#             )
    
#     return normalized


# def apply_weights(normalized, criteria):
#     """Apply weights to normalized values"""
#     weighted = {}
    
#     for option_name, criterion_values in normalized.items():
#         weighted[option_name] = {}
#         for criterion_name, criterion_data in criteria.items():
#             weighted[option_name][criterion_name] = (
#                 criterion_values[criterion_name] * criterion_data['weight']
#             )
    
#     return weighted


# def find_ideal_solutions(weighted, criteria, options):
#     """Find ideal best and worst solutions"""
#     ideal_best = {}
#     ideal_worst = {}
    
#     for criterion_name, criterion_data in criteria.items():
#         values = [weighted[opt['name']][criterion_name] for opt in options]
        
#         if criterion_data['type'] == 'benefit':
#             ideal_best[criterion_name] = max(values)
#             ideal_worst[criterion_name] = min(values)
#         else:  # cost
#             ideal_best[criterion_name] = min(values)
#             ideal_worst[criterion_name] = max(values)
    
#     return ideal_best, ideal_worst


# def calculate_distances(weighted, ideal_best, ideal_worst, options, criteria):
#     """Calculate Euclidean distance from ideal solutions"""
#     distances = {}
    
#     for option in options:
#         option_name = option['name']
        
#         dist_best = math.sqrt(sum(
#             (weighted[option_name][crit_name] - ideal_best[crit_name]) ** 2
#             for crit_name in criteria.keys()
#         ))
        
#         dist_worst = math.sqrt(sum(
#             (weighted[option_name][crit_name] - ideal_worst[crit_name]) ** 2
#             for crit_name in criteria.keys()
#         ))
        
#         distances[option_name] = (dist_best, dist_worst)
    
#     return distances


# def calculate_scores(distances):
#     """Calculate relative closeness scores"""
#     scores = {}
    
#     for option_name, (dist_best, dist_worst) in distances.items():
#         denominator = dist_best + dist_worst
#         scores[option_name] = dist_worst / denominator if denominator != 0 else 0
    
#     return scores


# def analyze_decision(options, criteria):
#     """Run complete TOPSIS analysis"""
#     normalized = normalize_matrix(options, criteria)
#     weighted = apply_weights(normalized, criteria)
#     ideal_best, ideal_worst = find_ideal_solutions(weighted, criteria, options)
#     distances = calculate_distances(weighted, ideal_best, ideal_worst, options, criteria)
#     scores = calculate_scores(distances)
    
#     ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
#     return ranked, scores


# def print_results(ranked, scores, options, criteria):
#     """Print analysis results"""
#     print("\n" + "="*70)
#     print("DECISION ANALYSIS RESULTS")
#     print("="*70)
    
#     best_name = ranked[0][0]
#     best_score = ranked[0][1]
    
#     print(f"\n🏆 RECOMMENDED OPTION: {best_name}")
#     print(f"   Score: {best_score:.4f} ({best_score*100:.2f}%)")
    
#     best_option = next(opt for opt in options if opt['name'] == best_name)
    
#     print(f"\n{'─'*70}")
#     print("WHY THIS OPTION:")
#     print(f"{'─'*70}")
    
#     # Show criteria in priority order (as entered by user)
#     criterion_list = list(criteria.items())
    
#     for i, (crit_name, crit_data) in enumerate(criterion_list, 1):
#         value = best_option['values'][crit_name]
#         weight_pct = crit_data['weight'] * 100
#         type_str = "↑ Higher is better" if crit_data['type'] == 'benefit' else "↓ Lower is better"
        
#         all_values = [opt['values'][crit_name] for opt in options]
#         if crit_data['type'] == 'benefit':
#             sorted_values = sorted(all_values, reverse=True)
#         else:
#             sorted_values = sorted(all_values)
#         rank = sorted_values.index(value) + 1
        
#         print(f"\n• Priority #{i}: {crit_name} (Auto-weight: {weight_pct:.1f}%, {type_str})")
#         print(f"  Value: {value:.2f} | Rank: #{rank} of {len(options)}")
    
#     print(f"\n{'─'*70}")
#     print("COMPLETE RANKING:")
#     print(f"{'─'*70}\n")
    
#     for i, (name, score) in enumerate(ranked, 1):
#         print(f"{i}. {name:<30} Score: {score:.4f} ({score*100:.2f}%)")
    
#     print("\n" + "="*70 + "\n")


# def main():
#     """Main execution"""
#     print("\n" + "="*70)
#     print("DECISION COMPANION SYSTEM")
#     print("="*70)
#     print("\n✨ Simple Priority-Based Decision Making")
#     print("   Just rank what matters most to you - we handle the rest!")
    
#     decision = input("\n📋 What decision are you making?\n> ").strip()
    
#     # Get options
#     print(f"\n{'='*70}")
#     print("STEP 1: DEFINE OPTIONS")
#     print("="*70)
#     num_options = get_int("\nHow many options to compare? ")
    
#     options = []
#     for i in range(num_options):
#         name = input(f"Option {i+1} name: ").strip()
#         options.append({'name': name, 'values': {}})
    
#     # Get criteria IN PRIORITY ORDER
#     print(f"\n{'='*70}")
#     print("STEP 2: DEFINE CRITERIA (In Priority Order)")
#     print("="*70)
#     print("\n⭐ IMPORTANT: Enter criteria from MOST to LEAST important")
#     print("   Example: 1st = Performance, 2nd = Price, 3rd = Battery")
#     print("\n💡 Weights will be assigned automatically:")
#     print("   Priority 1 gets 50% importance")
#     print("   Priority 2 gets 25% importance")
#     print("   Priority 3 gets 12.5% importance")
#     print("   And so on...\n")
    
#     num_criteria = get_int("How many criteria? ")
    
#     # Calculate weights automatically
#     weights = calculate_priority_weights(num_criteria)
    
#     criteria = {}
    
#     print("\n" + "─"*70)
#     for i in range(num_criteria):
#         print(f"\n--- Priority #{i+1} Criterion (Auto-weight: {weights[i]*100:.1f}%) ---")
#         name = input("Name: ").strip()
        
#         print("Type: 1 = Benefit (higher is better), 2 = Cost (lower is better)")
#         type_choice = input("Choose (1/2): ").strip()
#         crit_type = 'benefit' if type_choice == '1' else 'cost'
        
#         criteria[name] = {
#             'weight': weights[i],
#             'type': crit_type,
#             'priority': i + 1
#         }
    
#     # Show assigned weights
#     print(f"\n{'─'*70}")
#     print("📊 AUTO-ASSIGNED WEIGHTS:")
#     print(f"{'─'*70}")
#     total_check = 0
#     for crit_name, crit_data in criteria.items():
#         print(f"  • {crit_name:<25} {crit_data['weight']*100:>6.2f}% (Priority #{crit_data['priority']})")
#         total_check += crit_data['weight']
#     print(f"{'─'*70}")
#     print(f"  {'Total:':<25} {total_check*100:>6.2f}%")
    
#     # Get values for each option
#     print(f"\n{'='*70}")
#     print("STEP 3: ENTER VALUES")
#     print("="*70)
#     print("\nEnter the value for each option on each criterion\n")
    
#     for option in options:
#         print(f"--- {option['name']} ---")
#         for crit_name in criteria.keys():
#             value = get_float(f"  {crit_name}: ")
#             option['values'][crit_name] = value
#         print()
    
#     # Analyze
#     print("="*70)
#     print("ANALYZING...")
#     print("="*70)
    
#     ranked, scores = analyze_decision(options, criteria)
    
#     # Display results
#     print_results(ranked, scores, options, criteria)
    
#     print("Thank you for using Decision Companion System!\n")


# if __name__ == "__main__":
#     try:
#         main()
#     except KeyboardInterrupt:
#         print("\n\n❌ Cancelled by user\n")
#     except Exception as e:
#         print(f"\n\n❌ Error: {e}\n")

#!/usr/bin/env python3
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
#                 ideal_best[c_id], ideal_worst[c_id] = max(v_list), min(v_list)
#             else:
#                 ideal_best[c_id], ideal_worst[c_id] = min(v_list), max(v_list)

#         # 4. Scoring
#         results = []
#         for opt in options:
#             name = opt['name']
#             d_best = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_best[c['id']])**2 for c in criteria))
#             d_worst = math.sqrt(sum((weighted_matrix[name][c['id']] - ideal_worst[c['id']])**2 for c in criteria))
            
#             total_dist = d_best + d_worst
#             performance_score = (d_worst / total_dist) if total_dist != 0 else 0.5
            
#             results.append({"name": name, "score": round(performance_score, 4)})

#         return sorted(results, key=lambda x: x['score'], reverse=True)

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
#     print("\n--- DECISION COMPANION SYSTEM ---")
#     goal = input("What are you deciding? (e.g., Best Laptop): ")

#     # 1. Gather Criteria
#     print("\nSTEP 1: Define Criteria (Ranked from Most Important to Least)")
#     num_crit = get_input("How many criteria? ", int)
#     criteria = []
#     for i in range(num_crit):
#         print(f"\nPriority #{i+1}:")
#         name = get_input("  Name (e.g., Price): ")
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

#     # 2. Gather Options
#     print("\nSTEP 2: Define Options")
#     num_opts = get_input("How many options to compare? ", int)
#     options = []
#     for i in range(num_opts):
#         opt_name = get_input(f"  Name for Option {i+1}: ")
#         opt_values = {}
#         print(f"  Enter values for {opt_name} (use numbers or 'High', 'Medium', 'Low'):")
#         for crit in criteria:
#             val = get_input(f"    {crit['name']}: ")
#             opt_values[crit['id']] = val
#         options.append({"name": opt_name, "values": opt_values})

#     # 3. Calculate and Display
#     print("\n--- RESULTS ---")
#     results = engine.run_topsis(options, criteria)
    
#     for i, res in enumerate(results, 1):
#         status = "🏆 RECOMMENDED" if i == 1 else f"Rank {i}"
#         print(f"{status}: {res['name']} (Match Score: {res['score']*100:.2f}%)")

# if __name__ == "__main__":
#     main()

import math

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
                "original_values": opt['values']  # Keep original user inputs
            })

        # Sort by score
        results = sorted(results, key=lambda x: x['score'], reverse=True)
        
        return results, ideal_best, weighted_matrix, criteria

    def generate_reasoning(self, top_option, ideal_best, weighted_matrix, criteria, all_options):
        """Generate reasoning statement with original user values"""
        matching_criteria = []
        threshold = 0.05  # Within 5% considered matching
        
        for crit in criteria:
            c_id = crit['id']
            option_weighted = top_option['weighted_values'][c_id]
            ideal_value = ideal_best[c_id]
            
            # Check if this option matches ideal
            if ideal_value != 0:
                diff_pct = abs(option_weighted - ideal_value) / abs(ideal_value)
            else:
                diff_pct = abs(option_weighted - ideal_value)
            
            if diff_pct <= threshold:
                # This criterion matches ideal - get the original user input
                original_input = top_option['original_values'][c_id]
                
                matching_criteria.append({
                    'name': crit['name'],
                    'value': original_input,  # The actual value user entered
                    'type': crit['type'],
                    'weight': crit['weight']
                })
        
        # Sort by weight (most important first)
        matching_criteria.sort(key=lambda x: x['weight'], reverse=True)
        
        return matching_criteria

def get_input(prompt, type_=str):
    while True:
        try:
            val = input(prompt).strip()
            if not val: continue
            return type_(val)
        except ValueError:
            print(f"Invalid input. Please enter a {type_.__name__}.")

def main():
    engine = DecisionEngine()
    print("\n" + "="*70)
    print("DECISION COMPANION SYSTEM")
    print("="*70)
    goal = input("\nWhat are you deciding? (e.g., Best Laptop): ")

    # 1. Gather Criteria
    print("\n" + "="*70)
    print("STEP 1: Define Criteria (Ranked from Most Important to Least)")
    print("="*70)
    num_crit = get_input("How many criteria? ", int)
    criteria = []
    for i in range(num_crit):
        print(f"\nPriority #{i+1}:")
        name = get_input("  Name (e.g., Price, Processor, Cost): ")
        c_type = get_input("  Type (1 for Benefit/Higher is better, 2 for Cost/Lower is better): ")
        criteria.append({
            "id": f"c{i}", 
            "name": name, 
            "type": "benefit" if c_type == "1" else "cost"
        })

    # Auto-assign ROC weights
    weights = engine.calculate_roc_weights(num_crit)
    for i, crit in enumerate(criteria):
        crit['weight'] = weights[i]

    print("\n" + "-"*70)
    print("AUTO-ASSIGNED WEIGHTS (Based on Priority):")
    print("-"*70)
    for i, crit in enumerate(criteria):
        print(f"  Priority #{i+1}: {crit['name']:<20} {crit['weight']*100:>6.2f}%")

    # 2. Gather Options
    print("\n" + "="*70)
    print("STEP 2: Define Options")
    print("="*70)
    num_opts = get_input("How many options to compare? ", int)
    options = []
    for i in range(num_opts):
        opt_name = get_input(f"\nName for Option {i+1}: ")
        opt_values = {}
        print(f"Enter values for '{opt_name}' (use numbers or 'High', 'Medium', 'Low'):")
        for crit in criteria:
            val = get_input(f"  {crit['name']}: ")
            opt_values[crit['id']] = val
        options.append({"name": opt_name, "values": opt_values})

    # 3. Calculate and Display
    print("\n" + "="*70)
    print("ANALYZING...")
    print("="*70)
    
    results, ideal_best, weighted_matrix, criteria_list = engine.run_topsis(options, criteria)
    
    # Show ranking
    print("\n" + "="*70)
    print("RESULTS:")
    print("="*70)
    for i, res in enumerate(results, 1):
        if i == 1:
            print(f"🏆 {res['name']:<30} Score: {res['score']*100:>6.2f}%")
        else:
            print(f"{i}.  {res['name']:<30} Score: {res['score']*100:>6.2f}%")
    
    # Generate and show reasoning
    if results:
        top_option = results[0]
        matching_criteria = engine.generate_reasoning(
            top_option, ideal_best, weighted_matrix, criteria_list, results
        )
        
        print("\n" + "="*70)
        print("WHY THIS OPTION WON:")
        print("="*70)
        
        if matching_criteria:
            # Build the statement
            option_name = top_option['name']
            
            # Create pairs of "adjective + criterion"
            criterion_phrases = []
            for mc in matching_criteria:
                value_str = str(mc['value'])
                criterion_name = mc['name'].lower()
                
                # Build the phrase
                phrase = f"{value_str} {criterion_name}"
                criterion_phrases.append(phrase)
            
            # Format the statement
            if len(criterion_phrases) == 1:
                statement = f"'{option_name}' is the best option due to its {criterion_phrases[0]}."
            elif len(criterion_phrases) == 2:
                statement = f"'{option_name}' is the best option due to its {criterion_phrases[0]} and {criterion_phrases[1]}."
            else:
                # Three or more criteria
                all_but_last = ", ".join(criterion_phrases[:-1])
                statement = f"'{option_name}' is the best option due to its {all_but_last}, and {criterion_phrases[-1]}."
            
            print(f"\n{statement}")
            print("\nThese criteria match or are very close to the ideal solution.")
            
        else:
            print(f"\n'{top_option['name']}' is the best overall option based on")
            print("the weighted combination of all criteria.")
    
    print("\n" + "="*70)
    print("Thank you for using Decision Companion System!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()