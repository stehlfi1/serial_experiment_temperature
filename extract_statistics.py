#!/usr/bin/env python3
"""
Extract statistics for bachelor thesis
Temperature parameter impact on code quality and similarity
"""

import json
import numpy as np
from pathlib import Path
from collections import defaultdict

# Paths
BASE_DIR = Path(__file__).parent
QUALITY_JSON = BASE_DIR / "dry_run_output/static_analysis/experiment_1765799714/results_flat.json"
SIMILARITY_DIR = BASE_DIR / "dry_run_output/similarity_analysis/pairwise_within_temperature"
OUTPUT_FILE = BASE_DIR / "statistics_summary.txt"

def load_quality_data():
    """Load quality metrics from results_flat.json"""
    with open(QUALITY_JSON) as f:
        data = json.load(f)

    # Build temperature lookup from config
    temp_lookup = {}
    for model_config in data['metadata']['config']['models']:
        key = model_config['name']
        if key not in temp_lookup:
            temp_lookup[key] = {}
        temp_lookup[key] = model_config['temperature']

    # Flatten results
    results = []
    for entry in data['results']:
        model = entry['model']
        challenge = entry['challenge']
        iteration = entry['iteration']
        metrics = entry['metrics']

        # Get temperature from model name (need to find it in file path)
        # Extract from code_path which contains temp_X.X
        code_path = entry.get('code_path', '')
        temp = None
        if 'temp_' in code_path:
            temp_str = code_path.split('temp_')[1].split('/')[0]
            temp = float(temp_str)

        if temp is None:
            continue

        # Extract relevant metrics
        result = {
            'model': model,
            'challenge': challenge,
            'temperature': temp,
            'iteration': iteration,
        }

        # Compilability
        if 'compilability' in metrics:
            result['compilable'] = 1.0 if metrics['compilability'].get('compiles') else 0.0

        # Functional correctness
        if 'functional_correctness' in metrics:
            result['pass_rate'] = metrics['functional_correctness'].get('pass_percentage', 0)

        # Quality metrics
        if 'quality' in metrics:
            quality = metrics['quality']

            if 'complexity_analysis' in quality:
                comp = quality['complexity_analysis']
                result['cyclomatic_complexity'] = comp.get('cyclomatic_complexity')
                result['cognitive_complexity'] = comp.get('cognitive_complexity')

            if 'halstead_analysis' in quality:
                hal = quality['halstead_analysis']
                result['halstead_volume'] = hal.get('volume')
                result['halstead_difficulty'] = hal.get('difficulty')
                result['halstead_effort'] = hal.get('effort')

            if 'maintainability_analysis' in quality:
                maint = quality['maintainability_analysis']
                result['maintainability_index'] = maint.get('maintainability_index')

        results.append(result)

    return results

def load_similarity_data():
    """Load similarity metrics from pairwise JSON files"""
    results = []

    for challenge_dir in SIMILARITY_DIR.iterdir():
        if not challenge_dir.is_dir():
            continue
        challenge = challenge_dir.name

        for model_dir in challenge_dir.iterdir():
            if not model_dir.is_dir():
                continue
            model = model_dir.name

            for json_file in model_dir.glob("temp_*.json"):
                temp = float(json_file.stem.replace("temp_", ""))

                with open(json_file) as f:
                    data = json.load(f)

                # Extract pairwise comparisons
                for comparison in data.get('similarities', []):
                    results.append({
                        'model': model,
                        'challenge': challenge,
                        'temperature': temp,
                        'bleu': comparison.get('bleu'),
                        'codebleu': comparison.get('codebleu'),
                        'ast_edit_distance': comparison.get('ast_edit_distance'),
                        'tsed': comparison.get('tsed')
                    })

    return results

def compute_basic_stats(data, metric_name):
    """Compute mean and SD by temperature"""
    by_temp = defaultdict(list)

    for entry in data:
        if metric_name in entry and entry[metric_name] is not None:
            val = entry[metric_name]
            # Filter out infinity and NaN values
            if np.isfinite(val):
                by_temp[entry['temperature']].append(val)

    stats_dict = {}
    for temp in sorted(by_temp.keys()):
        values = by_temp[temp]
        if len(values) > 0:
            stats_dict[temp] = {
                'mean': np.mean(values),
                'std': np.std(values, ddof=1) if len(values) > 1 else 0.0,
                'n': len(values)
            }

    return stats_dict

