from pathlib import Path
from typing import Optional, List
import time

from .config import CHALLENGES
from .llm import Llm
from .utils import (
    create_temp_folder_name, get_iteration_range, create_output_directories,
    write_generation_metadata, write_llm_output
)


def find_challenge_and_prompt(challenge_name: str, prompt_name: str) -> tuple[Optional[object], Optional[object]]:
    """Find challenge and prompt objects by name."""
    target_challenge = None
    target_prompt = None
    
    for challenge in CHALLENGES:
        if challenge.name == challenge_name:
            target_challenge = challenge
            for prompt in challenge.prompts:
                if prompt.name == prompt_name:
                    target_prompt = prompt
                    break
            break
    
    return target_challenge, target_prompt


def create_llms_with_temperature(temperature: float, top_k: int = None, top_p: float = None) -> list:
    """Create LLM instances with specified temperature and sampling parameters."""
    from .config import LLMS
    return [
        Llm(llm.model, llm.name, temperature=temperature, top_k=top_k, top_p=top_p)
        for llm in LLMS
    ]


def generate_code_only(challenge_name: str, prompt_name: str, iterations: int = 1, 
                      temperature: float = 1.0, base_dir: str = "dry_run_output", 
                      top_k: int = None, top_p: float = None) -> None:
    """Generate code without running tests."""
    llms = create_llms_with_temperature(temperature, top_k, top_p)
    
    print(f"🚀 Generating code: {challenge_name} - {prompt_name}")
    print(f"📁 Output directory: {base_dir}")
    print(f"🔄 Iterations: {iterations}")
    print(f"🌡️  Temperature: {temperature}")
    print(f"🤖 LLMs: {', '.join(llm.name for llm in llms)}")
    print("-" * 50)
    
    challenge, prompt = find_challenge_and_prompt(challenge_name, prompt_name)
    
    if not challenge:
        raise ValueError(f"Challenge '{challenge_name}' not found. Available: {[c.name for c in CHALLENGES]}")
    
    if not prompt:
        available_prompts = [p.name for p in challenge.prompts]
        raise ValueError(f"Prompt '{prompt_name}' not found in challenge '{challenge_name}'. Available: {available_prompts}")
    
    # Calculate iteration range using auto-indexing
    project_root = Path(__file__).parent.parent.parent
    temp_folder = create_temp_folder_name(temperature, llms[0].top_k, llms[0].top_p)
    temp_folder_path = project_root / base_dir / "code" / challenge.name / prompt.name / temp_folder
    iteration_range = get_iteration_range(temp_folder_path, iterations)
    
    print(f"📝 Will create iterations: {list(iteration_range)}")
    
    for llm in llms:
        for i in iteration_range:
            code_dir, response_dir = create_output_directories(
                base_dir, challenge.name, prompt.name, i, temperature, llm.top_k, llm.top_p
            )
            
            # Write metadata on first model for this iteration
            if llm == llms[0]:
                write_generation_metadata(code_dir, llms, temperature, llm.top_k, llm.top_p)
            
            print(f"🔄 Generating: {challenge.name} - {prompt.name} - iteration [{i}] ({llm.name})")
            
            try:
                start_time = time.time()
                answer = llm.query(prompt.prompt)
                response_content = answer.choices[0].message.content
                generation_time = time.time() - start_time
                
                write_llm_output(code_dir, response_dir, llm.name, response_content)
                
                print(f"✅ Generated: {llm.name} (took {generation_time:.2f}s)")
                
            except Exception as e:
                print(f"❌ Error with {llm.name}: {str(e)}")
                continue
    
    print(f"\n🎉 Code generation completed!")


