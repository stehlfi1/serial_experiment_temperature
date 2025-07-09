import argparse
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from generation.config import (
    CHALLENGES, 
    DRY_RUN_CHALLENGE,
    DRY_RUN_PROMPT,
    DRY_RUN_ITERATIONS,
    DRY_RUN_OUTPUT_DIR
)
from generation.generator import generate_code_only, dry_run_with_tests
from static_analysis.test_analyzer import test_existing_code
from similarity_analysis.runner import run_similarity_analysis


def require_sudo():
    """Check if running with sudo privileges for restricted commands."""
    if os.geteuid() != 0:
        print("❌ Error: This command requires sudo privileges")
        print("   Run with: sudo uv run python main.py generate ...")
        print("   Or:       sudo uv run python main.py full ...")
        sys.exit(1)


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
        default=1.0,
        help="Temperature for generation (default: 1.0)"
    )
    gen_parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Top-k sampling parameter (optional)"
    )
    gen_parser.add_argument(
        "--top-p", 
        type=float,
        default=None,
        help="Top-p (nucleus) sampling parameter (optional)"
    )
    gen_parser.add_argument(
        "--output-dir",
        type=str,
        default=DRY_RUN_OUTPUT_DIR,
        help=f"Output directory (default: {DRY_RUN_OUTPUT_DIR})"
    )
    
    # Comparison command
    comp_parser = subparsers.add_parser('compare', help='Run similarity comparison analysis')
    comp_parser.add_argument(
        "--input-dir",
        type=str,
        default=DRY_RUN_OUTPUT_DIR,
        help=f"Directory containing generated code (default: {DRY_RUN_OUTPUT_DIR})"
    )
    comp_parser.add_argument(
        "--force-recompute",
        action="store_true",
        help="Force recomputation of existing analyses"
    )
    comp_parser.add_argument(
        "--export-viz",
        action="store_true",
        help="Export visualization data after analysis"
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
        default=1.0,
        help="Temperature for generation (default: 1.0)"
    )
    full_parser.add_argument(
        "--top-k",
        type=int,
        default=None,
        help="Top-k sampling parameter (optional)"
    )
    full_parser.add_argument(
        "--top-p", 
        type=float,
        default=None,
        help="Top-p (nucleus) sampling parameter (optional)"
    )
    full_parser.add_argument(
        "--test-groups",
        nargs="*",
        choices=["legacy", "quality", "structure"],
        default=["legacy"],
        help="Test groups to run (default: legacy). Options: legacy, quality, structure"
    )
    
    args = parser.parse_args()
    
    # Check sudo requirement for restricted commands
    if args.command in ['generate', 'full']:
        require_sudo()
    
    if args.command == 'generate':
        generate_code_only(args.challenge, args.prompt, args.iterations, args.temperature, args.output_dir, 
                     getattr(args, 'top_k', None), getattr(args, 'top_p', None))
    elif args.command == 'test':
        test_existing_code(args.input_dir, getattr(args, 'test_groups', ['legacy']))
    elif args.command == 'compare':
        run_similarity_analysis(args.input_dir, args.force_recompute, args.export_viz)
    elif args.command == 'full':
        dry_run_with_tests(args.challenge, args.prompt, args.iterations, args.temperature, 
                          getattr(args, 'test_groups', ['legacy']), getattr(args, 'top_k', None), 
                          getattr(args, 'top_p', None))
    else:
        parser.print_help()
        print("\n❌ Please specify a command: generate, test, compare, or full")
        sys.exit(1)


if __name__ == "__main__":
    main()