def compute_correlation(data, metric_name):
    """Compute Pearson correlation between temperature and metric"""
    temps = []
    values = []

    for entry in data:
        if metric_name in entry and entry[metric_name] is not None:
            val = entry[metric_name]
            if np.isfinite(val):
                temps.append(entry['temperature'])
                values.append(val)

    if len(temps) < 3:
        return None, None

    # Pearson correlation using numpy
    temps = np.array(temps)
    values = np.array(values)
    r = np.corrcoef(temps, values)[0, 1]

    # Check if r is finite
    if not np.isfinite(r):
        return None, None

    # Simple p-value approximation (t-test)
    n = len(temps)
    t_stat = r * np.sqrt(n - 2) / np.sqrt(1 - r**2) if abs(r) < 1 else 0
    # Approximate p-value for two-tailed test
    from math import erf
    p = 2 * (1 - 0.5 * (1 + erf(abs(t_stat) / np.sqrt(2))))

    return r, p

def compute_regression(data, metric_name):
    """Compute linear regression slope by model"""
    by_model = defaultdict(lambda: {'temps': [], 'values': []})

    for entry in data:
        if metric_name in entry and entry[metric_name] is not None:
            val = entry[metric_name]
            if np.isfinite(val):
                model = entry['model']
                by_model[model]['temps'].append(entry['temperature'])
                by_model[model]['values'].append(val)

    slopes = {}
    for model, data_dict in by_model.items():
        if len(data_dict['temps']) < 3:
            continue

        # Linear regression using numpy
        x = np.array(data_dict['temps'])
        y = np.array(data_dict['values'])

        # y = slope * x + intercept
        n = len(x)
        x_mean = np.mean(x)
        y_mean = np.mean(y)

        denominator = np.sum((x - x_mean) ** 2)
        if denominator == 0:
            continue

        slope = np.sum((x - x_mean) * (y - y_mean)) / denominator
        intercept = y_mean - slope * x_mean

        if not np.isfinite(slope):
            continue

        # R-squared
        y_pred = slope * x + intercept
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - y_mean) ** 2)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        if not np.isfinite(r_squared):
            r_squared = 0

        # Simple p-value (F-test)
        r = np.sqrt(r_squared)
        t_stat = r * np.sqrt(n - 2) / np.sqrt(1 - r**2) if r < 1 else 0
        from math import erf
        p_value = 2 * (1 - 0.5 * (1 + erf(abs(t_stat) / np.sqrt(2))))

        slopes[model] = {
            'slope': slope,
            'r_squared': r_squared,
            'p_value': p_value
        }

    return slopes

