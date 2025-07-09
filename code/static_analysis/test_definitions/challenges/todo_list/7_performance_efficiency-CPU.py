"""
Test of CPU time taken by different operations
Output: processor time of running operations over todo sheet
"""

import psutil
import sys


from chatgpt import TaskManager as ChatGPTTaskManager
from claude import TaskManager as ClaudeTaskManager
from gemini import TaskManager as GeminiTaskManager


def measure_cpu_time(instance, method, iterations, flag, *args) -> None:
    """
    Measures the CPU time taken by a specified method of a given instance over a number of iterations.

    Args:
        instance (object): The instance of the class containing the method to be measured.
        method (str): The name of the method to be measured.
        iterations (int): The number of times the method should be called.
        *args: Additional arguments to be passed to the method.

    Prints:
        str: The user and system CPU time taken by the method over the specified number of iterations.
    """
    try:
        process = psutil.Process()

        cpu_times_before = process.cpu_times()

        for i in range(iterations):
            if flag:
                formated_args = [arg.format(i=i + 1) for arg in args]
                if method in ("finish", "remove"):
                    formated_args = [int(arg) for arg in formated_args]
                getattr(instance, method)(*formated_args)
            else:
                getattr(instance, method)()

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
    Test the CPU usage of various operations on a given instance.
    This function measures the CPU time taken to perform a series of operations
    on the provided instance.

    Args:
        instance: The instance on which the operations will be performed.
        iterations (int): The number of times each operation will be performed.

    Returns:
        None
    """
    print(f"Testing CPU time with {iterations} iterations of each operation\n")

    measure_cpu_time(
        instance, "add", iterations, True, "task_name_{i}", "task_description_{i}"
    )
    measure_cpu_time(instance, "get_all", iterations, False)
    measure_cpu_time(instance, "search", iterations, True, "task_name_{i}")
    measure_cpu_time(instance, "search", iterations, True, "task_description_{i}")
    measure_cpu_time(instance, "finish", iterations, True, "{i}")
    measure_cpu_time(instance, "remove", iterations, True, "{i}")


if __name__ == "__main__":
    modules = {
        "chatgpt": ChatGPTTaskManager,
        "claude": ClaudeTaskManager,
        "gemini": GeminiTaskManager,
    }

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")

    print(f"Testing module: {modules[sys.argv[1]].__module__}")
    try:
        test_cpu_usage(modules[sys.argv[1]](), 10_000)
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
