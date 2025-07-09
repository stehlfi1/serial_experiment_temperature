from pathlib import Path
from typing import Dict, List, Any, Optional
import json
import pandas as pd
from datetime import datetime

from .data_models import ExperimentResults


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
            
            for metric_type, metric_data in result.metrics.to_dict().items():
                if isinstance(metric_data, dict):
                    for key, value in metric_data.items():
                        row[f"{metric_type}_{key}"] = value
                else:
                    row[metric_type] = metric_data
            
            rows.append(row)
        
        self.df = pd.DataFrame(rows)
    
    def summary_by_model(self) -> pd.DataFrame:
        df = self.to_dataframe()
        
        summary = df.groupby('model').agg({
            'compilability_compiles': 'mean',
            'code_length_lines': 'mean',
            'modularity_score': 'mean',
            'functional_completeness_score': 'mean',
            'execution_time': 'mean',
            'status': lambda x: (x == 'success').mean()
        }).round(3)
        
        summary.columns = [
            'Compilability Rate',
            'Avg Lines',
            'Avg Modularity',
            'Avg Completeness',
            'Avg Execution Time',
            'Success Rate'
        ]
        
        return summary
    
    def summary_by_prompt(self) -> pd.DataFrame:
        df = self.to_dataframe()
        
        summary = df.groupby('prompt').agg({
            'compilability_compiles': 'mean',
            'code_length_lines': 'mean',
            'modularity_score': 'mean',
            'functional_completeness_score': 'mean',
            'execution_time': 'mean',
            'status': lambda x: (x == 'success').mean()
        }).round(3)
        
        summary.columns = [
            'Compilability Rate',
            'Avg Lines',
            'Avg Modularity',
            'Avg Completeness',
            'Avg Execution Time',
            'Success Rate'
        ]
        
        return summary
    
    def detailed_comparison(self) -> pd.DataFrame:
        df = self.to_dataframe()
        
        comparison = df.groupby(['model', 'prompt']).agg({
            'compilability_compiles': 'mean',
            'code_length_lines': 'mean',
            'modularity_score': 'mean',
            'functional_completeness_score': 'mean',
            'execution_time': 'mean'
        }).round(3)
        
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
        
        if 'modularity_score' in df.columns:
            best_modularity = df.loc[df['modularity_score'].idxmax()]
            best['modularity'] = {
                'model': best_modularity['model'],
                'prompt': best_modularity['prompt'],
                'score': best_modularity['modularity_score']
            }
        
        if 'functional_completeness_score' in df.columns:
            best_completeness = df.loc[df['functional_completeness_score'].idxmax()]
            best['completeness'] = {
                'model': best_completeness['model'],
                'prompt': best_completeness['prompt'],
                'score': best_completeness['functional_completeness_score']
            }
        
        if 'code_length_lines' in df.columns:
            most_concise = df.loc[df['code_length_lines'].idxmin()]
            best['most_concise'] = {
                'model': most_concise['model'],
                'prompt': most_concise['prompt'],
                'lines': most_concise['code_length_lines']
            }
        
        return best


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
        
        trends = df.groupby(['experiment_date', 'model']).agg({
            'modularity_score': 'mean',
            'functional_completeness_score': 'mean',
            'execution_time': 'mean'
        }).round(3)
        
        return trends
