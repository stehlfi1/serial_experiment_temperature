
# -*- coding: utf-8 -*-
"""
A high-quality, professional implementation of a console-based todo list
application that adheres to the principles of the ISO/IEC 25010 standard.

This module provides a TaskManager class for managing todo list items in memory.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# --- Data Model (Modularity & Readability) ---
# Using a dataclass provides type safety, immutability for certain fields,
# and a clear structure for our core data entity.
@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

# --- Core Logic (Functional Suitability & Reliability) ---
class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a clean interface for adding, removing, searching,
    and updating tasks, ensuring data integrity and efficient operations.
    It is designed for reliability and maintainability.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        Internal data structures:
        _tasks (Dict[int, Task]): Stores tasks, keyed by task ID for O(1) lookups.
        _next_id (int): A counter to generate unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, *args: str) -> None:
        """
        Private helper to validate that string inputs are not empty.

        Raises:
            ValueError: If any of the provided strings are empty or whitespace.
        """
        for arg in args:
            if not isinstance(arg, str) or not arg.strip():
                raise ValueError("Input strings cannot be empty or just whitespace.")

    def _get_task_or_raise(self, task_id: int) -> Task:
        """
        Private helper to retrieve a task by ID or raise an error.

        This centralizes the logic for task existence checks, promoting DRY
        (Don't Repeat Yourself) and consistent error handling.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        task = self._tasks.get(task_id)
        if task is None:
            raise ValueError(f"Error: Task with ID '{task_id}' not found.")
        return task

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name or task_description are empty.
        """
        self._validate_string_input(task_name, task_description)

        task_id = self._next_id
        new_task = Task(
            id=task_id,
            name=task_name.strip(),
            description=task_description.strip()
        )
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
            This method is fault-tolerant and will not raise an exception for
            a non-existent ID, making it user-friendly for direct API calls.
        """
        try:
            self._get_task_or_raise(task_id)
            del self._tasks[task_id]
            return True
        except (ValueError, TypeError):
            return False

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.
        """
        try:
            task = self._get_task_or_raise(task_id)
            task.is_finished = True
            return True
        except (ValueError, TypeError):
            return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for in task names and descriptions.

        Returns:
            A list of dictionaries, where each dictionary represents a
            matching task. Returns an empty list if no matches are found.

        Raises:
            ValueError: If the search_term is empty.
        """
        self._validate_string_input(search_term)
        lower_term = search_term.lower()
        
        # Performance: This is an O(n) operation, which is optimal for this
        # requirement as every task must be checked.
        results = [
            asdict(task) for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]
        return results

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries representing all tasks.
        """
        return [asdict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean state
        return True


# --- User Interface (Example Usage & Usability) ---
# This section demonstrates how to use the TaskManager class.
# It is kept separate from the core logic for better modularity.
def print_task(task: Dict[str, Any]) -> None:
    """Helper function to format and print a single task."""
    status = "DONE" if task['is_finished'] else "PENDING"
    print(
        f"  ID: {task['id']} [{status}]\n"
        f"  Name: {task['name']}\n"
        f"  Description: {task['description']}\n"
        f"----------------------------------------"
    )

def main() -> None:
    """A simple command-line interface to demonstrate TaskManager functionality."""
    manager = TaskManager()
    print("--- Console Todo List App ---")

    # Pre-populate with some data for demonstration
    manager.add("Finish report", "Complete the Q3 financial report for management.")
    manager.add("Buy groceries", "Milk, bread, eggs, and cheese.")
    manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")

    while True:
        print("\nAvailable commands: [add, list, search, finish, remove, clear, exit]")
        command = input("> ").lower().strip()

        if command == "exit":
            print("Exiting application. Goodbye!")
            sys.exit(0)
        
        elif command == "add":
            try:
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Success: Task added with ID {task_id}.")
            except ValueError as e:
                print(f"Error: {e}")

        elif command == "list":
            tasks = manager.get_all()
            if not tasks:
                print("No tasks found.")
            else:
                print("\n--- All Tasks ---")
                for task in tasks:
                    print_task(task)

        elif command == "search":
            try:
                term = input("Enter search term: ")
                results = manager.search(term)
                if not results:
                    print("No tasks found matching your search.")
                else:
                    print(f"\n--- Search Results for '{term}' ---")
                    for task in results:
                        print_task(task)
            except ValueError as e:
                print(f"Error: {e}")

        elif command in ("finish", "remove"):
            try:
                task_id_str = input(f"Enter task ID to {command}: ")
                task_id = int(task_id_str)
                
                success = False
                if command == "finish":
                    success = manager.finish(task_id)
                elif command == "remove":
                    success = manager.remove(task_id)

                if success:
                    print(f"Success: Task {task_id} has been {command}ed.")
                else:
                    print(f"Error: Could not {command} task with ID {task_id}. It may not exist.")

            except ValueError:
                print("Error: Invalid ID. Please enter a number.")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

        elif command == "clear":
            confirm = input("Are you sure you want to delete all tasks? [y/N]: ").lower()
            if confirm == 'y':
                manager.clear_all()
                print("Success: All tasks have been cleared.")
            else:
                print("Operation cancelled.")
        
        else:
            print("Invalid command. Please try again.")


if __name__ == "__main__":
    main()
