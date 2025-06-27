#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from code.experiment.experiment_manager import ExperimentManager
from code.experiment.analyzer import ExperimentAnalyzer


def list_experiments(base_dir: Path):
    experiments = ExperimentManager.list_experiments(base_dir)
    
    if not experiments:
        print("No experiments found.")
        return
    
    print("📋 Available Experiments:")
    print("-" * 80)
    
    for exp in experiments:
        print(f"ID: {exp['experiment_id'][:8]}...")
        print(f"Timestamp: {exp['timestamp']}")
        print(f"Status: {exp['status']}")
        print(f"Config: {exp['config']['models']} | {exp['config']['challenges']} | {exp['config']['prompts']}")
        print(f"Path: {exp['path']}")
        print("-" * 80)


def analyze_experiment(experiment_path: Path, output_dir: Path = None):
    if not experiment_path.exists():
        print(f"Experiment path does not exist: {experiment_path}")
        return 1
    
    try:
        experiment = ExperimentManager.load_experiment(experiment_path)
        analyzer = ExperimentAnalyzer(experiment)
        
        print("📊 Experiment Analysis")
        print("=" * 50)
        
        print("\n🤖 Summary by Model:")
        print(analyzer.summary_by_model())
        
        print("\n📝 Summary by Prompt:")
        print(analyzer.summary_by_prompt())
        
        print("\n🏆 Best Performers:")
        best = analyzer.get_best_performers()
        for category, data in best.items():
            print(f"  {category}: {data}")
        
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            files = analyzer.export_for_latex(output_dir)
            print(f"\n💾 Exported files to {output_dir}:")
            for name, path in files.items():
                print(f"  {name}: {path}")
        
        return 0
        
    except Exception as e:
        print(f"Failed to analyze experiment: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description="Experiment Management CLI")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    list_parser = subparsers.add_parser("list", help="List all experiments")
    list_parser.add_argument("--base-dir", type=Path, default=Path.cwd() / "dry_run_output",
                            help="Base directory containing experiments")
    
    analyze_parser = subparsers.add_parser("analyze", help="Analyze an experiment")
    analyze_parser.add_argument("experiment_path", type=Path, help="Path to experiment directory")
    analyze_parser.add_argument("--output", type=Path, help="Output directory for exported files")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_experiments(args.base_dir)
        return 0
    elif args.command == "analyze":
        return analyze_experiment(args.experiment_path, args.output)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
