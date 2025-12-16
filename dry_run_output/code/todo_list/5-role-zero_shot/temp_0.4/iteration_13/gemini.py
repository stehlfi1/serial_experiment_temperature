
"""
A high-quality, console-based Todo List application.

This module provides a TaskManager class for managing tasks and a simple
command-line interface (CLI) for user interaction. The design adheres to
ISO/IEC 25010 principles, focusing on correctness, efficiency, safety,
and maintainability.

Key Design Choices:
- OOP: Core logic is encapsulated within the TaskManager class.
- Data Structure: A dictionary is used for the main task store, mapping
  task IDs to task objects. This provides efficient O(1) average time
  complexity for additions, deletions, and lookups by ID.
- Error Handling: Methods raise specific, built-in exceptions for invalid
  input, which are gracefully handled by the UI layer.
- Modularity: The TaskManager logic is completely decoupled from the UI,
  making it independently testable and reusable.
- Documentation: All public methods are documented with docstrings, and
  type hints are used for clarity and static analysis.
"""

import sys
from typing import List, Dict, Any, Union

# A type alias for a task dictionary for better readability.
Task = Dict[str, Union[int, str, bool]]


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides the core business logic for a todo list application,
    including adding, removing, searching, and updating tasks.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an in-memory dictionary to store tasks and a counter
        to generate unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
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
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

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
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty or whitespace-only string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower()
        results = [
            task.copy() for task in self._tasks.values()
            if lower_term in task["name"].lower() or lower_term in task["description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task's status was changed to 'finished',
            False if the task was already finished.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        task = self._tasks[task_id]
        if task["is_finished"]:
            return False  # No change was made

        task["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all task dictionaries. Returns copies to prevent
            unintended modification of internal state.
        """
        # Return a list of copies to ensure data encapsulation
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            True upon successful deletion of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


# --- User Interface (UI) Layer ---

def _print_tasks(tasks: List[Task]) -> None:
    """Helper function to print a list of tasks in a formatted way."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- Tasks ---")
    for task in sorted(tasks, key=lambda t: t['id']):
        status = "✓ Finished" if task["is_finished"] else "✗ Pending"
        print(
            f"ID: {task['id']} | Status: {status}\n"
            f"  Name: {task['name']}\n"
            f"  Description: {task['description']}\n"
            f"-------------"
        )

def _get_task_id_from_user() -> int:
    """Prompts user for a task ID and handles validation."""
    while True:
        try:
            task_id_str = input("Enter task ID: ")
            return int(task_id_str)
        except ValueError:
            print("Invalid input. Please enter a valid integer for the task ID.")

def main() -> None:
    """Main function to run the console-based UI for the Todo List App."""
    task_manager = TaskManager()
    print("Welcome to the Console Todo List App!")

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Mark Task as Finished")
        print("5. List All Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = task_manager.add(name, description)
                print(f"Success! Task added with ID: {task_id}")

            elif choice == '2':
                if not task_manager.get_all():
                    print("No tasks to remove.")
                    continue
                task_id = _get_task_id_from_user()
                if task_manager.remove(task_id):
                    print(f"Success! Task with ID {task_id} removed.")

            elif choice == '3':
                term = input("Enter search term: ")
                results = task_manager.search(term)
                _print_tasks(results)

            elif choice == '4':
                if not task_manager.get_all():
                    print("No tasks to finish.")
                    continue
                task_id = _get_task_id_from_user()
                if task_manager.finish(task_id):
                    print(f"Success! Task with ID {task_id} marked as finished.")
                else:
                    print(f"Info: Task with ID {task_id} was already finished.")

            elif choice == '5':
                all_tasks = task_manager.get_all()
                _print_tasks(all_tasks)

            elif choice == '6':
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    task_manager.clear_all()
                    print("Success! All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == '7':
                print("Exiting application. Goodbye!")
                sys.exit(0)

            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

        except (ValueError, TypeError, KeyError) as e:
            # Gracefully handle all expected errors from the TaskManager
            print(f"\nError: {e}")
        except Exception as e:
            # Catch any unexpected errors
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
