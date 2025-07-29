
"""
A high-quality, maintainable implementation of a Todo List application.

This module provides a TaskManager class that handles the core logic for managing
a collection of tasks in memory, adhering to the principles of the
ISO/IEC 25010 standard for software quality.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Union

# For Python versions < 3.9, use List and Dict from typing
if sys.version_info < (3, 9):
    from typing import List as list
    from typing import Dict as dict


@dataclass
class Task:
    """
    Represents a single task in the todo list.

    This dataclass provides a structured, readable, and type-safe way to
    store task information.

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

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Task object to a dictionary.

        This is useful for returning a structured, serializable representation
        of the task, which is a common practice in APIs.

        Returns:
            A dictionary representation of the task instance.
        """
        # Using asdict provides a clean conversion. We rename keys for clarity
        # in the output, as requested in the requirements.
        data = asdict(self)
        return {
            'id': data['id'],
            'task_name': data['name'],
            'task_description': data['description'],
            'is_finished': data['is_finished']
        }


class TaskManager:
    """
    Manages a collection of tasks with high performance and reliability.

    This class implements the core business logic for a todo list application.
    It uses a dictionary for efficient O(1) lookups, insertions, and deletions
    by task ID. It is designed to be completely independent of the user
    interface, making it highly modular and testable.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, *args: str) -> None:
        """
        Internal helper to validate that string inputs are not empty.

        Raises:
            ValueError: If any of the provided strings are empty or just whitespace.
        """
        for arg in args:
            if not isinstance(arg, str) or not arg.strip():
                raise ValueError("Task name and description cannot be empty.")

    def _get_task_or_raise(self, task_id: int) -> Task:
        """
        Internal helper to retrieve a task or raise a specific error.

        This promotes code reuse and consistent error handling for operations
        that require an existing task ID.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")
        return self._tasks[task_id]

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name or task_description are empty strings.
        """
        self._validate_string_input(task_name, task_description)

        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description.strip())
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        """
        try:
            self._get_task_or_raise(task_id)  # Validate existence
            del self._tasks[task_id]
            return True
        except (KeyError, TypeError):
            return False

    def search(self, search_term: str) -> list[dict]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.

        Raises:
            ValueError: If the search_term is an empty string.
        """
        self._validate_string_input(search_term)
        lower_term = search_term.lower()
        
        return [
            task.to_dict()
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.
        """
        try:
            task = self._get_task_or_raise(task_id)
            task.is_finished = True
            return True
        except (KeyError, TypeError):
            return False

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, representing all tasks currently in the manager.
            The list is sorted by task ID for consistent ordering.
        """
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [task.to_dict() for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Removes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean state
        return True


# --- Example Usage ---
def main():
    """
    A simple demonstration of the TaskManager's functionality.
    This function serves as a basic console-based UI and test harness.
    """
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n1. Adding tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"  - Added task with ID: {id1}")
        id2 = manager.add("Finish report", "Q3 financial report for management.")
        print(f"  - Added task with ID: {id2}")
        id3 = manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")
        print(f"  - Added task with ID: {id3}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # 2. Get all tasks
    print("\n2. Current tasks:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"  - {task}")

    # 3. Finish a task
    print(f"\n3. Marking task {id2} as finished...")
    success = manager.finish(id2)
    print(f"  - Operation successful: {success}")
    print(f"  - Finishing a non-existent task (ID 99): {manager.finish(99)}")

    # 4. Search for tasks
    print("\n4. Searching for tasks with the term 'report':")
    search_results = manager.search("report")
    for task in search_results:
        print(f"  - Found: {task}")

    # 5. Remove a task
    print(f"\n5. Removing task {id1}...")
    success = manager.remove(id1)
    print(f"  - Operation successful: {success}")
    print(f"  - Removing a non-existent task (ID 99): {manager.remove(99)}")

    # 6. Show tasks after modifications
    print("\n6. Current tasks after modifications:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"  - {task}")

    # 7. Demonstrate error handling
    print("\n7. Demonstrating error handling:")
    try:
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"  - Caught expected error: {e}")
    
    try:
        manager.search("   ")
    except ValueError as e:
        print(f"  - Caught expected error: {e}")

    # 8. Clear all tasks
    print("\n8. Clearing all tasks...")
    success = manager.clear_all()
    print(f"  - Operation successful: {success}")
    print(f"  - All tasks after clearing: {manager.get_all()}")


if __name__ == "__main__":
    main()
