
"""
A console-based To-Do list application adhering to ISO/IEC 25010 principles.

This module provides a TaskManager class for managing tasks and a simple
command-line interface for user interaction.

ISO/IEC 25010 Characteristics Addressed:
- Functional Suitability: Implements all required functionalities (add, remove, etc.).
- Performance Efficiency: Uses a dictionary for efficient O(1) lookups, insertions,
  and deletions by task ID.
- Maintainability:
    - Modularity: Business logic (TaskManager) is decoupled from the UI (main block).
    - Reusability: TaskManager can be used in other contexts (e.g., a web API).
    - Testability: The TaskManager class can be instantiated and tested in isolation.
    - Readability: Code is documented with docstrings, type hints, and clear
      variable names.
- Reliability:
    - Maturity: The logic is straightforward and robust.
    - Fault Tolerance (Safety): Graceful error handling with specific exceptions for
      invalid inputs or non-existent tasks.
- Usability: The console interface provides clear instructions and feedback.
- Portability: Uses only Python's standard library.
"""

import sys
from typing import Any, Dict, List

# Define a type alias for a Task dictionary for better readability and maintenance.
Task = Dict[str, Any]


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides the core logic for creating, retrieving, updating, and
    deleting tasks, ensuring data integrity and efficient operations.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an in-memory dictionary to store tasks and a counter for
        generating unique task IDs. The dictionary provides efficient O(1)
        average time complexity for ID-based operations.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID.

        Args:
            task_id: The ID of the task to validate.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            KeyError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is empty or contains only whitespace.
            TypeError: If task_name or task_description are not strings.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string.")

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
            TypeError, ValueError, KeyError: Propagated from _validate_task_id.
        """
        self._validate_task_id(task_id)
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

        Raises:
            ValueError: If search_term is empty or contains only whitespace.
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        term = search_term.lower().strip()
        return [
            task for task in self._tasks.values()
            if term in task["task_name"].lower() or
               term in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError, ValueError, KeyError: Propagated from _validate_task_id.
        """
        self._validate_task_id(task_id)
        if self._tasks[task_id]["is_finished"]:
            # Idempotency: If already finished, still report success.
            print(f"Info: Task {task_id} was already marked as finished.")
        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. Returns a copy to prevent
            modification of the internal state.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        This action is irreversible and also resets the task ID counter.

        Returns:
            True indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


def print_tasks(tasks: List[Task]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return

    for task in sorted(tasks, key=lambda t: t['id']):
        status = "Finished" if task["is_finished"] else "Pending"
        print(
            f"  ID: {task['id']} | Status: {status}\n"
            f"  Name: {task['task_name']}\n"
            f"  Description: {task['task_description']}\n"
            f"{'-'*40}"
        )


def main() -> None:
    """Main function to run the console-based UI for the To-Do list app."""
    manager = TaskManager()
    print("--- Console To-Do List Application ---")

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Mark Task as Finished")
        print("5. List All Tasks")
        print("6. Clear All Tasks")
        print("0. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Success: Task added with ID: {task_id}")

            elif choice == '2':
                task_id_str = input("Enter task ID to remove: ")
                manager.remove(int(task_id_str))
                print(f"Success: Task {task_id_str} removed.")

            elif choice == '3':
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\n--- Search Results for '{term}' ---")
                print_tasks(results)

            elif choice == '4':
                task_id_str = input("Enter task ID to mark as finished: ")
                manager.finish(int(task_id_str))
                print(f"Success: Task {task_id_str} marked as finished.")

            elif choice == '5':
                print("\n--- All Tasks ---")
                print_tasks(manager.get_all())

            elif choice == '6':
                confirm = input("Are you sure you want to delete all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    manager.clear_all()
                    print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == '0':
                print("Exiting application. Goodbye!")
                sys.exit(0)

            else:
                print("Error: Invalid choice. Please try again.")

        except (ValueError, TypeError, KeyError) as e:
            # Gracefully handle all expected errors from the TaskManager
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
