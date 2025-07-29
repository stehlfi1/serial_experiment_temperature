
# -*- coding: utf-8 -*-
"""
A high-quality, maintainable implementation of a console-based Todo list application.

This module provides a TaskManager class that adheres to the principles of
ISO/IEC 25010, focusing on reliability, efficiency, and maintainability.
"""

import dataclasses
from typing import Dict, List, Any

# --- Data Model (Modularity) ---

@dataclasses.dataclass
class Task:
    """
    Represents a single task in the todo list.

    Using a dataclass provides type safety, automatic __init__ and __repr__,
    and clearly defines the data structure for a task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


# --- Core Logic (Functional Suitability, Performance, Reliability) ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface to add, remove, search,
    and modify tasks, ensuring data integrity and efficient operations.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        An internal dictionary `_tasks` is used for storage, providing O(1)
        average time complexity for lookups, insertions, and deletions by ID.
        An ID counter `_next_id` ensures unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Private helper to validate a task ID. (Reliability & Reusability)

        Args:
            task_id: The ID to validate.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID '{task_id}' not found.")

    @staticmethod
    def _task_to_dict(task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to its dictionary representation. (Maintainability)

        This ensures a consistent output format for all public methods.
        """
        return dataclasses.asdict(task)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description for the task.

        Returns:
            The unique ID assigned to the new task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

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
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        """
        try:
            self._validate_task_id(task_id)
            del self._tasks[task_id]
            return True
        except (ValueError, TypeError):
            return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a case-insensitive search term in name or description.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower()
        return [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.
        """
        try:
            self._validate_task_id(task_id)
            self._tasks[task_id].is_finished = True
            return True
        except (ValueError, TypeError):
            return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, where each task is a dictionary.
            Returns an empty list if no tasks exist.
        """
        return [self._task_to_dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean state
        return True


# --- Example Usage (Testability & Usability) ---

if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It also serves as a basic integration test.

    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n1. Adding tasks...")
    try:
        id1 = manager.add("Implement Core Logic", "Write the main TaskManager class.")
        print(f"  - Added task with ID: {id1}")
        id2 = manager.add("Write Unit Tests", "Use pytest to test all methods.")
        print(f"  - Added task with ID: {id2}")
        id3 = manager.add("Refactor Database Module", "Replace list with a more efficient data structure.")
        print(f"  - Added task with ID: {id3}")
        # Example of invalid input
        manager.add("", "This should fail.")
    except ValueError as e:
        print(f"  - Caught expected error: {e}")

    print("\n2. Getting all tasks:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"  - {task}")

    print("\n3. Finishing a task...")
    success = manager.finish(id2)
    print(f"  - Marking task {id2} as finished: {'Success' if success else 'Failed'}")
    
    print("\n4. Searching for tasks with the term 'logic':")
    search_results = manager.search("logic")
    for task in search_results:
        print(f"  - Found: {task}")
        
    print("\n5. Removing a task...")
    success = manager.remove(id3)
    print(f"  - Removing task {id3}: {'Success' if success else 'Failed'}")
    
    print("\n6. Attempting to remove a non-existent task (ID 99):")
    success = manager.remove(99)
    print(f"  - Removing task 99: {'Success' if success else 'Failed'}")

    print("\n7. Getting all tasks after modifications:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"  - {task}")

    print("\n8. Clearing all tasks...")
    manager.clear_all()
    print("  - All tasks cleared.")

    print("\n9. Getting all tasks after clearing:")
    all_tasks = manager.get_all()
    print(f"  - Current tasks: {all_tasks}")

