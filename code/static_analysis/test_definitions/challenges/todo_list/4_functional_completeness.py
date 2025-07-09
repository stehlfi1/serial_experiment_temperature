"""
Test of existence of all required functions (required interface)
Output: individual errors (absence of required functions, incorrect argument counts, incorrect argument types)
"""

import inspect
import sys
from typing import Optional


import chatgpt
import claude
import gemini


expected_classes = {
    "TaskManager": {
        "add": (2, {"task_name": str, "task_description": str}),
        "remove": (1, {"task_id": int}),
        "search": (1, {"task_term": str}),
        "finish": (1, {"task_id": int}),
        "get_all": (0, {}),
        "clear_all": (0, {}),
    }
}


def check_class_method(
    module, class_name, method_name, expected_args, expected_types
) -> Optional[str]:
    """
    Checks if a specified class method exists in a module and verifies its argument count and types.
    Args:
        module (module): The module to check.
        class_name (str): The name of the class to check.
        method_name (str): The name of the method to check.
        expected_args (int): The expected number of arguments for the method.
        expected_types (dict): A dictionary mapping argument names to their expected types.
    Returns:
        str: An error message if a check fails.
    """
    if not hasattr(module, class_name):
        return f"Class '{class_name}' is missing!"

    cls = getattr(module, class_name)
    if not hasattr(cls, method_name):
        return f"Method '{method_name}' in class '{class_name}' is missing!"

    method = getattr(cls, method_name)
    sig = inspect.signature(method)

    parameters = list(sig.parameters.values())
    if parameters and parameters[0].name == "self" or parameters[0].name == "cls":
        num_args = len(parameters) - 1
    else:
        num_args = len(sig.parameters)

    if num_args != expected_args:
        return f"Method '{method_name}' has {num_args} arguments, expected {expected_args}."

    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        expected_type = expected_types.get(param_name)
        actual_type = (
            param.annotation if param.annotation != inspect.Parameter.empty else None
        )
        if expected_type and actual_type and expected_type != actual_type:
            return f"Method '{method_name}' in class '{class_name}': parameter '{param_name}' should be {expected_type}, but is {actual_type}."
        if actual_type is None:
            return f"Method '{method_name}' in class '{class_name}': parameter '{param_name}' is missing a type annotation."


if __name__ == "__main__":
    modules = {"chatgpt": chatgpt, "claude": claude, "gemini": gemini}

    if sys.argv[1] not in modules:
        raise ValueError(f"Invalid module name: {sys.argv[1]}")

    print(f"Testing module: {modules[sys.argv[1]].__name__}")
    try:
        errors = []
        for class_name, methods in expected_classes.items():
            for method, (expected_args, expected_types) in methods.items():
                error = check_class_method(
                    modules[sys.argv[1]],
                    class_name,
                    method,
                    expected_args,
                    expected_types,
                )

                if error:
                    errors.append(error)
        if errors:
            print("\n".join(errors))
        else:
            print("All classes and methods exist and have the correct parameters.")
    except Exception as _:
        print(f"Module {modules[sys.argv[1]].__name__} failed with error.")
