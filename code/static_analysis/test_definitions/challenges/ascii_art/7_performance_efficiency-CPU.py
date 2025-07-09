"""
Test of CPU time taken by different operations
Output: processor time of running operations over ascii art
"""

import psutil
import sys


from chatgpt import AsciiArt as ChatGPTAsciiArt
from claude import AsciiArt as ClaudeAsciiArt
from gemini import AsciiArt as GeminiAsciiArt


def measure_cpu_time(instance, method, iterations, *args) -> None:
    """
    Measures the CPU time taken by a specified method of a given instance over a number of iterations.

    Args:
        instance (object): The instance of the class containing the method to be measured.
        method (str): The name of the method to be measured.
        iterations (int): The number of times the method should be called.
        *args: Additional arguments to be passed to the method.

    Returns:
        None
    """
    try:
        process = psutil.Process()

        cpu_times_before = process.cpu_times()

        for _ in range(iterations):
            getattr(instance, method)(*args)

        cpu_times_after = process.cpu_times()

        user_time = cpu_times_after.user - cpu_times_before.user
        system_time = cpu_times_after.system - cpu_times_before.system

        print(
            f"CPU time - {method}: User time = {user_time:.20f}s, System time = {system_time:.20f}s"
        )
    except Exception as _:
        print(f"Method {method} failed with error.")


def test_cpu_usage(instance, iterations) -> None:
    """
    Tests the CPU usage of various drawing operations.
    This function measures the CPU time taken to perform a number of iterations
    of different drawing operations (square, rectangle, circle, triangle, and pyramid)
    using the provided instance.

    Parameters:
        instance (object): The instance of the class containing the drawing methods.
        iterations (int): The number of iterations to perform for each drawing operation.

    Returns:
        None
    """
    width = 100
    height = 50
    symbol = "#"

    print(f"Testing CPU time with {iterations} iterations of each operation\n")

    measure_cpu_time(instance, "draw_square", iterations, width, symbol)
    measure_cpu_time(instance, "draw_rectangle", iterations, width, height, symbol)
    measure_cpu_time(instance, "draw_parallelogram", iterations, width, height, symbol)
    measure_cpu_time(instance, "draw_triangle", iterations, width, height, symbol)
    measure_cpu_time(instance, "draw_pyramid", iterations, height, symbol)


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
        test_cpu_usage(modules[sys.argv[1]](), 100_000)
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