def dry_run_with_tests(challenge_name: str, prompt_name: str, iterations: int = 1, 
                      temperature: float = 1.0, test_groups: List[str] = None, 
                      top_k: int = None, top_p: float = None, 
                      base_dir: str = "dry_run_output") -> None:
    """Generate code and run tests in one command."""
    from ..static_analysis.results.experiment_manager import ExperimentManager
    from ..static_analysis.results.data_models import ExperimentConfig, ModelInfo
    from ..static_analysis.execution.test_runner import TestRunner
    
    llms = create_llms_with_temperature(temperature, top_k, top_p)
    
    print(f"🧪 Starting dry run: {challenge_name} - {prompt_name}")
    print(f"📁 Output directory: {base_dir}")
    print(f"🔄 Iterations: {iterations}")
    print(f"🌡️  Temperature: {temperature}")
    print(f"🤖 LLMs: {', '.join(llm.name for llm in llms)}")
    print("-" * 50)
    
    challenge, prompt = find_challenge_and_prompt(challenge_name, prompt_name)
    
    if not challenge:
        raise ValueError(f"Challenge '{challenge_name}' not found. Available: {[c.name for c in CHALLENGES]}")
    
    if not prompt:
        available_prompts = [p.name for p in challenge.prompts]
        raise ValueError(f"Prompt '{prompt_name}' not found in challenge '{challenge_name}'. Available: {available_prompts}")
    
    project_root = Path(__file__).parent.parent.parent
    experiment_manager = ExperimentManager(project_root / base_dir / "static_analysis")
    test_runner = TestRunner(project_root / "code" / "static_analysis" / "test_definitions")
    
    config = ExperimentConfig(
        models=[ModelInfo(
            name=llm.name,
            provider=llm.model.split('/')[0],
            model_id=llm.model,
            temperature=temperature
        ) for llm in llms],
        challenges=[challenge_name],
        prompts=[prompt_name],
        iterations=iterations
    )

    metadata = experiment_manager.start_experiment(config)
    print(f"📋 Experiment ID: {metadata.experiment_id}")
    
    # Calculate iteration range using auto-indexing
    temp_folder = create_temp_folder_name(temperature, llms[0].top_k, llms[0].top_p)
    temp_folder_path = project_root / base_dir / "code" / challenge.name / prompt.name / temp_folder
    iteration_range = get_iteration_range(temp_folder_path, iterations)
    
    print(f"📝 Will create iterations: {list(iteration_range)}")
    
    for llm in llms:
        for i in iteration_range:
            code_dir, response_dir = create_output_directories(
                base_dir, challenge.name, prompt.name, i, temperature, llm.top_k, llm.top_p
            )
            
            # Write metadata on first model for this iteration
            if llm == llms[0]:
                write_generation_metadata(code_dir, llms, temperature, llm.top_k, llm.top_p)
            
            print(f"🔄 Generating: {challenge.name} - {prompt.name} - iteration [{i}] ({llm.name})")
            
            try:
                start_time = time.time()
                answer = llm.query(prompt.prompt)
                response_content = answer.choices[0].message.content
                generation_time = time.time() - start_time
                
                write_llm_output(code_dir, response_dir, llm.name, response_content)
                
                code_path = Path(code_dir) / f"{llm.name}.py"
                
                test_results = test_runner.run_all_tests_for_model(
                    llm.name, Path(code_dir), challenge.name, test_groups or ["legacy"]
                )
                
                # Extract metrics based on test groups run
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
                
                experiment_manager.add_result(
                    model=llm.name,
                    challenge=challenge.name,
                    prompt=prompt.name,
                    iteration=i,
                    metrics_data=metrics_data,
                    code_path=str(code_path),
                    execution_time=generation_time,
                    status="success"
                )
                
                print(f"✅ Completed: {llm.name}")
                
            except Exception as e:
                print(f"❌ Error with {llm.name}: {str(e)}")
                
                experiment_manager.add_result(
                    model=llm.name,
                    challenge=challenge.name,
                    prompt=prompt.name,
                    iteration=i,
                    metrics_data={},
                    code_path="",
                    execution_time=0,
                    status="failed"
                )
                continue
    
    results_path = experiment_manager.finish_experiment()
    print(f"\n🎉 Dry run completed! Results saved to: {results_path}")