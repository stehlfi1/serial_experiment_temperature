
"""
A high-quality, maintainable implementation of a Todo List application.

This module provides a TaskManager class that adheres to the principles of
the ISO/IEC 25010 standard for software quality.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional

# For Python versions < 3.9, use typing.List and typing.Dict instead of list and dict
# This check ensures backward compatibility.
if sys.version_info < (3, 9):
    from typing import List as list
    from typing import Dict as dict


@dataclass
class Task:
    """
    Represents a single task in the todo list.

    This data class provides a structured, immutable-by-default way to handle
    task data, improving readability and reducing errors.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


class TaskManager:
    """
    Manages a collection of tasks with an in-memory storage system.

    This class provides a complete interface for adding, removing, searching,
    and updating tasks. It is designed for efficiency, safety, and testability.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an in-memory dictionary to store tasks for efficient
        lookups and a counter to generate unique task IDs.
        """
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, input_str: str, field_name: str) -> None:
        """
        Validates that a string input is not None and is not empty.

        Args:
            input_str: The string to validate.
            field_name: The name of the field being validated (for error messages).

        Raises:
            TypeError: If the input is not a string.
            ValueError: If the string is empty or consists only of whitespace.
        """
        if not isinstance(input_str, str):
            raise TypeError(f"{field_name} must be a string.")
        if not input_str or not input_str.strip():
            raise ValueError(f"{field_name} cannot be empty or just whitespace.")

    def _task_to_dict(self, task: Task) -> dict:
        """
        Converts a Task object to a dictionary.

        This helper ensures a consistent output format for all methods
        that return task details.

        Args:
            task: The Task object to convert.

        Returns:
            A dictionary representation of the task.
        """
        # asdict is a convenient utility from the dataclasses module
        return asdict(task)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be empty.
            task_description: A description for the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is empty or whitespace.
            TypeError: If inputs are not strings.
        """
        self._validate_string_input(task_name, "Task name")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string.")

        task_id = self._next_id
        new_task = Task(
            id=task_id,
            name=task_name.strip(),
            description=task_description.strip()
        )
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            return False
        
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> list[dict]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The term to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a
            matching task. Returns an empty list if no matches are found.

        Raises:
            ValueError: If search_term is empty or whitespace.
            TypeError: If search_term is not a string.
        """
        self._validate_string_input(search_term, "Search term")
        
        lower_search_term = search_term.lower()
        
        # Using a list comprehension for a concise and efficient implementation
        return [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if lower_search_term in task.name.lower() or \
               lower_search_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            return False

        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, representing all tasks currently stored.
            The list is sorted by task ID.
        """
        # Sorting by key (task.id) provides a consistent and predictable order.
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [self._task_to_dict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        This action is irreversible. It also resets the ID counter.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID sequence for a clean state
        return True


# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates how to use the TaskManager class.
    # It also serves as a basic integration test.
    
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n--- Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Clean the house", "Vacuum and dust all rooms")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Python Project", "Finish the todo list app")
        print(f"Added task with ID: {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    # 2. Get all tasks
    print("\n--- Current Tasks ---")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(task)

    # 3. Finish a task
    print("\n--- Finishing a Task ---")
    task_id_to_finish = 2
    if manager.finish(task_id_to_finish):
        print(f"Task {task_id_to_finish} marked as finished.")
    else:
        print(f"Failed to finish task {task_id_to_finish}. It may not exist.")

    # 4. Search for tasks
    print("\n--- Searching for 'python' ---")
    search_results = manager.search("python")
    if search_results:
        for task in search_results:
            print(f"Found: {task}")
    else:
        print("No tasks found matching the search term.")

    # 5. Remove a task
    print("\n--- Removing a Task ---")
    task_id_to_remove = 1
    if manager.remove(task_id_to_remove):
        print(f"Task {task_id_to_remove} removed successfully.")
    else:
        print(f"Failed to remove task {task_id_to_remove}. It may not exist.")

    # 6. Display tasks after modifications
    print("\n--- Tasks After Modifications ---")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(task)

    # 7. Test error handling
    print("\n--- Testing Error Cases ---")
    # Invalid add
    try:
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"Caught expected error: {e}")
    # Non-existent remove
    print(f"Attempting to remove non-existent task 99: Success = {manager.remove(99)}")
    # Non-existent finish
    print(f"Attempting to finish non-existent task 99: Success = {manager.finish(99)}")

    # 8. Clear all tasks
    print("\n--- Clearing All Tasks ---")
    manager.clear_all()
    print("All tasks cleared.")

    # 9. Final state
    print("\n--- Final Task List (should be empty) ---")
    print(manager.get_all())
