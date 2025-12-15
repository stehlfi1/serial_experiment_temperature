"""
Data loader for static analysis results.
Loads test results and quality metrics into unified DataFrame.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.data_filtering import (
    get_all_problematic_iterations,
    get_non_compilable_iterations,
    get_pattern_a_errors,
    get_exclusion_summary
)


class StaticAnalysisDataLoader:
    """Load and combine static analysis data from experiments."""

    def __init__(self, base_dir: str = "dry_run_output/static_analysis"):
        self.base_dir = Path(base_dir)

    def load_all_experiments(self, exclude_mode: str = "all") -> pd.DataFrame:
        """
        Load all experiment results into a single DataFrame.

        Args:
            exclude_mode: Filtering mode:
                - "none": No filtering (raw data, for compilation graphs)
                - "syntax": Exclude only syntax errors
                - "all": Exclude syntax errors + Pattern A errors (default)

        Returns:
            DataFrame with quality metrics per iteration
        """
        # Get list of iterations to exclude
        if exclude_mode == "none":
            excluded = set()
            print("Loading raw data (no filtering)")
        elif exclude_mode == "syntax":
            excluded = get_non_compilable_iterations()
            print(f"Excluding {len(excluded)} syntax errors only")
        elif exclude_mode == "all":
            excluded = get_all_problematic_iterations()
            syntax_errors = get_non_compilable_iterations()
            pattern_a = get_pattern_a_errors()
            print(f"Excluding {len(excluded)} problematic iterations:")
            print(f"  - Syntax errors: {len(syntax_errors)}")
            print(f"  - Pattern A errors (pytest-incompatible): {len(pattern_a)}")
        else:
            raise ValueError(f"Invalid exclude_mode: {exclude_mode}. Must be 'none', 'syntax', or 'all'")

        if excluded:
            summary = get_exclusion_summary(excluded)
            print(f"  Total: {summary['total_excluded']} iterations ({summary['percentage']:.2f}%)")
        print()

        all_data = []

        # Find all experiment directories
        for exp_dir in self.base_dir.glob("experiment_*"):
            results_file = exp_dir / "results_flat.json"
            if not results_file.exists():
                continue

            # Load results
            with open(results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Build model->temperature mapping from config
            temp_map = {}
            config = data.get('metadata', {}).get('config', {})
            for model_config in config.get('models', []):
                model_name = model_config['name']
                temp = model_config.get('temperature')
                # Use model_name as key (may have duplicates with different temps)
                # For now, we'll match by looking at the code_path in results
                if model_name not in temp_map:
                    temp_map[model_name] = []
                temp_map[model_name].append(temp)

            # Process each result
            for result in data['results']:
                row = self._flatten_result(result, temp_map)

                # Check if this iteration should be excluded
                should_exclude = False
                if excluded and row['temperature'] is not None:
                    for ex_model, ex_challenge, ex_temp, ex_iteration in excluded:
                        if (row['model'] == ex_model and
                            row['challenge'] == ex_challenge and
                            row['temperature'] == ex_temp and
                            row['iteration'] == ex_iteration):
                            should_exclude = True
                            break

                if not should_exclude:
                    all_data.append(row)

        if not all_data:
            raise ValueError(f"No static analysis data found in {self.base_dir}")

        df = pd.DataFrame(all_data)
        return df

    def _flatten_result(self, result: Dict[str, Any], temp_map: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Flatten nested metrics into single-level dict.

        Args:
            result: Single test result from results_flat.json
            temp_map: Map from model name to list of temperatures

        Returns:
            Flattened dictionary
        """
        row = {
            'model': result['model'],
            'challenge': result['challenge'],
            'iteration': result['iteration'],
            'prompt': result['prompt'],
        }

        # Extract temperature from code_path (contains temp_X.X folder)
        code_path = result.get('code_path', '')
        temp = None
        if 'temp_' in code_path:
            # Extract temperature from path like .../temp_0.4/...
            import re
            match = re.search(r'temp_([\d.]+)', code_path)
            if match:
                temp = float(match.group(1))

        row['temperature'] = temp

        metrics = result.get('metrics', {})

        # Compilability
        comp = metrics.get('compilability', {})
        row['compiles'] = comp.get('compiles', False)

        # Functional completeness
        func_comp = metrics.get('functional_completeness', {})
        row['completeness_score'] = func_comp.get('score', 0.0)
        row['expected_features'] = func_comp.get('expected_features', 0)
        row['found_features'] = func_comp.get('found_features', 0)

        # Functional correctness
        func_corr = metrics.get('functional_correctness', {})
        row['tests_passed'] = func_corr.get('tests_passed', 0)
        row['tests_run'] = func_corr.get('tests_run', 0)
        row['pass_rate'] = func_corr.get('pass_rate', 0.0)

        # Quality metrics
        quality = metrics.get('quality', {})

        # Complexity
        complexity = quality.get('complexity_analysis', {})
        row['cyclomatic_complexity'] = complexity.get('cyclomatic_complexity', 0)
        row['cognitive_complexity'] = complexity.get('cognitive_complexity', 0)
        row['max_nesting_depth'] = complexity.get('max_nesting_depth', 0)

        # Halstead
        halstead = quality.get('halstead_analysis', {})
        row['halstead_volume'] = halstead.get('volume', 0.0)
        row['halstead_difficulty'] = halstead.get('difficulty', 0.0)
        row['halstead_effort'] = halstead.get('effort', 0.0)
        row['halstead_bugs'] = halstead.get('bugs', 0.0)

        # Maintainability
        maint = quality.get('maintainability_analysis', {})
        row['maintainability_index'] = maint.get('maintainability_index', 0.0)
        row['maintainability_rank'] = maint.get('maintainability_rank', 'F')

        # Code style
        style = quality.get('code_style_analysis', {})
        row['naming_convention_score'] = style.get('naming_convention_score', 0.0)
        row['simple_function_ratio'] = style.get('simple_function_ratio', 0.0)

        # Structure metrics
        structure = metrics.get('structure', {})

        # Control flow
        control_flow = structure.get('control_flow_analysis', {})
        row['has_loops'] = control_flow.get('has_loops', False)
        row['has_conditionals'] = control_flow.get('has_conditionals', False)

        # OOP
        oop = structure.get('oop_analysis', {})
        row['class_count'] = oop.get('class_count', 0)
        row['method_count'] = oop.get('method_count', 0)

        return row

    def get_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get summary statistics about the loaded data."""
        return {
            'total_results': len(df),
            'challenges': sorted(df['challenge'].unique().tolist()),
            'models': sorted(df['model'].unique().tolist()),
            'temperatures': sorted([t for t in df['temperature'].unique() if t is not None]),
            'iterations': len(df[df['model'] == df['model'].iloc[0]]),
            'compilation_rate': df['compiles'].mean(),
            'avg_pass_rate': df['pass_rate'].mean(),
        }


if __name__ == "__main__":
    # Test loading
    loader = StaticAnalysisDataLoader()
    df = loader.load_all_experiments()

    print("Loaded static analysis data:")
    print(f"Shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())

    print(f"\nSummary:")
    summary = loader.get_summary(df)
    for key, value in summary.items():
        print(f"  {key}: {value}")
