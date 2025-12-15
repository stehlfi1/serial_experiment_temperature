"""
Data filtering utilities.
Identifies and filters non-compilable code iterations and pytest-incompatible code.
"""

import json
from pathlib import Path
from typing import List, Tuple, Set, Dict, Any


def get_pattern_a_errors(base_dir: str = "dry_run_output") -> Set[Tuple[str, str, float, int]]:
    """
    Find Pattern A errors: code compiles but has import-time execution issues.
    These iterations compile successfully but crash during pytest collection.

    Criteria:
        - compilability.compiles == True
        - functional_correctness.tests_run == 0
        - functional_correctness.error == "No test results found in pytest output"

    Args:
        base_dir: Base directory containing static analysis results

    Returns:
        Set of tuples: {(model, challenge, temperature, iteration), ...}
    """
    pattern_a = set()
    base_path = Path(base_dir) / "static_analysis"

    for exp_dir in base_path.glob("experiment_*"):
        results_file = exp_dir / "results_flat.json"
        if not results_file.exists():
            continue

        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        for result in data['results']:
            metrics = result.get('metrics', {})
            compilability = metrics.get('compilability', {})
            func_corr = metrics.get('functional_correctness', {})

            # Check for Pattern A: compiles but pytest fails at collection
            compiles = compilability.get('compiles', False)
            tests_run = func_corr.get('tests_run', 0)
            error = func_corr.get('error', '')

            if compiles and tests_run == 0 and error == "No test results found in pytest output":
                model = result['model']
                challenge = result['challenge']
                iteration = result['iteration']

                # Extract temperature
                code_path = result.get('code_path', '')
                temp = None
                if 'temp_' in code_path:
                    import re
                    match = re.search(r'temp_([\d.]+)', code_path)
                    if match:
                        temp = float(match.group(1))

                if temp is not None:
                    pattern_a.add((model, challenge, temp, iteration))

    return pattern_a


def get_non_compilable_iterations(base_dir: str = "dry_run_output") -> Set[Tuple[str, str, float, int]]:
    """
    Scan static analysis results to find non-compilable iterations.

    Args:
        base_dir: Base directory containing static analysis results

    Returns:
        Set of tuples: {(model, challenge, temperature, iteration), ...}

    Example:
        {('chatgpt', 'calculator', 0.6, 1)}
    """
    non_compilable = set()
    base_path = Path(base_dir) / "static_analysis"

    # Scan all experiment directories
    for exp_dir in base_path.glob("experiment_*"):
        results_file = exp_dir / "results_flat.json"
        if not results_file.exists():
            continue

        # Load results
        with open(results_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Check each result for compilation status
        for result in data['results']:
            metrics = result.get('metrics', {})
            compilability = metrics.get('compilability', {})

            # Check if it compiles
            compiles = compilability.get('compiles', False)

            if not compiles:
                # Extract metadata
                model = result['model']
                challenge = result['challenge']
                iteration = result['iteration']

                # Extract temperature from code path
                code_path = result.get('code_path', '')
                temp = None
                if 'temp_' in code_path:
                    import re
                    match = re.search(r'temp_([\d.]+)', code_path)
                    if match:
                        temp = float(match.group(1))

                if temp is not None:
                    non_compilable.add((model, challenge, temp, iteration))

    return non_compilable


def get_exclusion_summary(non_compilable: Set[Tuple[str, str, float, int]]) -> dict:
    """
    Generate summary statistics about excluded iterations.

    Args:
        non_compilable: Set of non-compilable iterations

    Returns:
        Dictionary with summary statistics
    """
    if not non_compilable:
        return {
            'total_excluded': 0,
            'percentage': 0.0,
            'by_model': {},
            'by_challenge': {},
            'by_temperature': {},
            'details': []
        }

    by_model = {}
    by_challenge = {}
    by_temperature = {}

    for model, challenge, temp, iteration in non_compilable:
        # Count by model
        by_model[model] = by_model.get(model, 0) + 1

        # Count by challenge
        by_challenge[challenge] = by_challenge.get(challenge, 0) + 1

        # Count by temperature
        by_temperature[temp] = by_temperature.get(temp, 0) + 1

    # Total iterations: 3 models × 3 challenges × 6 temps × 20 iterations = 1080
    total_iterations = 1080

    return {
        'total_excluded': len(non_compilable),
        'percentage': (len(non_compilable) / total_iterations) * 100,
        'by_model': by_model,
        'by_challenge': by_challenge,
        'by_temperature': by_temperature,
        'details': sorted(list(non_compilable))
    }


def get_all_problematic_iterations(base_dir: str = "dry_run_output") -> Set[Tuple[str, str, float, int]]:
    """
    Get all problematic iterations: both syntax errors and Pattern A errors.
    This is the recommended filter for analysis.

    Returns:
        Set of tuples: {(model, challenge, temperature, iteration), ...}
    """
    syntax_errors = get_non_compilable_iterations(base_dir)
    pattern_a = get_pattern_a_errors(base_dir)
    return syntax_errors | pattern_a


if __name__ == "__main__":
    # Test the filtering
    print("="*80)
    print("CODE QUALITY FILTERING ANALYSIS")
    print("="*80)
    print()

    # Syntax errors
    print("1. Syntax Errors (compiles = False):")
    print("-" * 40)
    syntax_errors = get_non_compilable_iterations()
    syntax_summary = get_exclusion_summary(syntax_errors)

    print(f"Found {syntax_summary['total_excluded']} iterations with syntax errors ({syntax_summary['percentage']:.2f}%)")
    if syntax_summary['total_excluded'] > 0:
        print("  By model:", syntax_summary['by_model'])
        print("  By challenge:", syntax_summary['by_challenge'])
        for model, challenge, temp, iteration in syntax_summary['details']:
            print(f"    - {model}/{challenge}/temp_{temp}/iteration_{iteration}")
    print()

    # Pattern A errors
    print("2. Pattern A Errors (compiles but pytest-incompatible):")
    print("-" * 40)
    pattern_a = get_pattern_a_errors()
    pattern_a_summary = get_exclusion_summary(pattern_a)

    print(f"Found {pattern_a_summary['total_excluded']} iterations with Pattern A errors ({pattern_a_summary['percentage']:.2f}%)")
    if pattern_a_summary['total_excluded'] > 0:
        print("  By model:", pattern_a_summary['by_model'])
        print("  By challenge:", pattern_a_summary['by_challenge'])
        for model, challenge, temp, iteration in pattern_a_summary['details']:
            print(f"    - {model}/{challenge}/temp_{temp}/iteration_{iteration}")
    print()

    # Combined
    print("3. Total Problematic Iterations (recommended filter):")
    print("-" * 40)
    all_problematic = get_all_problematic_iterations()
    all_summary = get_exclusion_summary(all_problematic)

    print(f"Total: {all_summary['total_excluded']} iterations ({all_summary['percentage']:.2f}%)")
    print(f"  Syntax errors: {len(syntax_errors)}")
    print(f"  Pattern A: {len(pattern_a)}")
    print()

    if all_summary['total_excluded'] > 0:
        print("Breakdown:")
        print(f"  By model: {all_summary['by_model']}")
        print(f"  By challenge: {all_summary['by_challenge']}")
        print(f"  By temperature: {all_summary['by_temperature']}")
