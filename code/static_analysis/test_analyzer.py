from pathlib import Path
from typing import List, Dict, Any, Optional
import json

from .results.experiment_manager import ExperimentManager
from .results.data_models import ExperimentConfig, ModelInfo
from .execution.test_runner import TestRunner


def test_existing_code(base_dir: str = "dry_run_output", test_groups: List[str] = None) -> None:
    """Test generated code in the specified directory."""
    print(f"🧪 Testing generated code in: {base_dir}")
    print("-" * 50)
    
    project_root = Path(__file__).parent.parent.parent
    test_runner = TestRunner(project_root / "code" / "static_analysis" / "test_definitions")
    base_path = project_root / base_dir
    
    if not base_path.exists():
        print(f"❌ Directory {base_dir} does not exist")
        return
    
    code_base = base_path / "code"
    if not code_base.exists():
        print(f"❌ No code directory found in {base_dir}")
        return
    
    # Create experiment manager to save results
    experiment_manager = ExperimentManager(base_path / "static_analysis")
    
    # Create a test-only experiment config
    config = ExperimentConfig(
        models=[],  # Will be populated as we find code files
        challenges=[],
        prompts=[],
        iterations=0
    )
    
    models_found = []
    results_summary = []
    
    for challenge_dir in code_base.iterdir():
        if not challenge_dir.is_dir():
            continue
            
        challenge_name = challenge_dir.name
        print(f"🎯 Testing challenge: {challenge_name}")
        
        for prompt_dir in challenge_dir.iterdir():
            if not prompt_dir.is_dir():
                continue
                
            prompt_name = prompt_dir.name
            print(f"  📝 Prompt: {prompt_name}")
            
            # Handle temperature folder structure: prompt_dir/temp_X.X/iteration_Y
            for temp_or_iter_dir in prompt_dir.iterdir():
                if not temp_or_iter_dir.is_dir():
                    continue
                
                # Check if this is a temperature folder (temp_X.X) or direct iteration folder
                if temp_or_iter_dir.name.startswith("temp_"):
                    temp_folder_name = temp_or_iter_dir.name
                    print(f"    🌡️  Temperature: {temp_folder_name}")
                    
                    # Look for iterations inside temperature folder
                    for iteration_dir in temp_or_iter_dir.iterdir():
                        if not iteration_dir.is_dir() or not iteration_dir.name.startswith("iteration_"):
                            continue
                            
                        iteration_num = int(iteration_dir.name.split("_")[1])
                        iteration = iteration_dir.name
                        print(f"      🔄 {iteration}")
                        
                        # Extract temperature parameters from generation_params.json
                        generation_params = {}
                        params_file = iteration_dir / "generation_params.json"
                        if params_file.exists():
                            try:
                                with open(params_file, 'r') as f:
                                    generation_params = json.load(f)
                            except Exception:
                                pass
                        
                        results_summary.extend(_test_iteration_files(
                            iteration_dir, challenge_name, prompt_name, 
                            iteration_num, temp_folder_name, generation_params, 
                            test_runner, test_groups, models_found
                        ))
                
                elif temp_or_iter_dir.name.startswith("iteration_"):
                    # Legacy structure: direct iteration folders under prompt
                    iteration_dir = temp_or_iter_dir
                    iteration_num = int(iteration_dir.name.split("_")[1])
                    iteration = iteration_dir.name
                    print(f"    🔄 {iteration}")
                    
                    results_summary.extend(_test_iteration_files(
                        iteration_dir, challenge_name, prompt_name, 
                        iteration_num, None, {}, 
                        test_runner, test_groups, models_found
                    ))
    
    # Update config with found data - extract unique model+temperature combinations
    unique_models = _build_unique_models_config(results_summary)
    
    config.models = list(unique_models.values())
    config.challenges = list(set([r["challenge"] for r in results_summary]))
    config.prompts = list(set([r["prompt"] for r in results_summary]))
    config.iterations = max([r["iteration"] for r in results_summary]) if results_summary else 0
    
    # Start experiment to save results
    metadata = experiment_manager.start_experiment(config)
    
    # Add all results to experiment
    for result in results_summary:
        experiment_manager.add_result(
            model=result["model"],
            challenge=result["challenge"],
            prompt=result["prompt"],
            iteration=result["iteration"],
            metrics_data=result["metrics"],
            code_path=result["code_path"],
            execution_time=0,  # Not tracked for post-hoc testing
            status=result["status"],
            temperature_folder=result.get("temperature_folder"),
            generation_params=result.get("generation_params")
        )
    
    # Save experiment results
    results_path = experiment_manager.finish_experiment()
    
    _print_test_summary(results_summary, results_path, metadata.experiment_id)


