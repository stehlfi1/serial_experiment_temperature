"""
Test of RAM usage
Output: RAM capacity allocated at the beginning and end of todo list operations
"""

import statistics
import psutil
import os
import sys
import multiprocessing


from chatgpt import TaskManager as ChatGPTTaskManager
from claude import TaskManager as ClaudeTaskManager
from gemini import TaskManager as GeminiTaskManager


def get_process_memory() -> float:
    """
    Get the current memory usage of the process in megabytes (MB).

    Returns:
        float: The memory usage of the current process in MB.
    """
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)  # in MB


def measure_method_memory_usage(
    todolist_manager, method, iterations, flag, method_manager, *args
) -> None:
    """
    Tests the memory usage of a specified method in the todolist_manager class.

    Args:
        todolist_manager (object): The instance of the todo list manager class.
        method (str): The name of the method to be tested (e.g., 'finish', 'remove').
        iterations (int): The number of times to call the method.
        flag (bool): A flag indicating whether to format the arguments.
        method_manager (dict): A dictionary to share state between tests.
        *args: Additional arguments to be passed to the method.

    Returns:
        None
    """
    try:
        mem_before = get_process_memory()
        for i in range(iterations):
            formated_args = [arg.format(i=i + 1) for arg in args] if flag else []
            if method in ("finish", "remove"):
                formated_args = [int(arg) for arg in formated_args]

            getattr(todolist_manager, method)(*formated_args)
        mem_after = get_process_memory()

        (method_manager["mem_deltas"]).append(mem_after - mem_before)

        if method == "add":
            method_manager["base_state"] = todolist_manager

    except Exception as e:
        (method_manager["errors"]).append(e)


def run_method_memory_test(
    TodoListManager, todolist_instance, method, iterations, flag, shared_manager, *args
) -> None:
    """
    Calls the memory_usage_test function in a separate process to test the memory usage of a TodoListManager class.

    Args:
        TodoListManager (class): The TodoListManager class to be tested.
        todolist_instance (object): The instance of the TodoListManager class.
        method (str): The name of the method to be tested.
        iterations (int): The number of times to call the method.
        flag (bool): A flag indicating whether to format the arguments.
        shared_manager (dict): A dictionary to share state between tests.
        *args: Additional arguments to be passed to the method being tested.

    Returns:
        None
    """
    try:
        with multiprocessing.Manager() as manager:
            method_manager = manager.dict()
            method_manager["mem_deltas"] = manager.list()
            method_manager["errors"] = manager.list()

            try:
                for _ in range(20):
                    if not todolist_instance:
                        todolist_instance = TodoListManager()

                    process = multiprocessing.Process(
                        target=measure_method_memory_usage,
                        args=(
                            todolist_instance,
                            method,
                            iterations,
                            flag,
                            method_manager,
                            *args,
                        ),
                    )
                    process.start()
                    process.join()

                    if method_manager["errors"]:
                        raise method_manager["errors"][0]
                    
                    if method == "add":
                        shared_manager["base_state"] = method_manager.get("base_state", None)

                mem_median = statistics.median(method_manager["mem_deltas"])
                print(f"Memory deltas for {method}: {mem_median:.2f} MB")
            except Exception as e:
                print(f"Method {method} failed with error.")
                shared_manager["errors"].append(e)

    except Exception as _:
        print("Failed to create shared manager.")


def benchmark_memory_usage(TodoListManager, iterations) -> None:
    """
    Runs a memory usage test on the given TodoListManager class.
    This function tests the memory efficiency of various methods in the TodoListManager class
    by running them in separate processes and measuring their memory usage.

    Args:
        TodoListManager (class): The class to be tested for memory usage.
        iterations (int): The number of iterations to run each test.

    Returns:
        None
    """
    try:
        with multiprocessing.Manager() as manager:
            shared_manager = manager.dict()
            shared_manager["errors"] = manager.list()

            add_process = multiprocessing.Process(
                target=run_method_memory_test,
                args=(
                    TodoListManager,
                    None,
                    "add",
                    iterations,
                    True,
                    shared_manager,
                    "task_name_{i}",
                    "task_description_{i}",
                ),
            )
            add_process.start()
            add_process.join()

            if not shared_manager["errors"]:
                todolist_instance = shared_manager["base_state"]

                tests = [
                    ("get_all", False),
                    ("search", True, "task_name_{i}"),
                    ("search", True, "task_description_{i}"),
                    ("finish", True, "{i}"),
                    ("remove", True, "{i}"),
                ]

                for method, flag, *args in tests:
                    process = multiprocessing.Process(
                        target=run_method_memory_test,
                        args=(
                            TodoListManager,
                            todolist_instance,
                            method,
                            iterations,
                            flag,
                            None,
                            *args,
                        ),
                    )
                    process.start()
                    process.join()
    except Exception as _:
        print(f"Module {TodoListManager.__module__} failed with error.")


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
        process = multiprocessing.Process(
            target=benchmark_memory_usage, args=(modules[sys.argv[1]], 10_000)
        )
        process.start()
        process.join()
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__module__} failed with error.")
