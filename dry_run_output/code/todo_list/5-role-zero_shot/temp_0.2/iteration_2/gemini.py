
"""
A high-quality, maintainable implementation of a Todo List Manager.

This module provides a TaskManager class that adheres to the principles of
ISO/IEC 25010, emphasizing reliability, performance, and maintainability.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# --- Data Model (Modularity, Readability) ---

@dataclass
class Task:
    """
    A dataclass representing a single task.

    This provides a structured, immutable-by-default way to handle task data,
    improving type safety and code clarity.
    """
    id: int
    task_name: str
    task_description: str
    is_finished: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the Task object to a dictionary.

        This is useful for serialization or consistent API responses.

        Returns:
            A dictionary representation of the task.
        """
        return asdict(self)

# --- Core Logic (Functional Suitability, Performance, Reliability) ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface to add, remove, search,
    and manage tasks, with a focus on efficiency and robust error handling.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an in-memory dictionary to store tasks and a counter
        for generating unique task IDs. The dictionary provides efficient
        O(1) average time complexity for lookups.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        A private helper to validate a task ID. (Modularity, Safety)

        Args:
            task_id: The ID of the task to validate.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description for the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is empty or contains only whitespace.
        """
        if not all(isinstance(arg, str) for arg in [task_name, task_description]):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        new_task = Task(
            id=task_id,
            task_name=task_name.strip(),
            task_description=task_description.strip()
        )
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If the task_id does not exist.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a
            matching task. Returns an empty list if no matches are found.

        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        term_lower = search_term.lower().strip()
        if not term_lower:
            return [] # Return empty for empty search term

        results = [
            task.to_dict() for task in self._tasks.values()
            if term_lower in task.task_name.lower() or
               term_lower in task.task_description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If the task_id does not exist.
        """
        self._validate_task_id(task_id)
        if self._tasks[task_id].is_finished:
            # Optional: Could return False or raise an error if already finished.
            # For idempotency, we'll allow it and return True.
            pass
        self._tasks[task_id].is_finished = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, with each dictionary representing a task.
            The list is sorted by task ID for consistent ordering.
        """
        # Sorting by ID provides a predictable order
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [task.to_dict() for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        This action is irreversible. It also resets the ID counter.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        print("All tasks have been cleared.")
        return True

# --- Example Usage (Testability, Usability) ---

if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It also serves as a basic integration test.
    
    def print_tasks(tasks: List[Dict[str, Any]]):
        """Helper function to pretty-print a list of tasks."""
        if not tasks:
            print("No tasks to show.")
            return
        for task in tasks:
            status = "✓" if task['is_finished'] else "✗"
            print(
                f"[{status}] ID: {task['id']} | "
                f"Name: {task['task_name']} | "
                f"Desc: {task['task_description']}"
            )
        print("-" * 20)

    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n--- Adding Tasks ---")
    id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
    id2 = manager.add("Code review", "Review the new feature branch")
    id3 = manager.add("Plan weekend trip", "Research destinations and book hotel")
    print(f"Added tasks with IDs: {id1}, {id2}, {id3}")

    print("\n--- All Tasks ---")
    all_tasks = manager.get_all()
    print_tasks(all_tasks)

    print("\n--- Finishing a Task (ID 2) ---")
    manager.finish(2)
    print_tasks(manager.get_all())

    print("\n--- Searching for 'review' ---")
    search_results = manager.search("review")
    print_tasks(search_results)
    
    print("\n--- Searching for 'trip' ---")
    search_results_2 = manager.search("trip")
    print_tasks(search_results_2)

    print("\n--- Removing a Task (ID 1) ---")
    manager.remove(1)
    print_tasks(manager.get_all())

    print("\n--- Handling Errors ---")
    try:
        manager.remove(99) # Non-existent ID
    except KeyError as e:
        print(f"Caught expected error: {e}")
    try:
        manager.add("", "This should fail") # Empty name
    except ValueError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Clearing All Tasks ---")
    manager.clear_all()
    print_tasks(manager.get_all())
