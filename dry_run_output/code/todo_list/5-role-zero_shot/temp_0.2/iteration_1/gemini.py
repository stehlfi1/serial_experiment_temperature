
"""
A high-quality, maintainable implementation of a Todo List application.

This module provides a TaskManager class that adheres to the principles of the
ISO/IEC 25010 standard for software quality, focusing on efficiency,
reliability, and maintainability.
"""

from __future__ import annotations
from typing import TypedDict, List, Dict

# By using a TypedDict, we enforce a consistent structure for our task objects,
# improving readability and enabling static analysis tools to catch potential bugs.
# This contributes to Maintainability and Reliability.
class Task(TypedDict):
    """Represents the structure of a single task."""
    id: int
    task_name: str
    task_description: str
    is_finished: bool


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface to add, remove, search, and manage
    tasks, ensuring data integrity and efficient operations.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an in-memory dictionary to store tasks and an ID counter.
        The dictionary provides O(1) average time complexity for lookups,
        insertions, and deletions, ensuring Performance Efficiency.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name or title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is empty or just whitespace.
            TypeError: If task_name or task_description are not strings.
        """
        # --- Input Validation (Reliability & Security) ---
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        # --- Core Logic ---
        task_id = self._next_id
        new_task: Task = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description,
            "is_finished": False,
        }
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
        
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks by a search term in the name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.
            Returns an empty list if no matches are found.

        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        term_lower = search_term.lower()
        results = [
            task.copy() for task in self._tasks.values()
            if term_lower in task["task_name"].lower()
            or term_lower in task["task_description"].lower()
        ]
        # Returning copies ensures encapsulation (Security/Integrity).
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.
            
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks. Each task is a dictionary.
            The list is a copy to prevent direct modification of internal state.
        """
        # Returning copies ensures encapsulation (Security/Integrity).
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean slate.
        return True


if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class and serves
    # as a basic integration test, contributing to Testability and Analysability.
    
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # --- Add Tasks ---
    print("\n--- Adding Tasks ---")
    id1 = manager.add("Learn Python", "Study advanced concepts like OOP and decorators.")
    id2 = manager.add("Write Project Documentation", "Document the TaskManager class.")
    id3 = manager.add("Go Grocery Shopping", "Buy milk, bread, and python snacks.")
    print(f"Added task with ID: {id1}")
    print(f"Added task with ID: {id2}")
    print(f"Added task with ID: {id3}")

    # --- Get All Tasks ---
    print("\n--- Current Tasks ---")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(task)

    # --- Finish a Task ---
    print("\n--- Finishing a Task ---")
    success = manager.finish(id2)
    print(f"Marked task {id2} as finished: {success}")
    print("Task status after finishing:")
    print(manager.search("Documentation")[0])

    # --- Search for Tasks ---
    print("\n--- Searching for 'python' ---")
    python_tasks = manager.search("python")
    for task in python_tasks:
        print(task)

    # --- Remove a Task ---
    print("\n--- Removing a Task ---")
    success = manager.remove(id3)
    print(f"Removed task {id3}: {success}")
    
    # --- Get All Tasks Again ---
    print("\n--- Current Tasks After Removal ---")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(task)

    # --- Demonstrate Error Handling ---
    print("\n--- Testing Error Handling ---")
    try:
        manager.add("", "This should fail.")
    except ValueError as e:
        print(f"Caught expected error: {e}")
        
    try:
        manager.remove("not-an-id")
    except TypeError as e:
        print(f"Caught expected error: {e}")

    # --- Clear All Tasks ---
    print("\n--- Clearing All Tasks ---")
    success = manager.clear_all()
    print(f"All tasks cleared: {success}")
    print("Final task list:", manager.get_all())
