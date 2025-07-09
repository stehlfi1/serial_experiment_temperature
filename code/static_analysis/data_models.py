from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from enum import Enum
import json
import uuid


class TestGroupType(Enum):
    """Test group classifications for organizing different types of quality tests."""
    LEGACY = "legacy"      # Original Renner's tests (compilability, functional_correctness)  
    QUALITY = "quality"    # Advanced quality metrics (complexity, maintainability, etc.)
    STRUCTURE = "structure" # AST-based structural analysis


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
    test_groups: Optional[List[str]] = None  # Track which test groups to run
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "models": [m.to_dict() for m in self.models],
            "challenges": self.challenges,
            "prompts": self.prompts,
            "iterations": self.iterations,
            "test_groups": self.test_groups or []
        }
    
    def get_experiment_matrix(self) -> Dict[str, Any]:
        """Get a hierarchical view of the experiment matrix"""
        matrix = {}
        for challenge in self.challenges:
            matrix[challenge] = {}
            for prompt in self.prompts:
                matrix[challenge][prompt] = {}
                for model in self.models:
                    matrix[challenge][prompt][model.name] = {
                        "temperature": model.temperature,
                        "top_p": model.top_p,
                        "top_k": model.top_k,
                        "iterations": list(range(1, self.iterations + 1))
                    }
        return matrix


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


# Enhanced metrics structure for temperature research
@dataclass
class AdvancedMetrics:
    """Comprehensive metrics for analyzing temperature impact on code quality and structure."""
    
    # === COMPLEXITY METRICS ===
    # Cyclomatic Complexity - primary metric for decision points
    cyclomatic_complexity: Optional[float] = None
    cyclomatic_complexity_per_function: Optional[List[float]] = None
    
    # Halstead metrics - operands and operators analysis
    halstead_volume: Optional[float] = None           # V = N * log2(n)
    halstead_difficulty: Optional[float] = None       # D = (n1/2) * (N2/n2)
    halstead_effort: Optional[float] = None           # E = D * V
    halstead_time: Optional[float] = None             # T = E / 18
    halstead_bugs: Optional[float] = None             # B = V / 3000
    halstead_length: Optional[int] = None             # N = N1 + N2
    halstead_vocabulary: Optional[int] = None         # n = n1 + n2
    halstead_operators: Optional[int] = None          # n1
    halstead_operands: Optional[int] = None           # n2
    halstead_operator_count: Optional[int] = None     # N1
    halstead_operand_count: Optional[int] = None      # N2
    
    # Cognitive Complexity - weighted branching and nesting
    cognitive_complexity: Optional[float] = None
    cognitive_complexity_per_function: Optional[List[float]] = None
    
    # Nesting depth - maximum level of nested blocks
    max_nesting_depth: Optional[int] = None
    avg_nesting_depth: Optional[float] = None
    nesting_depth_per_function: Optional[List[int]] = None
    
    # ABC metrics - Assignment, Branch, Condition
    abc_assignment_count: Optional[int] = None
    abc_branch_count: Optional[int] = None
    abc_condition_count: Optional[int] = None
    abc_magnitude: Optional[float] = None  # sqrt(A² + B² + C²)
    
    # Maintainability Index - composite metric
    maintainability_index: Optional[float] = None
    maintainability_rank: Optional[str] = None  # A, B, C, D based on MI score
    
    # === SIZE METRICS ===
    # Lines of Code metrics
    logical_lines_of_code: Optional[int] = None       # LLOC - executable lines
    physical_lines_of_code: Optional[int] = None      # LOC - total lines
    comment_lines: Optional[int] = None
    blank_lines: Optional[int] = None
    code_to_comment_ratio: Optional[float] = None
    
    # Function and class metrics
    function_count: Optional[int] = None
    class_count: Optional[int] = None
    method_count: Optional[int] = None
    methods_per_class: Optional[List[int]] = None
    parameters_per_function: Optional[List[int]] = None
    avg_parameters_per_function: Optional[float] = None
    
    # Weighted Methods per Class (WMC) - sum of CC for class methods
    wmc_per_class: Optional[List[float]] = None
    avg_wmc: Optional[float] = None
    
    # Import and dependency metrics
    import_count: Optional[int] = None
    from_import_count: Optional[int] = None
    unique_imports: Optional[int] = None
    stdlib_imports: Optional[int] = None
    third_party_imports: Optional[int] = None
    
    # === STRUCTURE / OOP METRICS ===
    # Inheritance metrics
    depth_of_inheritance: Optional[List[int]] = None  # DIT per class
    max_dit: Optional[int] = None
    avg_dit: Optional[float] = None
    
    # Number of Children (NOC) - direct subclasses
    children_per_class: Optional[List[int]] = None
    max_noc: Optional[int] = None
    avg_noc: Optional[float] = None
    
    # Coupling Between Objects (CBO) - classes referenced
    coupling_per_class: Optional[List[int]] = None
    max_cbo: Optional[int] = None
    avg_cbo: Optional[float] = None
    
    # === AST STRUCTURE METRICS ===
    # AST size and complexity
    ast_node_count: Optional[int] = None
    ast_depth: Optional[int] = None
    ast_node_types: Optional[Dict[str, int]] = None   # Histogram of node types
    ast_unique_node_types: Optional[int] = None
    
    # Control flow metrics
    loop_count: Optional[Dict[str, int]] = None       # {'for': x, 'while': y}
    conditional_count: Optional[Dict[str, int]] = None # {'if': x, 'try': y, 'elif': z}
    comprehension_count: Optional[Dict[str, int]] = None # {'list': x, 'dict': y, 'set': z}
    
    # Code patterns
    lambda_count: Optional[int] = None
    generator_count: Optional[int] = None
    decorator_count: Optional[int] = None
    docstring_count: Optional[int] = None
    return_statement_count: Optional[int] = None
    raise_statement_count: Optional[int] = None
    assert_statement_count: Optional[int] = None
    
    # Variable usage
    variable_count: Optional[int] = None
    global_variable_count: Optional[int] = None
    nonlocal_variable_count: Optional[int] = None
    
    # Operator usage distribution
    operator_distribution: Optional[Dict[str, int]] = None
    
    # Literal usage
    string_literal_count: Optional[int] = None
    number_literal_count: Optional[int] = None
    boolean_literal_count: Optional[int] = None
    
    # === ADDITIONAL QUALITY METRICS ===
    # Code style and formatting (can be analyzed via AST)
    naming_convention_score: Optional[float] = None
    code_duplication_ratio: Optional[float] = None
    
    # Function complexity distribution
    simple_function_ratio: Optional[float] = None     # CC <= 5
    complex_function_ratio: Optional[float] = None    # CC > 10
    very_complex_function_ratio: Optional[float] = None # CC > 20
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TestMetrics:
    # Legacy metrics (for backward compatibility)
    compilability: Dict[str, Any]
    code_length: Dict[str, Any]
    modularity: Dict[str, Any]
    functional_completeness: Dict[str, Any]
    functional_correctness: Optional[Dict[str, Any]] = None
    
    # Advanced test group results
    quality: Optional[Dict[str, Any]] = None
    structure: Optional[Dict[str, Any]] = None
    
    # New advanced metrics for temperature research
    advanced: Optional[AdvancedMetrics] = None
    test_groups_run: Optional[List[str]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        if self.advanced:
            data["advanced"] = self.advanced.to_dict()
        return data


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
    # Temperature-related fields
    temperature_folder: Optional[str] = None
    generation_params: Optional[Dict[str, Any]] = None
    
    @classmethod
    def create_new(cls, experiment_id: str, model: str, challenge: str, 
                   prompt: str, iteration: int, metrics: TestMetrics,
                   code_path: str, execution_time: float, status: str,
                   temperature_folder: Optional[str] = None,
                   generation_params: Optional[Dict[str, Any]] = None) -> "TestResult":
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
            status=status,
            temperature_folder=temperature_folder,
            generation_params=generation_params
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "result_id": self.result_id,
            "experiment_id": self.experiment_id,
            "generation_params": self.generation_params,
            "model": self.model,
            "challenge": self.challenge,
            "prompt": self.prompt,
            "iteration": self.iteration,
            "timestamp": self.timestamp,
            "metrics": self.metrics.to_dict(),
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
                            status=result_data["status"],
                            temperature_folder=result_data.get("temperature_folder"),
                            generation_params=result_data.get("generation_params")
                        )
                        experiment_results.add_result(result)
        
        return experiment_results


