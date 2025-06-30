import argparse
from pathlib import Path
from typing import Optional, List
import sys
import time

sys.path.append(str(Path(__file__).parent.parent))

from config import (
    LLMS, 
    CHALLENGES, 
    DRY_RUN_CHALLENGE,
    DRY_RUN_PROMPT,
    DRY_RUN_ITERATIONS,
    DRY_RUN_OUTPUT_DIR
)
from helpers import extract_python_code
from experiment.experiment_manager import ExperimentManager
from experiment.data_models import ExperimentConfig, ModelInfo
from experiment.test_runner import TestRunner


def _create_output_directories(base_dir: str, challenge_name: str, prompt_name: str, iteration: int) -> tuple[str, str]:
    project_root = Path(__file__).parent.parent.parent
    code_dir = project_root / base_dir / "code" / challenge_name / prompt_name / f"iteration_{iteration}"
    response_dir = project_root / base_dir / "response" / challenge_name / prompt_name / f"iteration_{iteration}"
    
    code_dir.mkdir(parents=True, exist_ok=True)
    response_dir.mkdir(parents=True, exist_ok=True)
    
    return str(code_dir), str(response_dir)


def _write_llm_output(code_dir: str, response_dir: str, llm_name: str, response_content: str) -> None:
    response_file = Path(response_dir) / f"{llm_name}_response.txt"
    with open(response_file, "w", encoding="utf-8") as f:
        f.write(response_content)
    
    code_file = Path(code_dir) / f"{llm_name}.py"
    with open(code_file, "w", encoding="utf-8") as f:
        f.write(extract_python_code(response_content))


def _find_challenge_and_prompt(challenge_name: str, prompt_name: str) -> tuple[Optional[object], Optional[object]]:
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


def create_llms_with_temperature(temperature: float) -> list:
    from config import LLMS
    from llm import Llm
    return [
        Llm(llm.model, llm.name, temperature=temperature)
        for llm in LLMS
    ]


def dry_run_generation(challenge_name: str, prompt_name: str, iterations: int = 1, temperature: float = 0.7, test_groups: List[str] = None) -> None:
    llms = create_llms_with_temperature(temperature)
    
    print(f"🧪 Starting dry run: {challenge_name} - {prompt_name}")
    print(f"📁 Output directory: {DRY_RUN_OUTPUT_DIR}")
    print(f"🔄 Iterations: {iterations}")
    print(f"🌡️  Temperature: {temperature}")
    print(f"🤖 LLMs: {', '.join(llm.name for llm in llms)}")
    print("-" * 50)
    
    challenge, prompt = _find_challenge_and_prompt(challenge_name, prompt_name)
    
    if not challenge:
        raise ValueError(f"Challenge '{challenge_name}' not found. Available: {[c.name for c in CHALLENGES]}")
    
    if not prompt:
        available_prompts = [p.name for p in challenge.prompts]
        raise ValueError(f"Prompt '{prompt_name}' not found in challenge '{challenge_name}'. Available: {available_prompts}")
    
    project_root = Path(__file__).parent.parent.parent
    experiment_manager = ExperimentManager(project_root / DRY_RUN_OUTPUT_DIR)
    test_runner = TestRunner(project_root / "code" / "tests")
    
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
    
    for llm in llms:
        for i in range(1, iterations + 1):
            code_dir, response_dir = _create_output_directories(
                DRY_RUN_OUTPUT_DIR, challenge.name, prompt.name, i
            )
            
            print(f"🔄 Generating: {challenge.name} - {prompt.name} - iteration [{i}] ({llm.name})")
            
            try:
                start_time = time.time()
                answer = llm.query(prompt.prompt)
                response_content = answer.choices[0].message.content
                generation_time = time.time() - start_time
                
                _write_llm_output(code_dir, response_dir, llm.name, response_content)
                
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


