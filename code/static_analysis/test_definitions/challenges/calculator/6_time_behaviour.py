"""
Test of average operation execution time
Output: average run time of the individual shape rendering operations
"""

import time
import sys


from chatgpt import Calculator as ChatGPTCalculator
from claude import Calculator as ClaudeCalculator
from gemini import Calculator as GeminiCalculator


def time_operation(instance, method, iterations, expression) -> None:
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
            getattr(instance, method)(expression)
        end_time = time.time()

        print(
            f"Average time for {method} ({expression}): {((end_time - start_time) / iterations):.20f} seconds"
        )
    except Exception as _:
        print(f"Method {method} ({expression}) failed with error.")


def test_operations(instance, iterations) -> None:
    """
    Test the performance of various calculator operations.
    This function tests the performance of addition, subtraction, multiplication,
    division, and a complex expression by running each operation a specified number
    of times and measuring the time taken for each.

    Args:
        instance: An instance of the calculator class that has a 'calculate' method.
        iterations (int): The number of times each operation should be performed.

    Returns:
        None
    """
    print(f"Testing {iterations} iterations of each operation\n")

    time_operation(instance, "calculate", iterations, "1974349+7972327")
    time_operation(instance, "calculate", iterations, "1974349-7972327")
    time_operation(instance, "calculate", iterations, "1974349*7972327")
    time_operation(instance, "calculate", iterations, "1974349/7972327")
    time_operation(
        instance, "calculate", iterations, "1974349+7972327-1974349*7972327/964"
    )


if __name__ == "__main__":
    modules = {
        "chatgpt": ChatGPTCalculator,
        "claude": ClaudeCalculator,
        "gemini": GeminiCalculator,
    }

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")

    print(f"Testing module: {modules[sys.argv[1]].__module__}")
    try:
        test_operations(modules[sys.argv[1]](), 100_000)
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
