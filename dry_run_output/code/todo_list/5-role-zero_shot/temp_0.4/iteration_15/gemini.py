
"""
A high-quality, console-based Todo List application.

This module provides a TaskManager class that handles the core logic for managing
a list of tasks. It is designed following OOP principles and adheres to the
ISO/IEC 25010 standard for software quality.

Author: AI Assistant (Senior Software Developer Persona)
Version: 1.0.0
"""

import sys
from typing import List, Dict, Any, TypedDict

# --- Data Structures and Custom Exceptions ---

class Task(TypedDict):
    """
    Represents the structure of a task using a TypedDict for clarity
    and static analysis benefits.
    """
    id: int
    name: str
    description: str
    is_finished: bool

class TaskManagerError(Exception):
    """Base exception for the TaskManager."""
    pass

class TaskNotFoundError(TaskManagerError):
    """Raised when a task with a given ID is not found."""
    pass

class InvalidTaskDataError(ValueError, TaskManagerError):
    """Raised when provided task data is invalid (e.g., empty name)."""
    pass


# --- Core Logic ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class encapsulates all the logic for adding, removing, searching,
    and modifying tasks. It is designed to be decoupled from any specific UI,
    making it reusable and easily testable.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an in-memory data store.
        
        _tasks is a dictionary for O(1) average time complexity for lookups.
        _next_id ensures unique, sequential IDs for new tasks.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description for the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            InvalidTaskDataError: If task_name is empty or not a string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise InvalidTaskDataError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            # Ensure description is a string, even if empty
            task_description = str(task_description)

        task_id = self._next_id
        new_task: Task = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False,
        }
        self._tasks[task_id] = new_task
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
            TaskNotFoundError: If no task with the given ID is found.
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")
        
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks by name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for in task names and descriptions.

        Returns:
            A list of tasks matching the search term. An empty list is returned
            if no matches are found or the search term is empty.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            return []
            
        lower_term = search_term.lower()
        return [
            task for task in self._tasks.values()
            if lower_term in task["name"].lower() or \
               lower_term in task["description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TaskNotFoundError: If no task with the given ID is found.
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")
            
        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, sorted by ID.
        """
        return sorted(self._tasks.values(), key=lambda t: t['id'])

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful deletion of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Console User Interface (UI) ---

def print_task(task: Task) -> None:
    """Formats and prints a single task to the console."""
    status = "✓ Done" if task["is_finished"] else "✗ Pending"
    print(
        f"  ID: {task['id']} | Status: {status}\n"
        f"  Name: {task['name']}\n"
        f"  Description: {task['description']}\n"
        f"  ----------------------------------------"
    )

def print_help() -> None:
    """Prints the available commands to the user."""
    print("\n--- Todo List Commands ---")
    print("  add <name> | <description>   - Add a new task (use '|' to separate name and description)")
    print("  remove <id>                  - Remove a task by its ID")
    print("  finish <id>                  - Mark a task as finished")
    print("  search <term>                - Search for tasks")
    print("  list                         - Show all tasks")
    print("  clear                        - Delete all tasks")
    print("  help                         - Show this help message")
    print("  exit                         - Exit the application")
    print("--------------------------\n")

def main() -> None:
    """
    Main function to run the console-based UI for the TaskManager.
    This function handles user input, calls the appropriate TaskManager methods,
    and prints results or error messages to the console.
    """
    manager = TaskManager()
    print("Welcome to the Console Todo List App!")
    print_help()

    while True:
        try:
            command_line = input("> ").strip().lower()
            if not command_line:
                continue

            parts = command_line.split(maxsplit=1)
            command = parts[0]
            args = parts[1] if len(parts) > 1 else ""

            if command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                print_help()
            elif command == "add":
                if '|' in args:
                    name, desc = [part.strip() for part in args.split('|', 1)]
                else:
                    name, desc = args.strip(), ""
                
                task_id = manager.add(name, desc)
                print(f"✅ Success: Added task with ID {task_id}.")
            elif command == "list":
                tasks = manager.get_all()
                if not tasks:
                    print("ℹ️  No tasks found. Add one with 'add <name>'.")
                else:
                    print("\n--- All Tasks ---")
                    for task in tasks:
                        print_task(task)
            elif command == "remove":
                task_id = int(args)
                manager.remove(task_id)
                print(f"✅ Success: Removed task with ID {task_id}.")
            elif command == "finish":
                task_id = int(args)
                manager.finish(task_id)
                print(f"✅ Success: Marked task {task_id} as finished.")
            elif command == "search":
                results = manager.search(args)
                if not results:
                    print(f"ℹ️  No tasks found matching '{args}'.")
                else:
                    print(f"\n--- Search Results for '{args}' ---")
                    for task in results:
                        print_task(task)
            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    manager.clear_all()
                    print("✅ Success: All tasks have been deleted.")
                else:
                    print("ℹ️  Operation cancelled.")
            else:
                print(f"❌ Error: Unknown command '{command}'. Type 'help' for a list of commands.")

        except (InvalidTaskDataError, TaskNotFoundError, TypeError) as e:
            print(f"❌ Error: {e}")
        except ValueError:
            print("❌ Error: Invalid ID. Please provide a valid integer.")
        except IndexError:
            print("❌ Error: Missing argument. Please provide the required arguments for the command.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
