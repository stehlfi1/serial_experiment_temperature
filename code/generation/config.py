from .llm import Llm
from .challange import Challenge
from .prompt import Prompt
from .helpers import load_string_from_file

LLMS = [
    Llm("openai/gpt-4.1", "chatgpt", temperature=0.7),
    Llm("anthropic/claude-sonnet-4", "claude", temperature=0.7),
    Llm("google/gemini-2.5-pro", "gemini", temperature=0.7),
]

CHALLENGES = [
    Challenge(
        "calculator",
        [
            Prompt(
                "1-zero_shot",
                load_string_from_file("prompts/calculator/1-zero_shot.txt"),
            ),
            Prompt(
                "2-few_shot", load_string_from_file("prompts/calculator/2-few_shot.txt")
            ),
            Prompt(
                "3-chain_of_thoughts-zero_shot",
                load_string_from_file(
                    "prompts/calculator/3-chain_of_thoughts-zero_shot.txt"
                ),
            ),
            Prompt(
                "4-chain_of_thoughts-few_shot",
                load_string_from_file(
                    "prompts/calculator/4-chain_of_thoughts-few_shot.txt"
                ),
            ),
            Prompt(
                "5-role-zero_shot",
                load_string_from_file("prompts/calculator/5-role-zero_shot.txt"),
            ),
            Prompt(
                "6-role-few_shot",
                load_string_from_file("prompts/calculator/6-role-few_shot.txt"),
            ),
        ],
    ),
    Challenge(
        "ascii_art",
        [
            Prompt(
                "1-zero_shot",
                load_string_from_file("prompts/ascii_art/1-zero_shot.txt"),
            ),
            Prompt(
                "2-few_shot", load_string_from_file("prompts/ascii_art/2-few_shot.txt")
            ),
            Prompt(
                "3-chain_of_thoughts-zero_shot",
                load_string_from_file(
                    "prompts/ascii_art/3-chain_of_thoughts-zero_shot.txt"
                ),
            ),
            Prompt(
                "4-chain_of_thoughts-few_shot",
                load_string_from_file(
                    "prompts/ascii_art/4-chain_of_thoughts-few_shot.txt"
                ),
            ),
            Prompt(
                "5-role-zero_shot",
                load_string_from_file("prompts/ascii_art/5-role-zero_shot.txt"),
            ),
            Prompt(
                "6-role-few_shot",
                load_string_from_file("prompts/ascii_art/6-role-few_shot.txt"),
            ),
        ],
    ),
    Challenge(
        "todo_list",
        [
            Prompt(
                "1-zero_shot",
                load_string_from_file("prompts/todo_list/1-zero_shot.txt"),
            ),
            Prompt(
                "2-few_shot", load_string_from_file("prompts/todo_list/2-few_shot.txt")
            ),
            Prompt(
                "3-chain_of_thoughts-zero_shot",
                load_string_from_file(
                    "prompts/todo_list/3-chain_of_thoughts-zero_shot.txt"
                ),
            ),
            Prompt(
                "4-chain_of_thoughts-few_shot",
                load_string_from_file(
                    "prompts/todo_list/4-chain_of_thoughts-few_shot.txt"
                ),
            ),
            Prompt(
                "5-role-zero_shot",
                load_string_from_file("prompts/todo_list/5-role-zero_shot.txt"),
            ),
            Prompt(
                "6-role-few_shot",
                load_string_from_file("prompts/todo_list/6-role-few_shot.txt"),
            ),
        ],
    ),
]

DRY_RUN_CHALLENGE = "calculator"
DRY_RUN_PROMPT = "5-role-zero_shot"
DRY_RUN_ITERATIONS = 1
DRY_RUN_OUTPUT_DIR = "dry_run_output"
