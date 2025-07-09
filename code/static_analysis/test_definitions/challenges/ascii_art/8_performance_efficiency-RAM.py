"""
Test of RAM usage
Output: RAM capacity allocated at the beginning and end of rendering each shape
"""

import statistics
import psutil
import os
import sys
import multiprocessing


from chatgpt import AsciiArt as ChatGPTAsciiArt
from claude import AsciiArt as ClaudeAsciiArt
from gemini import AsciiArt as GeminiAsciiArt


def get_memory_usage() -> float:
    """
    Get the current memory usage of the process in megabytes (MB).

    Returns:
        float: The memory usage of the current process in MB.
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # in MB


def measure_method_memory_usage(AsciiArt, method, iterations, shared_manager, *args) -> None:
    """
    Tests the memory usage of a specified method in the AsciiArt class over a number of iterations.

    Args:
        AsciiArt (class): The class containing the method to be tested.
        method (str): The name of the method to be tested.
        iterations (int): The number of times to call the method.
        *args: Additional arguments to pass to the method.

    Returns:
        None
    """
    try:
        instance = AsciiArt()

        mem_before = get_memory_usage()
        for _ in range(iterations):
            getattr(instance, method)(*args)
        mem_after = get_memory_usage()

        (shared_manager["mem_deltas"]).append(mem_after - mem_before)

    except Exception as e:
        (shared_manager["errors"]).append(e)


def run_method_memory_test(AsciiArt, method, iterations, *args) -> None:
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
                        args=(AsciiArt, method, iterations, shared_manager, *args),
                    )
                    process.start()
                    process.join()

                    if shared_manager["errors"]:
                        raise shared_manager["errors"][0]

                mem_median = statistics.median(shared_manager["mem_deltas"])
                print(f"Memory deltas for {method}: {mem_median:.2f} MB")
            except Exception as _:
                print(f"Method {method} failed with error.")

    except Exception as _:
        print("Failed to create shared manager.")


def benchmark_memory_usage(AsciiArt, iterations) -> None:
    """
    Runs memory usage tests for various drawing methods in the AsciiArt class.
    This function tests the memory usage of different drawing methods in the
    AsciiArt class by running each method in a separate process. The methods
    tested include drawing a square, rectangle, circle, triangle, and pyramid.

    Args:
        AsciiArt (class): The class containing the drawing methods to be tested.
        iterations (int): The number of iterations to run each test.

    Returns:
        None

    Raises:
        Exception: If any error occurs during the execution of the tests, it
                   will be caught and a message will be printed indicating
                   the failure of the module.
    """
    try:
        shapes = [
            ("draw_square", 100, "#"),
            ("draw_rectangle", 100, 50, "#"),
            ("draw_parallelogram", 100, 50, "#"),
            ("draw_triangle", 100, 50, "#"),
            ("draw_pyramid", 50, "#"),
        ]

        for method, *args in shapes:
            process = multiprocessing.Process(
                target=run_method_memory_test,
                args=(AsciiArt, method, iterations, *args),
            )
            process.start()
            process.join()
    except Exception as _:
        print(f"Module {AsciiArt.__module__} failed with error.")


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
        process = multiprocessing.Process(
            target=benchmark_memory_usage, args=(modules[sys.argv[1]], 100_000)
        )
        process.start()
        process.join()
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
