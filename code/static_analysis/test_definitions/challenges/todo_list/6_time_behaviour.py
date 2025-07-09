"""
Test of average operation execution time
Output: average run time of the individual shape rendering operations
"""

import time
import sys


from chatgpt import TaskManager as ChatGPTTaskManager
from claude import TaskManager as ClaudeTaskManager
from gemini import TaskManager as GeminiTaskManager


def time_operation(instance, method, iterations, flag, *args) -> None:
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
        for i in range(iterations):
            if flag:
                formated_args = [arg.format(i=i + 1) for arg in args]
                if method in ("finish", "remove"):
                    formated_args = [int(arg) for arg in formated_args]
                getattr(instance, method)(*formated_args)
            else:
                getattr(instance, method)()
        end_time = time.time()

        print(
            f"Average time for {method}: {((end_time - start_time) / iterations):.20f} seconds"
        )
    except Exception as _:
        print(f"Method {method} failed with error.")


def test_operations(instance, iterations) -> None:
    """
    Tests various operations on a given instance for a specified number of iterations.

    Args:
        instance: The instance on which the operations will be performed.
        iterations (int): The number of times each operation will be performed.

    Returns:
        None
    """
    print(f"Testing {iterations} iterations of each operation\n")

    time_operation(
        instance, "add", iterations, True, "task_name_{i}", "task_description_{i}"
    )
    time_operation(instance, "get_all", iterations, False)
    time_operation(instance, "search", iterations, True, "task_name_{i}")
    time_operation(instance, "search", iterations, True, "task_description_{i}")
    time_operation(instance, "finish", iterations, True, "{i}")
    time_operation(instance, "remove", iterations, True, "{i}")


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
        test_operations(modules[sys.argv[1]](), 10_000)
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
