
"""
A high-quality, maintainable implementation of a console-based Todo List application.

This module provides a TaskManager class that adheres to the principles of the
ISO/IEC 25010 standard for software quality.
"""

from __future__ import annotations
import sys
from typing import List, Dict, Any

# For Python versions < 3.9, List and Dict from typing are used.
# For Python >= 3.9, you can use the built-in list and dict for type hinting.
# This code uses the typing module for broad compatibility.


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class encapsulates all functionality for a todo list, including adding,
    removing, searching, and updating tasks. It is designed for correctness,
    efficiency, and testability.

    Attributes:
        _tasks (Dict[int, Dict[str, Any]]): A private dictionary to store tasks.
            The key is the task ID, and the value is a dictionary representing
            the task's properties. Using a dictionary provides O(1) average
            time complexity for lookups, insertions, and deletions by ID.
        _next_id (int): A private counter to ensure unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    def _validate_string_input(self, *args: str) -> None:
        """
        Validates that string inputs are non-empty and of type str.

        Raises:
            TypeError: If any argument is not a string.
            ValueError: If any string argument is empty or only contains whitespace.
        """
        for arg in args:
            if not isinstance(arg, str):
                raise TypeError(f"Input must be a string, but got {type(arg).__name__}.")
            if not arg.strip():
                raise ValueError("Input strings cannot be empty or contain only whitespace.")

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validates that a task ID is a valid integer and exists.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer or does not exist.
        """
        if not isinstance(task_id, int):
            raise TypeError(f"Task ID must be an integer, but got {type(task_id).__name__}.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the new task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name or task_description are empty strings.
        """
        self._validate_string_input(task_name, task_description)

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
        }
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
            ValueError: If task_id is invalid or does not exist.
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
            A list of task dictionaries that match the search term.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty string.
        """
        self._validate_string_input(search_term)
        normalized_term = search_term.lower().strip()
        
        return [
            task for task in self._tasks.values()
            if normalized_term in task["task_name"].lower()
            or normalized_term in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is invalid or does not exist.
        """
        self._validate_task_id(task_id)
        if self._tasks[task_id]["is_finished"]:
            # The task is already finished. Operation is idempotent.
            print(f"Info: Task {task_id} was already marked as finished.")
        
        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of all task dictionaries, sorted by ID.
        """
        return sorted(self._tasks.values(), key=lambda task: task["id"])

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful deletion of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


def print_tasks(tasks: List[Dict[str, Any]], title: str = "Tasks"):
    """Helper function to neatly print a list of tasks."""
    print(f"\n--- {title} ---")
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "✓ Finished" if task["is_finished"] else "✗ Pending"
        print(
            f"ID: {task['id']} | Status: {status}\n"
            f"  Name: {task['task_name']}\n"
            f"  Description: {task['task_description']}\n"
        )
    print("---------------------\n")


def main():
    """
    Main function to demonstrate the TaskManager functionality.
    This serves as a simple command-line interface and usage example.
    """
    print("Initializing Task Manager...")
    manager = TaskManager()

    # --- Add tasks ---
    print("Adding new tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese, and Eggs")
        id2 = manager.add("Complete project report", "Finalize the Q3 project report for review.")
        id3 = manager.add("Schedule dentist appointment", "Call the clinic for a check-up.")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}", file=sys.stderr)

    # --- Display all tasks ---
    all_tasks = manager.get_all()
    print_tasks(all_tasks, "All Tasks")

    # --- Finish a task ---
    print(f"Marking task {id2} as finished...")
    try:
        manager.finish(id2)
        print_tasks(manager.get_all(), "Tasks after finishing one")
    except (ValueError, TypeError) as e:
        print(f"Error finishing task: {e}", file=sys.stderr)

    # --- Search for tasks ---
    print("Searching for tasks containing 'report'...")
    search_results = manager.search("report")
    print_tasks(search_results, "Search Results for 'report'")
    
    print("Searching for tasks containing 'dentist'...")
    search_results_2 = manager.search("dentist")
    print_tasks(search_results_2, "Search Results for 'dentist'")

    # --- Remove a task ---
    print(f"Removing task {id1}...")
    try:
        manager.remove(id1)
        print_tasks(manager.get_all(), "Tasks after removing one")
    except (ValueError, TypeError) as e:
        print(f"Error removing task: {e}", file=sys.stderr)

    # --- Demonstrate Error Handling ---
    print("--- Demonstrating Error Handling ---")
    # 1. Add task with invalid input
    try:
        manager.add("  ", "This should fail")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # 2. Remove a non-existent task
    try:
        manager.remove(999)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # 3. Use a non-integer ID
    try:
        manager.finish("abc") # type: ignore
    except TypeError as e:
        print(f"Caught expected error: {e}")
        
    # --- Clear all tasks ---
    print("\nClearing all tasks...")
    manager.clear_all()
    print_tasks(manager.get_all(), "All Tasks after clearing")
    
    # Verify that a new task gets ID 1 again
    new_id = manager.add("New Task", "This is a fresh start.")
    print(f"Added a new task. Its ID is: {new_id}")
    print_tasks(manager.get_all(), "Final State")


if __name__ == "__main__":
    main()
