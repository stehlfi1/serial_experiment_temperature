"""
Test of RAM usage
Output: RAM capacity allocated at the beginning and end of calculation
"""

import statistics
import psutil
import os
import sys
import multiprocessing


from chatgpt import Calculator as ChatGPTCalculator
from claude import Calculator as ClaudeCalculator
from gemini import Calculator as GeminiCalculator


def get_process_memory():
    """
    Get the current memory usage of the process in megabytes (MB).

    Returns:
        float: The memory usage of the current process in MB.
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # in MB


def measure_method_memory_usage(
    Calculator, method, iterations, shared_manager, *args
) -> None:
    """
    Tests the memory usage of a specified method in a Calculator class over a number of iterations.

    Args:
        Calculator (type): The Calculator class to be tested.
        method (str): The name of the method to be tested.
        iterations (int): The number of times to call the method.
        *args: Arguments to pass to the method being tested.

    Returns:
        None
    """
    try:
        instance = Calculator()

        mem_before = get_process_memory()
        for _ in range(iterations):
            getattr(instance, method)(*args)
        mem_after = get_process_memory()

        (shared_manager["mem_deltas"]).append(mem_after - mem_before)
    except Exception as e:
        (shared_manager["errors"]).append(e)


def run_method_memory_test(Calculator, method, iterations, *args) -> None:
    """
    Calls the memory_usage_test function in a separate process to test the memory usage of a Calculator class.

    Args:
        Calculator (class): The Calculator class to be tested.
        method (str): The method name of the Calculator class to be tested.
        iterations (int): The number of iterations to run the memory usage test.
        *args: Additional arguments to be passed to the method being tested.

    Returns:
        None
    """
    try:
        with multiprocessing.Manager() as manager:
            shared_manager = manager.dict()
            shared_manager["mem_deltas"] = manager.list()
            shared_manager["errors"] = manager.list()

            try:
                for _ in range(100):
                    process = multiprocessing.Process(
                        target=measure_method_memory_usage,
                        args=(Calculator, method, iterations, shared_manager, *args),
                    )
                    process.start()
                    process.join()

                    if shared_manager["errors"]:
                        raise shared_manager["errors"][0]

                mem_median = statistics.median(shared_manager["mem_deltas"])
                print(f"Memory deltas for {method} ({args[0]}): {mem_median:.2f} MB")
            except Exception as _:
                print(f"Method {method} ({args[0]}) failed with error.")

    except Exception as _:
        print("Failed to create shared manager.")


def benchmark_memory_usage(Calculator, iterations) -> None:
    """
    Runs a memory usage test on a given Calculator class for a specified number of iterations.

    Args:
        Calculator (class): The Calculator class to be tested.
        iterations (int): The number of iterations to run the memory usage test.

    Returns:
        None
    """
    try:
        calculator = [
            ("calculate", "1974349+7972327"),
            ("calculate", "1974349-7972327"),
            ("calculate", "1974349*7972327"),
            ("calculate", "1974349/7972327"),
            ("calculate", "1974349+7972327-1974349*7972327/964"),
        ]

        for method, *args in calculator:
            process = multiprocessing.Process(
                target=run_method_memory_test,
                args=(Calculator, method, iterations, *args),
            )
            process.start()
            process.join()
    except Exception as _:
        print(f"Module {Calculator.__module__} failed with error.")


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
        process = multiprocessing.Process(
            target=benchmark_memory_usage, args=(modules[sys.argv[1]], 100_000)
        )
        process.start()
        process.join()
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