# Test group definitions for temperature research
@dataclass
class TestGroup:
    name: str
    description: str
    tests: List[str]
    category: str  # "legacy", "quality", "similarity", "structure"


# Predefined test groups
TEST_GROUPS = {
    "legacy": TestGroup(
        name="legacy",
        description="Original tests from Renner's work - compatibility and basic functionality",
        tests=[
            "1_code_compilability",
            "2_code_length_adaptive", 
            "3_modularity_adaptive",
            "4_functional_completeness_adaptive",
            "5_functional_correctness"  # Missing key test!
        ],
        category="legacy"
    ),
    "quality": TestGroup(
        name="quality",
        description="Advanced code quality metrics for temperature analysis",
        tests=[
            "complexity_analysis",     # CC, cognitive complexity, nesting depth
            "halstead_analysis",       # All Halstead metrics (V, D, E, T, B, etc.)
            "maintainability_analysis", # MI, ABC metrics
            "size_analysis",           # LLOC, function count, etc.
            "code_style_analysis"      # Naming conventions, duplication
        ],
        category="quality"
    ),
    "structure": TestGroup(
        name="structure",
        description="Structural analysis using AST and code organization",
        tests=[
            "ast_analysis",
            "control_flow_analysis", 
            "oop_metrics",
            "code_patterns",
            "variable_usage",
            "operator_distribution"
        ],
        category="structure"
    )
}
