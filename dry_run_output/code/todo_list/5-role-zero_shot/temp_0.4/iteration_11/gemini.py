
"""
A high-quality, maintainable implementation of a console-based To-Do list manager.

This module provides the TaskManager class, which encapsulates all the logic for
managing tasks in memory. It is designed with the ISO/IEC 25010 standard in mind,
focusing on:
- Functional Suitability: All required operations are implemented correctly.
- Performance Efficiency: Uses a dictionary for O(1) average time complexity on
  lookups, insertions, and deletions.
- Reliability: Robust error handling and input validation.
- Maintainability: Code is modular, readable, and well-documented.
- Testability: Core logic is decoupled from the UI, making it easy to unit test.
"""

from __future__ import annotations
import sys

# Define a type alias for a task dictionary for better readability and maintenance.
Task = dict[str, int | str | bool]


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface to add, remove, search, and update
    tasks. It ensures data integrity through validation and is optimized for
    performance.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an in-memory data store for tasks and an ID counter.
        The internal `_tasks` dictionary uses the task ID as the key for
        efficient lookups.
        """
        self._tasks: dict[int, Task] = {}
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
            ValueError: If `task_name` is not a non-empty string.
            TypeError: If `task_name` or `task_description` are not strings.
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
            True if the task was found and removed, False otherwise.

        Raises:
            TypeError: If `task_id` is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> list[Task]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term.

        Raises:
            TypeError: If `search_term` is not a string.
            ValueError: If `search_term` is an empty string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower()
        return [
            task
            for task in self._tasks.values()
            if lower_term in task["name"].lower()
            or lower_term in task["description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError: If `task_id` is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        task = self._tasks.get(task_id)
        if task:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> list[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. The list is a copy,
            so modifications to it will not affect the internal task list.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        This operation is irreversible for the current session.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


def print_task(task: Task) -> None:
    """Helper function to format and print a single task."""
    status = "Finished" if task["is_finished"] else "Pending"
    print(
        f"  ID: {task['id']} | Status: {status}\n"
        f"  Name: {task['name']}\n"
        f"  Description: {task['description']}\n"
        f"  -----------------------------------"
    )


def print_tasks(tasks: list[Task]) -> None:
    """Helper function to format and print a list of tasks."""
    if not tasks:
        print("\nNo tasks found.")
        return
    print("\n--- Your Tasks ---")
    for task in tasks:
        print_task(task)


def main() -> None:
    """
    Main function to run the console-based UI for the To-Do list app.

    This function handles user input, calls the appropriate TaskManager methods,
    and displays results or error messages to the user. It serves as the
    presentation layer, completely separate from the TaskManager's business logic.
    """
    manager = TaskManager()
    print("Welcome to the Console To-Do List App!")

    # Pre-populate with some data for demonstration
    try:
        manager.add("Buy groceries", "Milk, Bread, Cheese, Eggs")
        manager.add("Finish report", "Complete the Q3 financial report for review.")
        manager.add("Call mom", "Check in and see how she's doing.")
    except (ValueError, TypeError) as e:
        print(f"Error during initial setup: {e}")


    while True:
        print("\nAvailable commands: add, remove, search, finish, list, clear, exit")
        command = input("Enter command: ").lower().strip()

        try:
            if command == "add":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Success! Task added with ID: {task_id}")

            elif command == "remove":
                task_id_str = input("Enter task ID to remove: ")
                task_id = int(task_id_str)
                if manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
                else:
                    print(f"Error: Task with ID {task_id} not found.")

            elif command == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\nFound {len(results)} task(s) matching '{term}':")
                print_tasks(results)

            elif command == "finish":
                task_id_str = input("Enter task ID to mark as finished: ")
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
                else:
                    print(f"Error: Task with ID {task_id} not found.")

            elif command == "list":
                all_tasks = manager.get_all()
                print_tasks(all_tasks)

            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif command == "exit":
                print("Goodbye!")
                sys.exit(0)

            else:
                print("Invalid command. Please try again.")

        except ValueError as e:
            print(f"Input Error: {e}")
        except TypeError as e:
            print(f"Type Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
