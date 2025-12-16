
"""
A high-quality, maintainable implementation of a console-based Todo List application.

This module provides the TaskManager class, which handles the core logic for managing
tasks, and a simple command-line interface (CLI) for user interaction.

The implementation adheres to the principles of the ISO/IEC 25010 standard:
- Functional Suitability: Implements all required features (add, remove, etc.).
- Performance Efficiency: Uses efficient data structures (dictionaries) for
  time-critical operations like lookups and deletions.
- Reliability: Employs robust error handling and input validation to ensure
  stable operation.
- Maintainability: Features a modular design (logic separated from UI), clear
  documentation, and readable code, making it easy to test, modify, and reuse.
- Usability: The developer-facing API is clean and predictable, while the
  end-user CLI is straightforward.
"""

import sys
from typing import Any, Dict, List

# Define a type alias for a task dictionary for better readability and maintenance.
Task = Dict[str, Any]


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides the core business logic for a todo list application.
    It is designed to be completely independent of the user interface,
    allowing it to be reused in different contexts (e.g., CLI, GUI, web API).
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up the in-memory data structures for storing tasks and managing
        unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, input_str: str, field_name: str) -> None:
        """
        Private helper to validate that a string input is not empty or just whitespace.

        Args:
            input_str: The string to validate.
            field_name: The name of the field being validated (for error messages).

        Raises:
            TypeError: If the input is not a string.
            ValueError: If the input string is empty or contains only whitespace.
        """
        if not isinstance(input_str, str):
            raise TypeError(f"{field_name} must be a string.")
        if not input_str.strip():
            raise ValueError(f"{field_name} cannot be empty or just whitespace.")

    def _find_task(self, task_id: int) -> Task:
        """
        Private helper to find a task by its ID, with validation.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The task dictionary if found.

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
            task_name: The name/title of the task. Cannot be empty.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
        """
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")

        task_id = self._next_id
        self._tasks[task_id] = {
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
            ValueError: If no task with the given ID is found.
        """
        self._find_task(task_id)  # Ensures the task exists before deletion
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks where the search term appears in the name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search criteria. The list
            is empty if no matches are found.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty or whitespace-only string.
        """
        self._validate_string_input(search_term, "Search term")
        normalized_term = search_term.lower().strip()
        
        results = []
        for task_id, task_data in self._tasks.items():
            if (normalized_term in task_data["task_name"].lower() or
                normalized_term in task_data["task_description"].lower()):
                # Construct the full task object for the return value
                results.append({"id": task_id, **task_data})
        
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID is found.
        """
        task = self._find_task(task_id)
        if task["is_finished"]:
            # Optional: Inform the user it's already done.
            # For a boolean API, simply succeeding is fine.
            print(f"Info: Task {task_id} was already finished.")
        task["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all task dictionaries. Each dictionary includes the 'id'.
            Returns an empty list if no tasks exist.
        """
        return [{"id": task_id, **task_data} for task_id, task_data in self._tasks.items()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        This action is irreversible and also resets the task ID counter.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


def print_task(task: Task) -> None:
    """Helper function to format and print a single task."""
    status = "✓ Finished" if task["is_finished"] else "✗ Pending"
    print(
        f"  ID: {task['id']}\n"
        f"  Name: {task['task_name']}\n"
        f"  Description: {task['task_description']}\n"
        f"  Status: {status}\n"
        f"  {'-'*20}"
    )

def print_help() -> None:
    """Prints the available commands to the console."""
    print("\n--- Todo List Commands ---")
    print("  add          - Add a new task")
    print("  list         - List all tasks")
    print("  search       - Search for tasks")
    print("  finish <id>  - Mark a task as finished")
    print("  remove <id>  - Remove a task")
    print("  clear        - Remove all tasks")
    print("  help         - Show this help message")
    print("  exit         - Exit the application")
    print("--------------------------\n")

def main() -> None:
    """
    Main function to run the console-based UI for the TaskManager.
    
    This function handles user input, calls the appropriate TaskManager methods,
    and prints formatted output to the console. It demonstrates how to use the

    TaskManager class and gracefully handles potential errors.
    """
    task_manager = TaskManager()
    print("Welcome to the Console Todo List App!")
    print_help()

    while True:
        try:
            command_input = input("> ").strip().lower().split(maxsplit=1)
            if not command_input:
                continue

            command = command_input[0]
            args = command_input[1] if len(command_input) > 1 else ""

            if command == "add":
                name = input("  Enter task name: ")
                desc = input("  Enter task description: ")
                task_id = task_manager.add(name, desc)
                print(f"\nSuccess: Task '{name}' added with ID {task_id}.")
            
            elif command == "list":
                tasks = task_manager.get_all()
                if not tasks:
                    print("\nNo tasks found. Add one with the 'add' command.")
                else:
                    print("\n--- All Tasks ---")
                    for task in tasks:
                        print_task(task)
            
            elif command == "search":
                if not args:
                    print("Error: Please provide a search term. Usage: search <term>")
                    continue
                results = task_manager.search(args)
                if not results:
                    print(f"\nNo tasks found matching '{args}'.")
                else:
                    print(f"\n--- Search Results for '{args}' ---")
                    for task in results:
                        print_task(task)

            elif command == "finish":
                if not args:
                    print("Error: Please provide a task ID. Usage: finish <id>")
                    continue
                task_id = int(args)
                task_manager.finish(task_id)
                print(f"\nSuccess: Task {task_id} marked as finished.")

            elif command == "remove":
                if not args:
                    print("Error: Please provide a task ID. Usage: remove <id>")
                    continue
                task_id = int(args)
                task_manager.remove(task_id)
                print(f"\nSuccess: Task {task_id} removed.")

            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    task_manager.clear_all()
                    print("\nSuccess: All tasks have been cleared.")
                else:
                    print("\nOperation cancelled.")

            elif command == "help":
                print_help()

            elif command == "exit":
                print("Goodbye!")
                sys.exit(0)

            else:
                print(f"Error: Unknown command '{command}'. Type 'help' for a list of commands.")

        except (ValueError, TypeError) as e:
            # Gracefully handle validation and type errors from the TaskManager
            print(f"\nError: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
