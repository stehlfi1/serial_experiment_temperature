
# -*- coding: utf-8 -*-
"""
A console-based todo list application demonstrating best practices.

This module implements a TaskManager class that provides a clean API for
managing a list of tasks in memory, adhering to the principles of a
high-quality, maintainable application as outlined by ISO/IEC 25010.
"""

from __future__ import annotations

import dataclasses
from typing import Dict, List, TypedDict

# Using a TypedDict to define the structure of the data returned to the client.
# This improves readability and allows static analysis tools to catch potential bugs.
class TaskDict(TypedDict):
    """A dictionary representation of a Task."""
    id: int
    name: str
    description: str
    is_finished: bool

# Using a dataclass for the internal representation of a task.
# This is more robust and readable than using dictionaries internally.
# It provides type hints, default values, and a clear structure.
@dataclasses.dataclass
class _Task:
    """Internal data structure representing a single task."""
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> TaskDict:
        """
        Converts the _Task object to its dictionary representation.

        This method facilitates the conversion of the internal data model to the
        public-facing data format, ensuring a consistent interface.

        Returns:
            TaskDict: A dictionary containing the task's attributes.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_finished": self.is_finished,
        }


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class encapsulates all the logic for creating, retrieving, updating,
    and deleting tasks (CRUD operations). It is designed to be easily testable
    and reusable in different contexts (e.g., console app, web API).

    Attributes:
        _tasks (Dict[int, _Task]): A dictionary to store tasks, mapping
                                   task ID to the Task object for efficient
                                   O(1) average time complexity lookups.
        _next_id (int): A counter to generate unique IDs for new tasks.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, _Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If `task_name` is an empty or whitespace-only string.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or just whitespace.")

        task = _Task(
            id=self._next_id, name=task_name.strip(), description=task_description.strip()
        )
        self._tasks[task.id] = task
        self._next_id += 1
        return task.id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            KeyError: If no task with the given ID is found.
            ValueError: If the provided task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[TaskDict]:
        """
        Searches for tasks by a term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.
            Returns an empty list if no matches are found or the term is empty.
        """
        if not search_term or not search_term.strip():
            return []

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
            True if the task was successfully marked as finished.

        Raises:
            KeyError: If no task with the given ID is found.
            ValueError: If the provided task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")

        self._tasks[task_id].is_finished = True
        return True

    def get_all(self) -> List[TaskDict]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, where each task is a dictionary.
            The list is sorted by task ID.
        """
        # Sorting by ID provides a consistent and predictable order.
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [task.to_dict() for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        This operation is irreversible.

        Returns:
            True, indicating all tasks have been cleared.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


def _print_tasks(tasks: List[TaskDict]) -> None:
    """Helper function to print a list of tasks in a formatted way."""
    if not tasks:
        print("No tasks to display.")
        return

    # Find max width for alignment, providing a better user experience
    max_name_len = max(len(t["name"]) for t in tasks) if tasks else 10
    header = (
        f"{'ID':<4} | {'Status':<10} | {'Name':<{max_name_len}} | {'Description'}"
    )
    print(header)
    print("-" * len(header))

    for task in tasks:
        status = "Finished" if task["is_finished"] else "Pending"
        print(
            f"{task['id']:<4} | {status:<10} | "
            f"{task['name']:<{max_name_len}} | {task['description']}"
        )


def main() -> None:
    """
    Main function to run the console-based todo list application.

    This function handles the user interface, including menu display,
    input gathering, and calling the appropriate `TaskManager` methods.
    It gracefully handles errors raised by the `TaskManager` and provides
    user-friendly feedback.
    """
    manager = TaskManager()
    print("--- Console Todo List App ---")

    # Pre-populate with some data for demonstration
    manager.add("Buy groceries", "Milk, Bread, Cheese")
    manager.add("Finish report", "Complete the Q3 performance report for the team.")
    manager.add("Call mom", "")

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. List All Tasks")
        print("3. Mark Task as Finished")
        print("4. Remove Task")
        print("5. Search Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Success: Task added with ID {task_id}.")
            elif choice == "2":
                print("\n--- All Tasks ---")
                _print_tasks(manager.get_all())
            elif choice == "3":
                task_id_str = input("Enter task ID to mark as finished: ")
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"Success: Task {task_id} marked as finished.")
            elif choice == "4":
                task_id_str = input("Enter task ID to remove: ")
                task_id = int(task_id_str)
                if manager.remove(taskid):
                    print(f"Success: Task {task_id} removed.")
            elif choice == "5":
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\n--- Search Results for '{term}' ---")
                _print_tasks(results)
            elif choice == "6":
                confirm = input("Are you sure you want to delete all tasks? (y/N): ")
                if confirm.lower() == "y":
                    manager.clear_all()
                    print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")
            elif choice == "7":
                print("Exiting application. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

        except (ValueError, KeyError) as e:
            # Gracefully handle validation and logic errors from the manager
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
