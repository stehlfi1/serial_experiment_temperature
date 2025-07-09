from pathlib import Path
from typing import Dict, Any, List, Optional
import time
import json

from .data_models import (
    ExperimentConfig, ExperimentMetadata, ExperimentResults, 
    TestResult, TestMetrics
)


class ExperimentManager:
    def __init__(self, base_output_dir: Path):
        self.base_output_dir = base_output_dir
        self.current_experiment: Optional[ExperimentResults] = None
    
    def start_experiment(self, config: ExperimentConfig) -> ExperimentMetadata:
        experiment_dir = self.base_output_dir / f"experiment_{int(time.time())}"
        experiment_dir.mkdir(parents=True, exist_ok=True)
        
        metadata = ExperimentMetadata.create_new(config, str(experiment_dir))
        self.current_experiment = ExperimentResults(metadata)
        
        metadata_path = experiment_dir / "experiment_metadata.json"
        metadata.save(metadata_path)
        
        return metadata
    
    def add_result(self, model: str, challenge: str, prompt: str, iteration: int,
                   metrics_data: Dict[str, Any], code_path: str, 
                   execution_time: float, status: str = "success",
                   temperature_folder: Optional[str] = None,
                   generation_params: Optional[Dict[str, Any]] = None) -> None:
        if not self.current_experiment:
            raise RuntimeError("No active experiment")
        
        metrics = self._parse_metrics(metrics_data)
        
        result = TestResult.create_new(
            experiment_id=self.current_experiment.metadata.experiment_id,
            model=model,
            challenge=challenge,
            prompt=prompt,
            iteration=iteration,
            metrics=metrics,
            code_path=code_path,
            execution_time=execution_time,
            status=status,
            temperature_folder=temperature_folder,
            generation_params=generation_params
        )
        
        self.current_experiment.add_result(result)
    
    def finish_experiment(self) -> Path:
        if not self.current_experiment:
            raise RuntimeError("No active experiment")
        
        self.current_experiment.metadata.status = "completed"
        
        output_dir = Path(self.current_experiment.metadata.output_dir)
        
        tree_path = output_dir / "results_tree.json"
        self.current_experiment.save_tree(tree_path)
        
        flat_path = output_dir / "results_flat.json"
        self.current_experiment.save_flat(flat_path)
        
        metadata_path = output_dir / "experiment_metadata.json"
        self.current_experiment.metadata.save(metadata_path)
        
        experiment_results = self.current_experiment
        self.current_experiment = None
        
        return tree_path
    
    def _parse_metrics(self, metrics_data: Dict[str, Any]) -> TestMetrics:
        return TestMetrics(
            compilability=metrics_data.get("compilability", {}),
            code_length=metrics_data.get("code_length", {}),
            modularity=metrics_data.get("modularity", {}),
            functional_completeness=metrics_data.get("functional_completeness", {}),
            functional_correctness=metrics_data.get("functional_correctness"),
            quality=metrics_data.get("quality"),
            structure=metrics_data.get("structure"),
            test_groups_run=metrics_data.get("test_groups_run")
        )
    
    @staticmethod
    def load_experiment(experiment_dir: Path) -> ExperimentResults:
        tree_path = experiment_dir / "results_tree.json"
        return ExperimentResults.load_from_tree(tree_path)
    
    @staticmethod
    def list_experiments(base_dir: Path) -> List[Dict[str, Any]]:
        experiments = []
        
        for exp_dir in base_dir.iterdir():
            if exp_dir.is_dir() and exp_dir.name.startswith("experiment_"):
                metadata_path = exp_dir / "experiment_metadata.json"
                if metadata_path.exists():
                    metadata = ExperimentMetadata.load(metadata_path)
                    experiments.append({
                        "path": str(exp_dir),
                        "experiment_id": metadata.experiment_id,
                        "timestamp": metadata.timestamp,
                        "status": metadata.status,
                        "config": metadata.config.to_dict()
                    })
        
        return sorted(experiments, key=lambda x: x["timestamp"], reverse=True)