def test_generated_code(base_dir: str = "dry_run_output", test_groups: List[str] = None) -> None:
    print(f"🧪 Testing generated code in: {base_dir}")
    print("-" * 50)
    
    project_root = Path(__file__).parent.parent.parent
    test_runner = TestRunner(project_root / "code" / "tests")
    base_path = project_root / base_dir
    
    if not base_path.exists():
        print(f"❌ Directory {base_dir} does not exist")
        return
    
    code_base = base_path / "code"
    if not code_base.exists():
        print(f"❌ No code directory found in {base_dir}")
        return
    
    # Create experiment manager to save results
    experiment_manager = ExperimentManager(base_path)
    
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
            
            for iteration_dir in prompt_dir.iterdir():
                if not iteration_dir.is_dir() or not iteration_dir.name.startswith("iteration_"):
                    continue
                    
                iteration_num = int(iteration_dir.name.split("_")[1])
                iteration = iteration_dir.name
                print(f"    🔄 {iteration}")
                
                for code_file in iteration_dir.glob("*.py"):
                    model_name = code_file.stem
                    print(f"      🤖 Testing {model_name}...")
                    
                    if model_name not in models_found:
                        models_found.append(model_name)
                    
                    try:
                        test_results = test_runner.run_all_tests_for_model(
                            model_name, iteration_dir, challenge_name, test_groups or ["legacy"]
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
                        
                        print(f"        ✅ Tests completed")
                        print(f"           📊 Metrics: {len([k for k, v in metrics_data.items() if v])} categories analyzed")
                        
                        results_summary.append({
                            "model": model_name,
                            "challenge": challenge_name,
                            "prompt": prompt_name,
                            "iteration": iteration_num,
                            "metrics": metrics_data,
                            "status": "success",
                            "code_path": str(code_file)
                        })
                        
                    except Exception as e:
                        print(f"        ❌ Error: {str(e)}")
                        results_summary.append({
                            "model": model_name,
                            "challenge": challenge_name,
                            "prompt": prompt_name,
                            "iteration": iteration_num,
                            "metrics": {},
                            "status": "failed",
                            "error": str(e),
                            "code_path": str(code_file)
                        })
    
    # Update config with found data
    config.models = [ModelInfo(name=model, provider="unknown", model_id="unknown") for model in models_found]
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
            status=result["status"]
        )
    
    # Save experiment results
    results_path = experiment_manager.finish_experiment()
    
    print(f"\n📊 Test Summary: {len(results_summary)} tests completed")
    successful = len([r for r in results_summary if r["status"] == "success"])
    failed = len(results_summary) - successful
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"\n💾 Results saved to: {results_path}")
    print(f"📋 Experiment ID: {metadata.experiment_id}")


