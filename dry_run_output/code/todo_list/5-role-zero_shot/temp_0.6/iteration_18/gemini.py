
"""
A module for managing a collection of tasks in-memory.

This module provides the TaskManager class, which implements a full
Create, Read, Update, Delete (CRUD) interface for a todo list. It is designed
with a focus on code quality, adhering to principles from ISO/IEC 25010.
"""

import sys
from typing import Any, Dict, List

# Define a type alias for a Task dictionary for better readability and maintenance.
Task = Dict[str, Any]


class TaskManager:
    """
    Manages a collection of tasks with an in-memory storage dictionary.

    This class provides methods to add, remove, search, and modify tasks.
    It is designed for efficiency, with most ID-based operations having an
    average time complexity of O(1).
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an empty dictionary to store tasks and initializes the
        task ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the collection.

        Args:
            task_name: The name or title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique integer ID assigned to the new task.

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
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The unique ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term. Returns an
            empty list if the search term is empty or no matches are found.

        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        
        if not search_term.strip():
            return []

        lower_term = search_term.lower()
        
        return [
            task for task in self._tasks.values()
            if lower_term in task["task_name"].lower()
            or lower_term in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The unique ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """

        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. The list is a copy, so
            modifications to it will not affect the internal task storage.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        This action is irreversible and also resets the task ID counter.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


def print_tasks(tasks: List[Task]):
    """Helper function to format and print a list of tasks."""
    if not tasks:
        print("No tasks to display.")
        return

    print("-" * 80)
    print(f"{'ID':<5} {'Status':<12} {'Name':<25} {'Description'}")
    print("-" * 80)
    for task in tasks:
        status = "Finished" if task["is_finished"] else "Pending"
        print(
            f"{task['id']:<5} {status:<12} {task['task_name']:<25} {task['task_description']}"
        )
    print("-" * 80)


def main_cli():
    """Main function to run the command-line interface for the TaskManager."""
    manager = TaskManager()
    print("Welcome to the Console Todo List App!")

    # Pre-populate with some data for demonstration
    manager.add("Buy groceries", "Milk, Bread, Cheese")
    manager.add("Finish report", "Complete the Q3 sales report for management.")
    manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")

    while True:
        print("\nAvailable commands: add, remove, search, finish, list, clear, exit")
        command = input("Enter command: ").strip().lower()

        try:
            if command == "add":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Success: Task added with ID {task_id}.")

            elif command == "remove":
                task_id_str = input("Enter task ID to remove: ")
                manager.remove(int(task_id_str))
                print(f"Success: Task {task_id_str} removed.")

            elif command == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\nFound {len(results)} matching tasks:")
                print_tasks(results)

            elif command == "finish":
                task_id_str = input("Enter task ID to mark as finished: ")
                manager.finish(int(task_id_str))
                print(f"Success: Task {task_id_str} marked as finished.")

            elif command == "list":
                print("\nAll Tasks:")
                print_tasks(manager.get_all())

            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ").lower()
                if confirm == 'yes':
                    manager.clear_all()
                    print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif command == "exit":
                print("Exiting application. Goodbye!")
                sys.exit(0)

            else:
                print("Error: Invalid command. Please try again.")

        except (ValueError, TypeError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main_cli()
