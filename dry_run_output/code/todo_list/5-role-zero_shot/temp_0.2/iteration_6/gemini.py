
"""
A high-quality, maintainable implementation of a Todo List application backend.

This module provides a TaskManager class that handles all the logic for managing
a collection of tasks in memory, adhering to the principles of the
ISO/IEC 25010 standard for software product quality.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# For Python versions < 3.9, use List, Dict from typing
if sys.version_info < (3, 9):
    from typing import List, Dict

@dataclass
class Task:
    """
    A dataclass representing a single task.

    This provides a structured, immutable-by-default way to handle task data,
    improving readability and type safety over using raw dictionaries internally.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface for adding, removing, searching,
    and updating tasks. It is designed for correctness, efficiency, and
    maintainability.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up the in-memory data storage using a dictionary for efficient
        lookups (O(1) average time complexity) and a counter for unique ID
        generation.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, input_value: str, field_name: str) -> str:
        """A private helper to validate string inputs."""
        if not isinstance(input_value, str) or not input_value.strip():
            raise ValueError(f"{field_name} cannot be empty or just whitespace.")
        return input_value.strip()

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to the specified dictionary format for the API.

        This decouples the internal data representation (Task dataclass) from the
        external API contract, improving modularity.
        """
        return {
            "id": task.id,
            "task_name": task.name,
            "task_description": task.description,
            "is_finished": task.is_finished,
        }

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be empty.
            task_description: The description of the task. Cannot be empty.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name or task_description are empty or invalid.
        """
        validated_name = self._validate_string_input(task_name, "Task name")
        validated_desc = self._validate_string_input(task_description, "Task description")

        new_id = self._next_id
        new_task = Task(id=new_id, name=validated_name, description=validated_desc)
        self._tasks[new_id] = new_task
        self._next_id += 1

        return new_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise (e.g.,
            if the task ID does not exist).
        """
        if isinstance(task_id, int) and task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.
            Returns an empty list if the search term is empty or no tasks match.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            return []

        normalized_term = search_term.strip().lower()
        
        # Using a list comprehension for a concise and readable implementation.
        return [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if normalized_term in task.name.lower()
            or normalized_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False
            otherwise (e.g., if the task ID does not exist).
        """
        if isinstance(task_id, int) and task_id in self._tasks:
            self._tasks[task_id].is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, where each task is a dictionary.
            The list is sorted by task ID for consistent ordering.
        """
        # Sorting by key (task.id) ensures a predictable output order.
        sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.id)
        return [self._task_to_dict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        This operation is irreversible for the current session.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean state
        return True


# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates how the TaskManager class can be used.
    # It also serves as a basic, informal test suite.
    
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n--- Adding Tasks ---")
    try:
        task1_id = manager.add("Learn Python", "Study advanced concepts like OOP and decorators.")
        print(f"Added task with ID: {task1_id}")
        task2_id = manager.add("Write Documentation", "Document the TaskManager class.")
        print(f"Added task with ID: {task2_id}")
        task3_id = manager.add("Test Application", "Write unit tests for all public methods.")
        print(f"Added task with ID: {task3_id}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    print("\n--- Demonstrating Input Validation ---")
    try:
        manager.add("", "This should fail.")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Getting All Tasks ---")
    all_tasks = manager.get_all()
    print(all_tasks)

    print(f"\n--- Finishing Task {task1_id} ---")
    success = manager.finish(task1_id)
    print(f"Operation successful: {success}")
    print(manager.get_all())

    print("\n--- Searching for 'python' ---")
    search_results = manager.search("python")
    print(search_results)

    print("\n--- Searching for 'doc' ---")
    search_results_doc = manager.search("doc")
    print(search_results_doc)

    print(f"\n--- Removing Task {task2_id} ---")
    success = manager.remove(task2_id)
    print(f"Operation successful: {success}")
    print(manager.get_all())

    print("\n--- Attempting to Remove Non-existent Task (ID 999) ---")
    success = manager.remove(999)
    print(f"Operation successful: {success}")

    print("\n--- Clearing All Tasks ---")
    success = manager.clear_all()
    print(f"Operation successful: {success}")

    print("\n--- Getting All Tasks After Clearing ---")
    print(manager.get_all())