def _test_iteration_files(iteration_dir: Path, challenge_name: str, prompt_name: str, iteration_num: int,
                         temp_folder_name: Optional[str], generation_params: Dict[str, Any],
                         test_runner: TestRunner, test_groups: List[str], 
                         models_found: List[str]) -> List[Dict[str, Any]]:
    """Test all Python files in an iteration directory."""
    results = []
    
    for code_file in iteration_dir.glob("*.py"):
        if code_file.name == "generation_params.json":
            continue
            
        model_name = code_file.stem
        print(f"        🤖 Testing {model_name}...")
        
        if model_name not in models_found:
            models_found.append(model_name)
        
        try:
            test_results = test_runner.run_all_tests_for_model(
                model_name, iteration_dir, challenge_name, test_groups or ["legacy"]
            )
            
            metrics_data = _extract_metrics_from_tests(test_results, test_groups)
            
            print(f"          ✅ Tests completed")
            print(f"             📊 Metrics: {len([k for k, v in metrics_data.items() if v])} categories analyzed")
            
            # Extract model-specific temperature params
            model_params = generation_params.get("models", {}).get(model_name, {})
            
            result = {
                "model": model_name,
                "challenge": challenge_name,
                "prompt": prompt_name,
                "iteration": iteration_num,
                "metrics": metrics_data,
                "status": "success",
                "code_path": str(code_file)
            }
            
            if temp_folder_name:
                result["temperature_folder"] = temp_folder_name
                result["generation_params"] = {
                    "temperature": model_params.get("temperature"),
                    "top_k": model_params.get("top_k"),
                    "top_p": model_params.get("top_p"),
                    "model_id": model_params.get("model_id"),
                    "provider": model_params.get("provider")
                }
            
            results.append(result)
            
        except Exception as e:
            print(f"          ❌ Error: {str(e)}")
            
            model_params = generation_params.get("models", {}).get(model_name, {})
            
            result = {
                "model": model_name,
                "challenge": challenge_name,
                "prompt": prompt_name,
                "iteration": iteration_num,
                "metrics": {},
                "status": "failed",
                "error": str(e),
                "code_path": str(code_file)
            }
            
            if temp_folder_name:
                result["temperature_folder"] = temp_folder_name
                result["generation_params"] = {
                    "temperature": model_params.get("temperature"),
                    "top_k": model_params.get("top_k"),
                    "top_p": model_params.get("top_p"),
                    "model_id": model_params.get("model_id"),
                    "provider": model_params.get("provider")
                }
            
            results.append(result)
    
    return results


def _extract_metrics_from_tests(test_results: Dict[str, Any], test_groups: List[str]) -> Dict[str, Any]:
    """Extract metrics data from test results based on test groups."""
    metrics_data = {}
    
    # Legacy test results (backward compatibility)
    if "legacy" in (test_groups or ["legacy"]):
        legacy_results = test_results.get("legacy", {})
        metrics_data.update({
            "compilability": legacy_results.get("1_code_compilability", {}),
            "code_length": legacy_results.get("2_code_length_adaptive", {}),
            "modularity": legacy_results.get("3_modularity_adaptive", {}),
            "functional_completeness": legacy_results.get("4_functional_completeness_adaptive", {}),
            "functional_correctness": legacy_results.get("5_functional_correctness", {})
        })
    
    # Advanced test results
    if "quality" in (test_groups or []):
        metrics_data["quality"] = test_results.get("quality", {})
    
    if "structure" in (test_groups or []):
        metrics_data["structure"] = test_results.get("structure", {})
    
    return metrics_data


def _build_unique_models_config(results_summary: List[Dict[str, Any]]) -> Dict[str, ModelInfo]:
    """Build unique model configurations from results."""
    unique_models = {}
    
    for result in results_summary:
        model_name = result["model"]
        gen_params = result.get("generation_params", {})
        if gen_params:
            temp = gen_params.get("temperature")
            top_k = gen_params.get("top_k")
            top_p = gen_params.get("top_p")
            # Create unique key for model+temperature combination
            key = f"{model_name}_temp_{temp}"
            if top_k is not None:
                key += f"_topk_{top_k}"
            if top_p is not None:
                key += f"_topp_{top_p}"
            
            if key not in unique_models:
                unique_models[key] = ModelInfo(
                    name=model_name,
                    provider=gen_params.get("provider", "unknown"),
                    model_id=gen_params.get("model_id", "unknown"),
                    temperature=temp,
                    top_k=top_k,
                    top_p=top_p
                )
    
    return unique_models


def _print_test_summary(results_summary: List[Dict[str, Any]], results_path: Path, experiment_id: str) -> None:
    """Print test summary statistics."""
    print(f"\n📊 Test Summary: {len(results_summary)} tests completed")
    successful = len([r for r in results_summary if r["status"] == "success"])
    failed = len(results_summary) - successful
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"\n💾 Results saved to: {results_path}")
    print(f"📋 Experiment ID: {experiment_id}")