
# -*- coding: utf-8 -*-
"""
A high-quality, console-based Todo List application.

This module contains the core logic for a Task Manager and a simple
console-based user interface for interacting with it. The design emphasizes
modularity, testability, and adherence to software quality standards.
"""

from __future__ import annotations
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Any

# --- Core Logic (Model) ---

@dataclass
class Task:
    """
    A dataclass representing a single task.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task. Defaults to False.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

class TaskManager:
    """
    Manages a collection of tasks with business logic and data validation.

    This class provides a clean interface for interacting with the todo list,
    handling all operations like adding, removing, and searching for tasks.
    It is designed to be completely independent of the user interface.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an in-memory data store."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, value: str, field_name: str) -> None:
        """
        Validates that a string input is not empty or just whitespace.

        Args:
            value (str): The string value to validate.
            field_name (str): The name of the field for use in error messages.

        Raises:
            TypeError: If the input is not a string.
            ValueError: If the input string is empty or only contains whitespace.
        """
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name (str): The name of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name or task_description are empty strings.
            TypeError: If task_name or task_description are not strings.
        """
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")

        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description.strip())
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.
        """
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was successfully marked as finished, False otherwise.
        """
        if task := self._tasks.get(task_id):
            task.is_finished = True
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.
        The search is case-insensitive.

        Args:
            search_term (str): The term to search for.

        Returns:
            list[dict]: A list of tasks that match the search term. Each task
                        is represented as a dictionary.

        Raises:
            ValueError: If the search_term is empty.
            TypeError: If the search_term is not a string.
        """
        self._validate_string_input(search_term, "Search term")
        lower_search_term = search_term.lower()

        results = [
            asdict(task)
            for task in self._tasks.values()
            if lower_search_term in task.name.lower() or \
               lower_search_term in task.description.lower()
        ]
        return results

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: A list of all tasks. Each task is represented as a dictionary.
                        Returns an empty list if there are no tasks.
        """
        return [asdict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list and resets the ID counter.

        Returns:
            bool: Always returns True to indicate success.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Presentation Layer (View/Controller) ---

def print_menu() -> None:
    """Prints the main menu of available actions to the console."""
    print("\n--- Todo List Menu ---")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Finished")
    print("4. List All Tasks")
    print("5. Search Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")
    print("----------------------")

def print_task(task: Dict[str, Any]) -> None:
    """Formats and prints a single task's details."""
    status = "✓ Finished" if task['is_finished'] else "✗ Pending"
    print(
        f"  ID: {task['id']} | Status: {status}\n"
        f"  Name: {task['name']}\n"
        f"  Description: {task['description']}\n"
        f"  -----------------"
    )

def main() -> None:
    """Main function to run the console-based UI for the TaskManager."""
    manager = TaskManager()
    print("Welcome to the Todo List App!")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"✅ Success: Task '{name}' added with ID {task_id}.")

            elif choice == '2':
                task_id_str = input("Enter task ID to remove: ")
                if not task_id_str.isdigit():
                    print("❌ Error: ID must be a positive number.")
                    continue
                if manager.remove(int(task_id_str)):
                    print(f"✅ Success: Task {task_id_str} removed.")
                else:
                    print(f"❌ Error: Task with ID {task_id_str} not found.")

            elif choice == '3':
                task_id_str = input("Enter task ID to mark as finished: ")
                if not task_id_str.isdigit():
                    print("❌ Error: ID must be a positive number.")
                    continue
                if manager.finish(int(task_id_str)):
                    print(f"✅ Success: Task {task_id_str} marked as finished.")
                else:
                    print(f"❌ Error: Task with ID {task_id_str} not found.")

            elif choice == '4':
                tasks = manager.get_all()
                if not tasks:
                    print("ℹ️  Your todo list is empty.")
                else:
                    print("\n--- All Tasks ---")
                    for task in tasks:
                        print_task(task)

            elif choice == '5':
                term = input("Enter search term: ")
                results = manager.search(term)
                if not results:
                    print(f"ℹ️  No tasks found matching '{term}'.")
                else:
                    print(f"\n--- Search Results for '{term}' ---")
                    for task in results:
                        print_task(task)

            elif choice == '6':
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ").lower()
                if confirm == 'yes':
                    manager.clear_all()
                    print("✅ Success: All tasks have been cleared.")
                else:
                    print("ℹ️  Operation cancelled.")

            elif choice == '7':
                print("Goodbye!")
                sys.exit(0)

            else:
                print("❌ Error: Invalid choice. Please enter a number between 1 and 7.")

        except (ValueError, TypeError) as e:
            print(f"❌ Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
