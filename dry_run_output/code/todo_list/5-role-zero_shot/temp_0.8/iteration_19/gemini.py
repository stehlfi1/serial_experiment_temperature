
"""
A console-based Todo List application adhering to high-quality code standards.

This module provides a TaskManager class for handling todo list logic and a simple
command-line interface (CLI) for user interaction.

ISO/IEC 25010 Compliance Notes:
- Functional Suitability: Implements all specified functionalities correctly.
- Performance Efficiency: Uses a dictionary for efficient O(1) task lookups.
- Modularity: Separates business logic (TaskManager) from presentation (CLI).
- Reliability: Gracefully handles errors and invalid inputs.
- Testability: The TaskManager class is self-contained and easily testable.
- Readability: Adheres to PEP 8, with clear docstrings and type hints.
"""

from __future__ import annotations
import sys
from typing import List, Dict, Any, Union

# Define a type alias for a task dictionary for better readability and maintenance.
TaskDict = Dict[str, Union[int, str, bool]]


class TaskManager:
    """
    Manages all operations related to tasks in a todo list.

    This class encapsulates the business logic for a todo list application,
    handling the storage and manipulation of tasks. It is designed to be
    decoupled from any specific user interface, making it reusable and testable.

    Attributes:
        _tasks (Dict[int, Dict[str, Any]]): An in-memory dictionary to store
            tasks, with the task ID as the key.
        _next_id (int): A counter to generate unique IDs for new tasks.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is empty or not a string.
            TypeError: If inputs are not of type string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or just whitespace.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        Args:
            task_id: The unique ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            ValueError: If the task_id does not exist or is invalid.
            TypeError: If task_id is not an integer.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[TaskDict]:
        """
        Searches for tasks containing a specific term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
            
        term_lower = search_term.lower()
        results = []
        for task_id, task_data in self._tasks.items():
            if (term_lower in task_data["task_name"].lower() or
                    term_lower in task_data["task_description"].lower()):
                results.append(self._format_task(task_id, task_data))
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The unique ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            ValueError: If the task_id does not exist or is invalid.
            TypeError: If task_id is not an integer.
        """
        self._validate_task_id(task_id)
        self._tasks[task_id]["is_finished"] = True
        return True
        
    def get_all(self) -> List[TaskDict]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
        """
        return [self._format_task(task_id, task_data)
                for task_id, task_data in self._tasks.items()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        This operation is irreversible. It also resets the task ID counter.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer or does not exist.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

    def _format_task(self, task_id: int, task_data: Dict[str, Any]) -> TaskDict:
        """
        Internal helper to format a task into the required output dictionary structure.
        """
        return {"id": task_id, **task_data}


def print_menu() -> None:
    """Prints the main menu options to the console."""
    print("\n--- Todo List Menu ---")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Finished")
    print("4. List All Tasks")
    print("5. Search Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")
    print("----------------------")


def display_tasks(tasks: List[TaskDict]) -> None:
    """Formats and prints a list of tasks to the console."""
    if not tasks:
        print("No tasks found.")
        return
        
    for task in sorted(tasks, key=lambda t: t['id']):
        status = "Finished" if task["is_finished"] else "Pending"
        print(
            f"ID: {task['id']} | Status: {status}\n"
            f"  Name: {task['task_name']}\n"
            f"  Description: {task['task_description']}\n"
        )


def main() -> None:
    """
    Main function to run the console-based todo list application.
    
    This function handles all user interaction, such as displaying menus,
    accepting input, and calling the appropriate TaskManager methods.
    """
    task_manager = TaskManager()
    print("Welcome to the Todo List App!")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")

        try:
            if choice == "1":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = task_manager.add(name, desc)
                print(f"✅ Success: Task added with ID: {task_id}")

            elif choice == "2":
                task_id_str = input("Enter task ID to remove: ")
                task_manager.remove(int(task_id_str))
                print(f"✅ Success: Task {task_id_str} removed.")

            elif choice == "3":
                task_id_str = input("Enter task ID to mark as finished: ")
                task_manager.finish(int(task_id_str))
                print(f"✅ Success: Task {task_id_str} marked as finished.")

            elif choice == "4":
                print("\n--- All Tasks ---")
                all_tasks = task_manager.get_all()
                display_tasks(all_tasks)

            elif choice == "5":
                term = input("Enter search term: ")
                print(f"\n--- Search Results for '{term}' ---")
                found_tasks = task_manager.search(term)
                display_tasks(found_tasks)

            elif choice == "6":
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ")
                if confirm.lower() == 'yes':
                    task_manager.clear_all()
                    print("✅ Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == "7":
                print("Exiting application. Goodbye!")
                sys.exit(0)

            else:
                print("❌ Error: Invalid choice. Please enter a number between 1 and 7.")

        except (ValueError, TypeError) as e:
            # Gracefully handle validation and type errors from the TaskManager
            print(f"❌ Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
