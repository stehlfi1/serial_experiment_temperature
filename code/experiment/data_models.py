from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import uuid


@dataclass
class ModelInfo:
    name: str
    provider: str
    model_id: str
    temperature: float = 0.7
    top_p: Optional[float] = None
    top_k: Optional[int] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ExperimentConfig:
    models: List[ModelInfo]
    challenges: List[str] 
    prompts: List[str]
    iterations: int
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "models": [m.to_dict() for m in self.models],
            "challenges": self.challenges,
            "prompts": self.prompts,
            "iterations": self.iterations
        }


@dataclass
class ExperimentMetadata:
    experiment_id: str
    timestamp: str
    config: ExperimentConfig
    output_dir: str
    status: str = "running"
    
    @classmethod
    def create_new(cls, config: ExperimentConfig, output_dir: str) -> "ExperimentMetadata":
        return cls(
            experiment_id=str(uuid.uuid4()),
            timestamp=datetime.now().isoformat(),
            config=config,
            output_dir=output_dir
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "timestamp": self.timestamp,
            "config": self.config.to_dict(),
            "output_dir": self.output_dir,
            "status": self.status
        }
    
    def save(self, path: Path) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load(cls, path: Path) -> "ExperimentMetadata":
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        models = [ModelInfo(**m) for m in data["config"]["models"]]
        config = ExperimentConfig(
            models=models,
            challenges=data["config"]["challenges"],
            prompts=data["config"]["prompts"],
            iterations=data["config"]["iterations"]
        )
        return cls(
            experiment_id=data["experiment_id"],
            timestamp=data["timestamp"],
            config=config,
            output_dir=data["output_dir"],
            status=data.get("status", "unknown")
        )


@dataclass
class TestMetrics:
    compilability: Dict[str, Any]
    code_length: Dict[str, Any]
    modularity: Dict[str, Any]
    functional_completeness: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TestResult:
    result_id: str
    experiment_id: str
    model: str
    challenge: str
    prompt: str
    iteration: int
    timestamp: str
    metrics: TestMetrics
    code_path: str
    execution_time: float
    status: str
    
    @classmethod
    def create_new(cls, experiment_id: str, model: str, challenge: str, 
                   prompt: str, iteration: int, metrics: TestMetrics,
                   code_path: str, execution_time: float, status: str) -> "TestResult":
        return cls(
            result_id=str(uuid.uuid4()),
            experiment_id=experiment_id,
            model=model,
            challenge=challenge,
            prompt=prompt,
            iteration=iteration,
            timestamp=datetime.now().isoformat(),
            metrics=metrics,
            code_path=code_path,
            execution_time=execution_time,
            status=status
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "experiment_id": self.experiment_id,
            "model": self.model,
            "challenge": self.challenge,
            "prompt": self.prompt,
            "iteration": self.iteration,
            "timestamp": self.timestamp,
            "metrics": self.metrics.to_dict(),
            "code_path": self.code_path,
            "execution_time": self.execution_time,
            "status": self.status
        }


class ExperimentResults:
    def __init__(self, metadata: ExperimentMetadata):
        self.metadata = metadata
        self.results: List[TestResult] = []
    
    def add_result(self, result: TestResult) -> None:
        self.results.append(result)
    
    def to_tree_structure(self) -> Dict[str, Any]:
        tree = {
            "metadata": self.metadata.to_dict(),
            "results": {}
        }
        
        for result in self.results:
            challenge = result.challenge
            prompt = result.prompt
            iteration = result.iteration
            model = result.model
            
            if challenge not in tree["results"]:
                tree["results"][challenge] = {}
            if prompt not in tree["results"][challenge]:
                tree["results"][challenge][prompt] = {}
            if iteration not in tree["results"][challenge][prompt]:
                tree["results"][challenge][prompt][iteration] = {}
            
            tree["results"][challenge][prompt][iteration][model] = result.to_dict()
        
        return tree
    
    def to_flat_structure(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "results": [result.to_dict() for result in self.results]
        }
    
    def save_tree(self, path: Path) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_tree_structure(), f, indent=2, ensure_ascii=False)
    
    def save_flat(self, path: Path) -> None:
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_flat_structure(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_tree(cls, path: Path) -> "ExperimentResults":
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        models = [ModelInfo(**m) for m in data["metadata"]["config"]["models"]]
        config = ExperimentConfig(
            models=models,
            challenges=data["metadata"]["config"]["challenges"],
            prompts=data["metadata"]["config"]["prompts"],
            iterations=data["metadata"]["config"]["iterations"]
        )
        metadata = ExperimentMetadata(
            experiment_id=data["metadata"]["experiment_id"],
            timestamp=data["metadata"]["timestamp"],
            config=config,
            output_dir=data["metadata"]["output_dir"],
            status=data["metadata"].get("status", "unknown")
        )
        
        experiment_results = cls(metadata)
        
        for challenge, prompts in data["results"].items():
            for prompt, iterations in prompts.items():
                for iteration, models in iterations.items():
                    for model, result_data in models.items():
                        metrics = TestMetrics(**result_data["metrics"])
                        result = TestResult(
                            result_id=result_data["result_id"],
                            experiment_id=result_data["experiment_id"],
                            model=result_data["model"],
                            challenge=result_data["challenge"],
                            prompt=result_data["prompt"],
                            iteration=result_data["iteration"],
                            timestamp=result_data["timestamp"],
                            metrics=metrics,
                            code_path=result_data["code_path"],
                            execution_time=result_data["execution_time"],
                            status=result_data["status"]
                        )
                        experiment_results.add_result(result)
        
        return experiment_results
