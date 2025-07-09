"""
Test of average operation execution time
Output: average run time of the individual shape rendering operations
"""

import time
import sys


from chatgpt import AsciiArt as ChatGPTAsciiArt
from claude import AsciiArt as ClaudeAsciiArt
from gemini import AsciiArt as GeminiAsciiArt


def time_operation(instance, method, iterations, *args) -> None:
    """
    Times the execution of a specified method on a given instance over a number of iterations.

    Args:
        instance (object): The object instance on which the method will be called.
        method (str): The name of the method to be timed.
        iterations (int): The number of times the method will be called.
        *args: Additional arguments to be passed to the method.

    Returns:
        None
    """
    try:
        start_time = time.time()
        for _ in range(iterations):
            getattr(instance, method)(*args)
        end_time = time.time()

        print(
            f"Average time for {method}: {((end_time - start_time) / iterations):.20f} seconds"
        )
    except Exception as _:
        print(f"Method {method} failed with error.")


def test_operations(instance, iterations):
    """
    Tests various drawing operations on the given instance for a specified number of iterations.

    Args:
        instance (object): The instance on which the drawing operations will be performed.
        iterations (int): The number of times each drawing operation will be executed.

    Returns:
        None
    """
    width = 100
    height = 50
    symbol = "#"

    print(f"Testing {iterations} iterations of each operation\n")

    time_operation(instance, "draw_square", iterations, width, symbol)
    time_operation(instance, "draw_rectangle", iterations, width, height, symbol)
    time_operation(instance, "draw_parallelogram", iterations, width, height, symbol)
    time_operation(instance, "draw_triangle", iterations, width, height, symbol)
    time_operation(instance, "draw_pyramid", iterations, height, symbol)


if __name__ == "__main__":
    modules = {
        "chatgpt": ChatGPTAsciiArt,
        "claude": ClaudeAsciiArt,
        "gemini": GeminiAsciiArt,
    }

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")

    print(f"Testing module: {modules[sys.argv[1]].__module__}")
    try:
        test_operations(modules[sys.argv[1]](), 100_000)
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
