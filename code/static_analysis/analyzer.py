from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import pandas as pd
from datetime import datetime

from .results.data_models import ExperimentResults


class ExperimentAnalyzer:
    def __init__(self, experiment_results: ExperimentResults):
        self.experiment = experiment_results
        self.df: Optional[pd.DataFrame] = None
    
    def to_dataframe(self) -> pd.DataFrame:
        if self.df is None:
            self._build_dataframe()
        return self.df
    
    def _build_dataframe(self) -> None:
        rows = []
        
        for result in self.experiment.results:
            row = {
                "experiment_id": result.experiment_id,
                "model": result.model,
                "challenge": result.challenge,
                "prompt": result.prompt,
                "iteration": result.iteration,
                "timestamp": result.timestamp,
                "code_path": result.code_path,
                "execution_time": result.execution_time,
                "status": result.status
            }
            
            # Handle both old flat format and new hierarchical format
            metrics_dict = result.metrics.to_dict()
            flattened_metrics = self._flatten_metrics(metrics_dict)
            row.update(flattened_metrics)
            
            rows.append(row)
        
        self.df = pd.DataFrame(rows)
    
    def summary_by_model(self) -> pd.DataFrame:
        df = self.to_dataframe()
        available_cols = self._get_available_columns()
        
        # Build aggregation dict with available columns
        agg_dict = {}
        for col in available_cols.keys():
            if col in df.columns:
                if col.endswith('_status'):
                    agg_dict[col] = lambda x: (x == 'success').mean()
                else:
                    agg_dict[col] = 'mean'
        
        # Always include these if available
        agg_dict['execution_time'] = 'mean'
        agg_dict['status'] = lambda x: (x == 'success').mean()
        
        if not agg_dict:
            # Return empty DataFrame if no metrics available
            return pd.DataFrame()
        
        summary = df.groupby('model').agg(agg_dict).round(3)
        
        # Rename columns to display names
        column_mapping = {col: available_cols.get(col, col) for col in summary.columns if col in available_cols}
        column_mapping.update({
            'execution_time': 'Avg Execution Time',
            'status': 'Success Rate'
        })
        
        summary = summary.rename(columns=column_mapping)
        return summary
    
    def summary_by_prompt(self) -> pd.DataFrame:
        df = self.to_dataframe()
        available_cols = self._get_available_columns()
        
        # Build aggregation dict with available columns
        agg_dict = {}
        for col in available_cols.keys():
            if col in df.columns:
                if col.endswith('_status'):
                    agg_dict[col] = lambda x: (x == 'success').mean()
                else:
                    agg_dict[col] = 'mean'
        
        # Always include these if available
        agg_dict['execution_time'] = 'mean'
        agg_dict['status'] = lambda x: (x == 'success').mean()
        
        if not agg_dict:
            return pd.DataFrame()
        
        summary = df.groupby('prompt').agg(agg_dict).round(3)
        
        # Rename columns to display names
        column_mapping = {col: available_cols.get(col, col) for col in summary.columns if col in available_cols}
        column_mapping.update({
            'execution_time': 'Avg Execution Time',
            'status': 'Success Rate'
        })
        
        summary = summary.rename(columns=column_mapping)
        return summary
    
    def detailed_comparison(self) -> pd.DataFrame:
        df = self.to_dataframe()
        available_cols = self._get_available_columns()
        
        # Build aggregation dict with available columns
        agg_dict = {}
        for col in available_cols.keys():
            if col in df.columns:
                if not col.endswith('_status'):
                    agg_dict[col] = 'mean'
        
        agg_dict['execution_time'] = 'mean'
        
        if not agg_dict:
            return pd.DataFrame()
        
        comparison = df.groupby(['model', 'prompt']).agg(agg_dict).round(3)
        return comparison
    
    def export_for_latex(self, output_dir: Path) -> Dict[str, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        
        files = {}
        
        model_summary = self.summary_by_model()
        model_file = output_dir / "model_summary.csv"
        model_summary.to_csv(model_file)
        files["model_summary"] = model_file
        
        prompt_summary = self.summary_by_prompt()
        prompt_file = output_dir / "prompt_summary.csv"
        prompt_summary.to_csv(prompt_file)
        files["prompt_summary"] = prompt_file
        
        detailed = self.detailed_comparison()
        detailed_file = output_dir / "detailed_comparison.csv"
        detailed.to_csv(detailed_file)
        files["detailed_comparison"] = detailed_file
        
        full_data = self.to_dataframe()
        full_file = output_dir / "full_data.csv"
        full_data.to_csv(full_file, index=False)
        files["full_data"] = full_file
        
        return files
    
    def get_best_performers(self) -> Dict[str, Any]:
        df = self.to_dataframe()
        best = {}
        
        # Try different metric column names (old and new formats)
        modularity_cols = ['modularity_score', 'quality_maintainability_analysis_maintainability_index', 'modularity']
        completeness_cols = ['functional_completeness_score', 'functional_completeness']
        lines_cols = ['code_length_lines', 'quality_size_analysis_logical_lines_of_code', 'code_length']
        complexity_cols = ['quality_complexity_analysis_cyclomatic_complexity']
        
        # Find best modularity/maintainability
        for col in modularity_cols:
            if col in df.columns and not df[col].isna().all():
                best_idx = df[col].idxmax()
                best_row = df.loc[best_idx]
                best['modularity'] = {
                    'model': best_row['model'],
                    'prompt': best_row['prompt'],
                    'score': best_row[col],
                    'metric': col
                }
                break
        
        # Find best completeness
        for col in completeness_cols:
            if col in df.columns and not df[col].isna().all():
                best_idx = df[col].idxmax()
                best_row = df.loc[best_idx]
                best['completeness'] = {
                    'model': best_row['model'],
                    'prompt': best_row['prompt'], 
                    'score': best_row[col],
                    'metric': col
                }
                break
        
        # Find most concise (lowest lines)
        for col in lines_cols:
            if col in df.columns and not df[col].isna().all():
                best_idx = df[col].idxmin()
                best_row = df.loc[best_idx]
                best['most_concise'] = {
                    'model': best_row['model'],
                    'prompt': best_row['prompt'],
                    'lines': best_row[col],
                    'metric': col
                }
                break
        
        # Find lowest complexity
        for col in complexity_cols:
            if col in df.columns and not df[col].isna().all():
                best_idx = df[col].idxmin()
                best_row = df.loc[best_idx]
                best['lowest_complexity'] = {
                    'model': best_row['model'],
                    'prompt': best_row['prompt'],
                    'complexity': best_row[col],
                    'metric': col
                }
                break
        
        return best
    
    def _flatten_metrics(self, metrics: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
        """Flatten hierarchical metrics into a flat dictionary with dot notation."""
        flattened = {}
        
        for key, value in metrics.items():
            new_key = f"{prefix}_{key}" if prefix else key
            
            if isinstance(value, dict):
                # Check if this is a test result with status/error (leaf node)
                if "status" in value and len(value) <= 4:  # status, error, execution_time, maybe one metric
                    # Extract the actual metric value if present
                    for sub_key, sub_value in value.items():
                        if sub_key not in ["status", "error", "execution_time"] and isinstance(sub_value, (int, float, bool)):
                            flattened[new_key] = sub_value
                            break
                    else:
                        # No metric value found, use status info
                        flattened[f"{new_key}_status"] = value.get("status")
                        if "error" in value:
                            flattened[f"{new_key}_error"] = value["error"]
                else:
                    # Recursively flatten nested dictionaries
                    nested = self._flatten_metrics(value, new_key)
                    flattened.update(nested)
            else:
                flattened[new_key] = value
        
        return flattened
    
    def _get_available_columns(self) -> Dict[str, str]:
        """Get available metric columns and their display names."""
        df = self.to_dataframe()
        available = {}
        
        # Legacy format mappings
        legacy_mappings = {
            'compilability_compiles': 'Compilability Rate',
            'code_length_lines': 'Avg Lines', 
            'modularity_score': 'Avg Modularity',
            'functional_completeness_score': 'Avg Completeness'
        }
        
        # New format mappings (hierarchical)
        new_mappings = {
            'quality_complexity_analysis_cyclomatic_complexity': 'Avg Cyclomatic Complexity',
            'quality_size_analysis_logical_lines_of_code': 'Avg Lines of Code',
            'quality_size_analysis_function_count': 'Avg Function Count',
            'quality_maintainability_analysis_maintainability_index': 'Avg Maintainability Index',
            'structure_ast_analysis_node_count': 'Avg AST Nodes',
            'structure_control_flow_analysis_loop_count': 'Avg Loop Count',
            'compilability': 'Compilability Success',
            'code_length': 'Code Length Success',
            'modularity': 'Modularity Success',
            'functional_completeness': 'Functional Completeness Success'
        }
        
        # Check which columns exist
        for col, display_name in {**legacy_mappings, **new_mappings}.items():
            if col in df.columns:
                available[col] = display_name
        
        return available


class MultiExperimentAnalyzer:
    def __init__(self, experiments_dir: Path):
        self.experiments_dir = experiments_dir
        self.experiments: List[ExperimentResults] = []
    
    def load_all_experiments(self) -> None:
        for exp_dir in self.experiments_dir.iterdir():
            if exp_dir.is_dir() and exp_dir.name.startswith("experiment_"):
                tree_file = exp_dir / "results_tree.json"
                if tree_file.exists():
                    try:
                        experiment = ExperimentResults.load_from_tree(tree_file)
                        self.experiments.append(experiment)
                    except Exception as e:
                        print(f"Failed to load experiment {exp_dir}: {e}")
    
    def combined_dataframe(self) -> pd.DataFrame:
        all_dfs = []
        
        for exp in self.experiments:
            analyzer = ExperimentAnalyzer(exp)
            df = analyzer.to_dataframe()
            df['experiment_timestamp'] = exp.metadata.timestamp
            all_dfs.append(df)
        
        return pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame()
    
    def trend_analysis(self) -> pd.DataFrame:
        df = self.combined_dataframe()
        
        if df.empty:
            return pd.DataFrame()
        
        df['experiment_date'] = pd.to_datetime(df['experiment_timestamp']).dt.date
        
        # Build aggregation dict with available columns
        agg_dict = {'execution_time': 'mean'}
        
        # Try different metric columns
        metric_candidates = [
            'modularity_score', 'quality_maintainability_analysis_maintainability_index',
            'functional_completeness_score', 'functional_completeness',
            'quality_complexity_analysis_cyclomatic_complexity',
            'quality_size_analysis_logical_lines_of_code'
        ]
        
        for col in metric_candidates:
            if col in df.columns:
                agg_dict[col] = 'mean'
        
        if len(agg_dict) == 1:  # Only execution_time
            return pd.DataFrame()
        
        trends = df.groupby(['experiment_date', 'model']).agg(agg_dict).round(3)
        return trends
