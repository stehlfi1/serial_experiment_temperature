#!/usr/bin/env python3
"""
Quick dry run helper script for testing LLM code generation.

This script provides a simple interface to run dry tests without having to remember
all the command line arguments.
"""

import subprocess
import sys
from pathlib import Path


def run_dry_test(challenge: str = "calculator", prompt: str = "1-zero_shot", iterations: int = 1) -> None:
    """
    Run a dry test with specified parameters.
    
    Args:
        challenge: Challenge to test (calculator, ascii_art, todo_list)
        prompt: Prompt type to use
        iterations: Number of iterations to run
    """
    cmd = [
        sys.executable, "main.py", 
        "--dry-run",
        "--challenge", challenge,
        "--prompt", prompt,
        "--iterations", str(iterations)
    ]
    
    print(f"🚀 Running dry test: {challenge} - {prompt} ({iterations} iterations)")
    print(f"📝 Command: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Dry test failed with exit code {e.returncode}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️  Dry test interrupted by user")
        sys.exit(1)


def main() -> None:
    """Interactive dry test runner."""
    print("🧪 LLM Code Generation - Quick Dry Test")
    print("=" * 50)
    
    # Available options
    challenges = ["calculator", "ascii_art", "todo_list"]
    prompts = [
        "1-zero_shot", "2-few_shot", 
        "3-chain_of_thoughts-zero_shot", "4-chain_of_thoughts-few_shot",
        "5-role-zero_shot", "6-role-few_shot"
    ]
    
    # Get user input
    print(f"Available challenges: {', '.join(challenges)}")
    challenge = input(f"Select challenge (default: calculator): ").strip() or "calculator"
    
    if challenge not in challenges:
        print(f"❌ Invalid challenge. Using 'calculator'")
        challenge = "calculator"
    
    print(f"\nAvailable prompts: {', '.join(prompts)}")
    prompt = input(f"Select prompt (default: 1-zero_shot): ").strip() or "1-zero_shot"
    
    try:
        iterations = int(input("Number of iterations (default: 1): ").strip() or "1")
        if iterations < 1:
            iterations = 1
    except ValueError:
        iterations = 1
    
    print(f"\n📋 Configuration:")
    print(f"   Challenge: {challenge}")
    print(f"   Prompt: {prompt}")
    print(f"   Iterations: {iterations}")
    
    confirm = input("\nProceed? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        run_dry_test(challenge, prompt, iterations)
    else:
        print("🚫 Dry test cancelled")


if __name__ == "__main__":
    main()
