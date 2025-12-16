
"""
A module for managing a list of tasks in memory.

This module provides the TaskManager class, which offers a clean, object-oriented
interface for creating, retrieving, updating, and deleting tasks. It is designed
with ISO/IEC 25010 quality characteristics in mind, focusing on:

- Functional Suitability: Correctly implements all required todo list operations.
- Performance Efficiency: Uses efficient data structures (dictionaries) for
  fast lookups, insertions, and deletions (O(1) average time complexity).
- Reliability & Safety: Includes robust validation and error handling to
  prevent crashes from invalid input.
- Maintainability & Testability: The core logic is encapsulated within the
  TaskManager class, decoupled from the user interface, making it easy to
  test, modify, and reuse.
- Readability: Adheres to PEP 8 and includes comprehensive documentation and
  type hints.
"""

import sys
from typing import List, Dict, Any, TypedDict

# Define a precise type for a task dictionary for improved static analysis and readability.
class Task(TypedDict):
    """Represents the structure of a single task."""
    id: int
    task_name: str
    task_description: str
    is_finished: bool

# --- Custom Exceptions for Clear Error Handling ---
class TaskError(Exception):
    """Base exception for errors related to task operations."""
    pass

class TaskNotFoundError(TaskError):
    """Raised when a task with a given ID is not found."""
    pass

class InvalidTaskDataError(ValueError, TaskError):
    """Raised when provided task data (e.g., name) is invalid."""
    pass


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class encapsulates all the logic for handling tasks, including
    creation, deletion, searching, and status updates. It uses a dictionary
    for efficient data storage and retrieval.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        Sets up an in-memory dictionary to store tasks and a counter for
        generating unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """
        Generates a new unique ID for a task.

        Returns:
            int: A unique integer ID.
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name/title of the task. Cannot be empty.
            task_description: A detailed description of the task.

        Returns:
            int: The unique ID of the newly created task.

        Raises:
            InvalidTaskDataError: If the task_name is empty or just whitespace.
        """
        if not task_name or not task_name.strip():
            raise InvalidTaskDataError("Task name cannot be empty.")

        task_id = self._generate_id()
        new_task: Task = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
        }
        self._tasks[task_id] = new_task
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed.

        Raises:
            TaskNotFoundError: If no task with the given ID is found.
            InvalidTaskDataError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskDataError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term.
            Returns an empty list if no matches are found.

        Raises:
            InvalidTaskDataError: If the search_term is empty or just whitespace.
        """
        if not search_term or not search_term.strip():
            raise InvalidTaskDataError("Search term cannot be empty.")

        lower_term = search_term.lower()
        return [
            task
            for task in self._tasks.values()
            if lower_term in task["task_name"].lower()
            or lower_term in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully updated.

        Raises:
            TaskNotFoundError: If no task with the given ID is found.
            InvalidTaskDataError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskDataError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all task dictionaries, sorted by ID.
        """
        return sorted(self._tasks.values(), key=lambda task: task["id"])

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            bool: True upon successful deletion of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Console User Interface (UI) ---
# This section is decoupled from the TaskManager logic for better maintainability.

def print_task(task: Task) -> None:
    """Formats and prints a single task to the console."""
    status = "✅ Finished" if task["is_finished"] else "◻️ Pending"
    print(
        f"  ID: {task['id']} | Status: {status}\n"
        f"  Name: {task['task_name']}\n"
        f"  Description: {task['task_description']}\n"
        f"  ----------------------------------------"
    )

def print_menu() -> None:
    """Prints the main menu of options."""
    print("\n===== Todo List Menu =====")
    print("1. Add a new task")
    print("2. Remove a task")
    print("3. Mark a task as finished")
    print("4. List all tasks")
    print("5. Search for a task")
    print("6. Clear all tasks")
    print("7. Exit")
    print("==========================")

def main() -> None:
    """The main entry point and run loop for the console application."""
    manager = TaskManager()
    print("Welcome to the Console Todo List App!")

    # Pre-populate with some data for demonstration
    manager.add("Buy groceries", "Milk, Bread, Cheese, and Eggs")
    manager.add("Finish report", "Complete the Q3 financial report for management.")
    manager.add("Call mom", "Check in and see how she's doing.")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")

        try:
            if choice == "1":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"\n✅ Success: Task '{name}' added with ID {task_id}.")

            elif choice == "2":
                task_id_str = input("Enter task ID to remove: ")
                manager.remove(int(task_id_str))
                print(f"\n✅ Success: Task {task_id_str} removed.")

            elif choice == "3":
                task_id_str = input("Enter task ID to mark as finished: ")
                manager.finish(int(task_id_str))
                print(f"\n✅ Success: Task {task_id_str} marked as finished.")

            elif choice == "4":
                all_tasks = manager.get_all()
                print("\n--- All Tasks ---")
                if not all_tasks:
                    print("No tasks found.")
                else:
                    for task in all_tasks:
                        print_task(task)

            elif choice == "5":
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\n--- Search Results for '{term}' ---")
                if not results:
                    print("No matching tasks found.")
                else:
                    for task in results:
                        print_task(task)

            elif choice == "6":
                confirm = input("Are you sure you want to delete ALL tasks? (y/N): ")
                if confirm.lower() == 'y':
                    manager.clear_all()
                    print("\n✅ Success: All tasks have been cleared.")
                else:
                    print("\nOperation cancelled.")

            elif choice == "7":
                print("Exiting application. Goodbye!")
                sys.exit(0)

            else:
                print("\n❌ Error: Invalid choice. Please enter a number between 1 and 7.")

        except (TaskNotFoundError, InvalidTaskDataError) as e:
            print(f"\n❌ Error: {e}")
        except ValueError:
            print("\n❌ Error: Invalid ID. Please enter a valid number.")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
