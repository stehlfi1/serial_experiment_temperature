
"""
A high-quality, maintainable, and efficient console-based Todo List application.

This module provides a TaskManager class that adheres to the principles of
ISO/IEC 25010, ensuring reliability, performance, and maintainability.
"""

import sys
from typing import Any, Dict, List, Union

# Define a type alias for a task dictionary for better readability and maintenance.
Task = Dict[str, Union[int, str, bool]]


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a clean, efficient, and robust interface for interacting
    with a todo list. It is designed for testability and reusability.

    Attributes:
        _tasks (dict[int, Task]): A dictionary to store tasks, mapping task ID to task data.
                                  Using a dictionary provides O(1) average time
                                  complexity for lookups, insertions, and deletions by ID.
        _next_id (int): A counter to generate unique, sequential task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
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
            raise KeyError(f"Task with ID {task_id} not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Cannot be empty.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If the task_name is empty or just whitespace.
            TypeError: If task_name or task_description are not strings.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or just whitespace.")

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
            ValueError: If task_id is not a positive integer.
            KeyError: If the task_id does not exist.
        """
        self._validate_task_id(task_id)  # Raises exceptions on failure
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
            Returns an empty list if no matches are found or the term is empty.

        Raises:
            TypeError: If the search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        if not search_term.strip():
            return []

        term_lower = search_term.lower()
        return [
            task
            for task in self._tasks.values()
            if term_lower in task["task_name"].lower()
            or term_lower in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            KeyError: If the task_id does not exist.
        """
        self._validate_task_id(task_id)  # Raises exceptions on failure
        if self._tasks[task_id]["is_finished"]:
            # Optional: Decide if re-finishing is an error or just idempotent.
            # Here, we allow it but inform the caller via a return value if needed.
            # For a boolean success status, this is still a success.
            pass
        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. The list is a copy,
            so modifications to it will not affect the internal state.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean state
        return True


# --- Console User Interface (for demonstration) ---

def print_tasks(tasks: List[Task]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("\nNo tasks found.")
        return

    print("\n--- Tasks ---")
    for task in sorted(tasks, key=lambda t: t['id']):
        status = "✓ Finished" if task["is_finished"] else "✗ Pending"
        print(
            f"ID: {task['id']} | Status: {status}\n"
            f"  Name: {task['task_name']}\n"
            f"  Desc: {task['task_description']}\n"
        )
    print("-------------")


def main() -> None:
    """Main function to run the console-based UI for the TaskManager."""
    manager = TaskManager()
    print("Welcome to the Console Todo List App!")

    # Pre-populate with some data for demonstration
    manager.add("Buy groceries", "Milk, Bread, Cheese")
    manager.add("Finish report", "Complete the Q3 performance report for management.")
    manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Mark Task as Finished")
        print("4. Search Tasks")
        print("5. List All Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"\n✅ Success: Task added with ID: {task_id}")
            elif choice == "2":
                task_id = int(input("Enter task ID to remove: "))
                manager.remove(task_id)
                print(f"\n✅ Success: Task {task_id} removed.")
            elif choice == "3":
                task_id = int(input("Enter task ID to finish: "))
                manager.finish(task_id)
                print(f"\n✅ Success: Task {task_id} marked as finished.")
            elif choice == "4":
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\nFound {len(results)} matching tasks.")
                print_tasks(results)
            elif choice == "5":
                all_tasks = manager.get_all()
                print_tasks(all_tasks)
            elif choice == "6":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    manager.clear_all()
                    print("\n✅ Success: All tasks have been cleared.")
                else:
                    print("\nOperation cancelled.")
            elif choice == "7":
                print("Exiting application. Goodbye!")
                sys.exit(0)
            else:
                print("\n❌ Error: Invalid choice. Please try again.")

        except (ValueError, TypeError, KeyError) as e:
            # Gracefully handle errors raised by the TaskManager
            print(f"\n❌ Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
