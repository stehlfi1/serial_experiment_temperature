"""
Test of CPU time taken by different operations
Output: processor time of running operations over calculator
"""

import psutil
import sys


from chatgpt import Calculator as ChatGPTCalculator
from claude import Calculator as ClaudeCalculator
from gemini import Calculator as GeminiCalculator


def measure_cpu_time(instance, method, iterations, expression) -> None:
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
            getattr(instance, method)(expression)

        cpu_times_after = process.cpu_times()

        user_time = cpu_times_after.user - cpu_times_before.user
        system_time = cpu_times_after.system - cpu_times_before.system

        print(
            f"CPU time - {method} ({expression}): User time = {user_time:.20f}s, System time = {system_time:.20f}s"
        )
    except Exception as _:
        print(f"Method {method} ({expression}) failed with error.")


def test_cpu_usage(instance, iterations) -> None:
    """
    Test the CPU usage of various arithmetic operations.
    This function measures the CPU time taken to perform a specified number of iterations
    of different arithmetic operations using the `calculate` method of the given instance.

    Args:
        instance: The instance of the class containing the `calculate` method.
        iterations (int): The number of iterations to perform for each operation.

    Returns:
        None
    """
    print(f"Testing CPU time with {iterations} iterations of each operation\n")

    measure_cpu_time(instance, "calculate", iterations, "1974349+7972327")
    measure_cpu_time(instance, "calculate", iterations, "1974349-7972327")
    measure_cpu_time(instance, "calculate", iterations, "1974349*7972327")
    measure_cpu_time(instance, "calculate", iterations, "1974349/7972327")
    measure_cpu_time(
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
        test_cpu_usage(modules[sys.argv[1]](), 100_000)
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