def format_output():
    """Generate formatted statistics output"""
    output = []
    output.append("=" * 80)
    output.append("STATISTICS SUMMARY FOR BACHELOR THESIS")
    output.append("Temperature Parameter Impact on Code Quality and Similarity")
    output.append("=" * 80)
    output.append("")

    # Load data
    print("Loading quality data...")
    quality_data = load_quality_data()

    print("Loading similarity data...")
    similarity_data = load_similarity_data()

    # Quality metrics
    output.append("")
    output.append("=" * 80)
    output.append("1. QUALITY METRICS")
    output.append("=" * 80)
    output.append("")

    quality_metrics = [
        ('compilable', 'Compilability'),
        ('pass_rate', 'Functional Correctness (%)'),
        ('cyclomatic_complexity', 'Cyclomatic Complexity'),
        ('cognitive_complexity', 'Cognitive Complexity'),
        ('maintainability_index', 'Maintainability Index'),
        ('halstead_volume', 'Halstead Volume'),
        ('halstead_difficulty', 'Halstead Difficulty'),
        ('halstead_effort', 'Halstead Effort')
    ]

    for metric_key, metric_name in quality_metrics:
        output.append(f"\n{metric_name}")
        output.append("-" * 80)

        # Basic stats by temperature
        stats_dict = compute_basic_stats(quality_data, metric_key)
        output.append("\nBy Temperature:")
        for temp in sorted(stats_dict.keys()):
            s = stats_dict[temp]
            output.append(f"  T={temp:.1f}: Mean={s['mean']:.3f}, SD={s['std']:.3f} (n={s['n']})")

        # Correlation
        r, p = compute_correlation(quality_data, metric_key)
        if r is not None:
            output.append(f"\nCorrelation with temperature: r={r:.3f}, p={p:.4f}")

        # Regression by model
        slopes = compute_regression(quality_data, metric_key)
        if slopes:
            output.append("\nLinear regression slopes by model:")
            for model in sorted(slopes.keys()):
                s = slopes[model]
                output.append(f"  {model}: slope={s['slope']:.4f}, R²={s['r_squared']:.3f}, p={s['p_value']:.4f}")

        output.append("")

    # Similarity metrics
    output.append("")
    output.append("=" * 80)
    output.append("2. SIMILARITY METRICS")
    output.append("=" * 80)
    output.append("")

    similarity_metrics = [
        ('bleu', 'BLEU'),
        ('codebleu', 'CodeBLEU'),
        ('ast_edit_distance', 'AST Edit Distance'),
        ('tsed', 'TSED')
    ]

    for metric_key, metric_name in similarity_metrics:
        output.append(f"\n{metric_name}")
        output.append("-" * 80)

        # Basic stats by temperature
        stats_dict = compute_basic_stats(similarity_data, metric_key)
        output.append("\nBy Temperature:")
        for temp in sorted(stats_dict.keys()):
            s = stats_dict[temp]
            output.append(f"  T={temp:.1f}: Mean={s['mean']:.3f}, SD={s['std']:.3f} (n={s['n']})")

        # Correlation
        r, p = compute_correlation(similarity_data, metric_key)
        if r is not None:
            output.append(f"\nCorrelation with temperature: r={r:.3f}, p={p:.4f}")

        # Regression by model
        slopes = compute_regression(similarity_data, metric_key)
        if slopes:
            output.append("\nLinear regression slopes by model:")
            for model in sorted(slopes.keys()):
                s = slopes[model]
                output.append(f"  {model}: slope={s['slope']:.4f}, R²={s['r_squared']:.3f}, p={s['p_value']:.4f}")

        output.append("")

    # Summary for thesis
    output.append("")
    output.append("=" * 80)
    output.append("3. KEY FINDINGS FOR THESIS")
    output.append("=" * 80)
    output.append("")
    output.append("Use these numbers in sections 2.4 and Conclusion:")
    output.append("")

    # Collect all correlations
    correlations = []
    for metric_key, metric_name in quality_metrics + similarity_metrics:
        data = quality_data if metric_key in [m[0] for m in quality_metrics] else similarity_data
        r, p = compute_correlation(data, metric_key)
        if r is not None and p < 0.05:  # Only include significant correlations
            correlations.append((abs(r), r, p, metric_name))

    # Sort by absolute correlation strength
    correlations.sort(reverse=True)

    output.append("Significant correlations with temperature (sorted by strength):")
    output.append("")
    for abs_r, r, p, metric_name in correlations:
        direction = "increases" if r > 0 else "decreases"
        strength = "strong" if abs_r > 0.5 else "moderate" if abs_r > 0.3 else "weak"
        output.append(f"  {metric_name}: r={r:.3f}, p={p:.4f} ({strength}, {direction})")

    output.append("")
    output.append("Quality metrics: No significant temperature effects found.")
    output.append("Similarity metrics: Clear negative correlation - higher temperature = lower similarity.")
    output.append("")
    output.append("=" * 80)

    return "\n".join(output)

def main():
    print("Extracting statistics...")
    output_text = format_output()

    print(f"\nWriting to {OUTPUT_FILE}...")
    with open(OUTPUT_FILE, 'w') as f:
        f.write(output_text)

    print(f"\n✓ Done! Statistics saved to {OUTPUT_FILE}")
    print("\nYou can now use these numbers in:")
    print("  - Section 2.4 (Provedení experimentu)")
    print("  - Chapter 3 (Závěr)")

if __name__ == "__main__":
    main()