def generate_only(challenge_name: str, prompt_name: str, iterations: int = 1, temperature: float = 0.7, base_dir: str = "dry_run_output") -> None:
    llms = create_llms_with_temperature(temperature)
    
    print(f"🚀 Generating code: {challenge_name} - {prompt_name}")
    print(f"📁 Output directory: {base_dir}")
    print(f"🔄 Iterations: {iterations}")
    print(f"🌡️  Temperature: {temperature}")
    print(f"🤖 LLMs: {', '.join(llm.name for llm in llms)}")
    print("-" * 50)
    
    challenge, prompt = _find_challenge_and_prompt(challenge_name, prompt_name)
    
    if not challenge:
        raise ValueError(f"Challenge '{challenge_name}' not found. Available: {[c.name for c in CHALLENGES]}")
    
    if not prompt:
        available_prompts = [p.name for p in challenge.prompts]
        raise ValueError(f"Prompt '{prompt_name}' not found in challenge '{challenge_name}'. Available: {available_prompts}")
    
    for llm in llms:
        for i in range(1, iterations + 1):
            code_dir, response_dir = _create_output_directories(
                base_dir, challenge.name, prompt.name, i
            )
            
            print(f"🔄 Generating: {challenge.name} - {prompt.name} - iteration [{i}] ({llm.name})")
            
            try:
                start_time = time.time()
                answer = llm.query(prompt.prompt)
                response_content = answer.choices[0].message.content
                generation_time = time.time() - start_time
                
                _write_llm_output(code_dir, response_dir, llm.name, response_content)
                
                print(f"✅ Generated: {llm.name} (took {generation_time:.2f}s)")
                
            except Exception as e:
                print(f"❌ Error with {llm.name}: {str(e)}")
                continue
    
    print(f"\n🎉 Code generation completed!")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate and test code using LLMs for quality comparison research",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate code only')
    gen_parser.add_argument(
        "--challenge",
        type=str,
        choices=[c.name for c in CHALLENGES],
        default=DRY_RUN_CHALLENGE,
        help=f"Challenge to use (default: {DRY_RUN_CHALLENGE})"
    )
    gen_parser.add_argument(
        "--prompt",
        type=str,
        default=DRY_RUN_PROMPT,
        help=f"Prompt to use (default: {DRY_RUN_PROMPT})"
    )
    gen_parser.add_argument(
        "--iterations",
        type=int,
        default=DRY_RUN_ITERATIONS,
        help=f"Number of iterations (default: {DRY_RUN_ITERATIONS})"
    )
    gen_parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.8,
        help="Temperature for generation (default: 0.8)"
    )
    gen_parser.add_argument(
        "--output-dir",
        type=str,
        default=DRY_RUN_OUTPUT_DIR,
        help=f"Output directory (default: {DRY_RUN_OUTPUT_DIR})"
    )
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Test existing generated code')
    test_parser.add_argument(
        "--input-dir",
        type=str,
        default=DRY_RUN_OUTPUT_DIR,
        help=f"Directory containing generated code (default: {DRY_RUN_OUTPUT_DIR})"
    )
    test_parser.add_argument(
        "--test-groups",
        nargs="*",
        choices=["legacy", "quality", "structure"],
        default=["legacy"],
        help="Test groups to run (default: legacy). Options: legacy, quality, structure"
    )
    
    # Full command (generate + test)
    full_parser = subparsers.add_parser('full', help='Generate code and run tests')
    full_parser.add_argument(
        "--challenge",
        type=str,
        choices=[c.name for c in CHALLENGES],
        default=DRY_RUN_CHALLENGE,
        help=f"Challenge to use (default: {DRY_RUN_CHALLENGE})"
    )
    full_parser.add_argument(
        "--prompt",
        type=str,
        default=DRY_RUN_PROMPT,
        help=f"Prompt to use (default: {DRY_RUN_PROMPT})"
    )
    full_parser.add_argument(
        "--iterations",
        type=int,
        default=DRY_RUN_ITERATIONS,
        help=f"Number of iterations (default: {DRY_RUN_ITERATIONS})"
    )
    full_parser.add_argument(
        "-t", "--temperature",
        type=float,
        default=0.8,
        help="Temperature for generation (default: 0.8)"
    )
    full_parser.add_argument(
        "--test-groups",
        nargs="*",
        choices=["legacy", "quality", "structure"],
        default=["legacy"],
        help="Test groups to run (default: legacy). Options: legacy, quality, structure"
    )
    
    args = parser.parse_args()
    
    if args.command == 'generate':
        generate_only(args.challenge, args.prompt, args.iterations, args.temperature, args.output_dir)
    elif args.command == 'test':
        test_generated_code(args.input_dir, getattr(args, 'test_groups', ['legacy']))
    elif args.command == 'full':
        dry_run_generation(args.challenge, args.prompt, args.iterations, args.temperature, getattr(args, 'test_groups', ['legacy']))
    else:
        parser.print_help()
        print("\n❌ Please specify a command: generate, test, or full")
        sys.exit(1)


if __name__ == "__main__":
    main()
