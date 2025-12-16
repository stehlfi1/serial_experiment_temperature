
"""
A high-quality, maintainable console-based to-do list application.

This module provides a TaskManager class that adheres to the principles of the
ISO/IEC 25010 standard, focusing on functional suitability, performance,
reliability, and maintainability.
"""

from __future__ import annotations
import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# ==============================================================================
# 1. Data Model (Modularity & Correctness)
# ==============================================================================

@dataclass
class Task:
    """
    Represents a single task in the to-do list.

    Using a dataclass provides type safety, immutability for the ID, and
    automatic generation of special methods like __init__ and __repr__.

    Attributes:
        id: A unique integer identifier for the task.
        name: The name or title of the task.
        description: A more detailed description of the task.
        is_finished: A boolean indicating if the task is completed.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


# ==============================================================================
# 2. Core Business Logic (Functional Suitability & Performance Efficiency)
# ==============================================================================

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides the core functionality for the to-do list application,
    including adding, removing, searching, and updating tasks. It is designed
    to be self-contained and easily testable.

    Data is stored in a dictionary for efficient O(1) average time complexity
    for ID-based lookups, insertions, and deletions.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate the existence of a task ID.

        Args:
            task_id: The ID of the task to validate.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID is found.
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
            task_description: The description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name is empty or contains only whitespace.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            # Enforce type safety for description as well
            raise TypeError("Task description must be a string.")

        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description)
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If the task ID does not exist.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.

        Raises:
            ValueError: If search_term is empty or not a string.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        term = search_term.lower()
        results = [
            asdict(task)
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully updated.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If the task ID does not exist.
        """
        self._validate_task_id(task_id)
        self._tasks[task_id].is_finished = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all tasks as dictionaries, sorted by ID.
        """
        return [asdict(task) for task in sorted(self._tasks.values(), key=lambda t: t.id)]

    def clear_all(self) -> bool:
        """

        Deletes all tasks from the list.

        Returns:
            True upon successful deletion of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# ==============================================================================
# 3. Presentation Layer (Usability & Reliability/Error Handling)
# ==============================================================================

def print_task(task: Dict[str, Any]) -> None:
    """Formats and prints a single task to the console."""
    status = "✓" if task['is_finished'] else "✗"
    print(f"[{status}] ID: {task['id']} - {task['name']}\n    Description: {task['description']}")

def print_help() -> None:
    """Prints the command menu."""
    print("\n--- To-Do List Menu ---")
    print("  add       - Add a new task")
    print("  list      - List all tasks")
    print("  search    - Search for a task")
    print("  finish    - Mark a task as finished")
    print("  remove    - Remove a task by ID")
    print("  clear     - Clear all tasks")
    print("  help      - Show this menu")
    print("  exit      - Exit the application")
    print("-------------------------")

def main() -> None:
    """
    Main function to run the console-based UI for the TaskManager.
    This function handles user input and calls the TaskManager methods,
    gracefully handling any exceptions that occur.
    """
    manager = TaskManager()
    print("Welcome to the To-Do List App!")
    print_help()

    while True:
        command = input("\nEnter a command: ").strip().lower()

        try:
            if command == "exit":
                print("Goodbye!")
                sys.exit(0)

            elif command == "help":
                print_help()

            elif command == "add":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"Success: Task added with ID {task_id}.")

            elif command == "list":
                tasks = manager.get_all()
                if not tasks:
                    print("No tasks found.")
                else:
                    print("\n--- All Tasks ---")
                    for task in tasks:
                        print_task(task)
                    print("-----------------")

            elif command == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                if not results:
                    print(f"No tasks found matching '{term}'.")
                else:
                    print(f"\n--- Search Results for '{term}' ---")
                    for task in results:
                        print_task(task)
                    print("---------------------------------")

            elif command == "finish":
                task_id_str = input("Enter the ID of the task to finish: ")
                manager.finish(int(task_id_str))
                print(f"Success: Task {task_id_str} marked as finished.")

            elif command == "remove":
                task_id_str = input("Enter the ID of the task to remove: ")
                manager.remove(int(task_id_str))
                print(f"Success: Task {task_id_str} removed.")

            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    manager.clear_all()
                    print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")
            
            else:
                print(f"Error: Unknown command '{command}'. Type 'help' for a list of commands.")

        except (ValueError, TypeError, KeyError) as e:
            # Gracefully handle validation and lookup errors from the manager
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
