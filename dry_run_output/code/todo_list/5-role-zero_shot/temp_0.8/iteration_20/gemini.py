
"""
A high-quality, console-based Todo List application.

This module provides a TaskManager class that implements the core logic for a
todo list application. It is designed with the ISO/IEC 25010 standard in mind,
prioritizing maintainability, reliability, and performance efficiency.

The module also includes a simple command-line interface (CLI) for demonstration
and direct interaction.
"""

import sys
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# --- Data Modeling ---

@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Using a dataclass provides type safety, immutability for the ID, and a
    clear, self-documenting structure for our data model.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


# --- Core Logic / Business Layer ---

class TaskManager:
    """
    Manages all operations related to tasks.

    This class encapsulates the entire logic for the todo list, including
    storage, retrieval, and modification of tasks. It uses an in-memory
    dictionary for efficient data handling, making it highly performant for
    key-based operations.
    """

    def __init__(self):
        """Initializes the TaskManager with an in-memory storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, *args: str):
        """Private helper to validate that string inputs are not empty."""
        for arg in args:
            if not isinstance(arg, str) or not arg.strip():
                raise ValueError("Task name and description cannot be empty.")

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """Converts a Task object to a dictionary for consistent output."""
        return asdict(task)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name or task_description are empty or invalid.
        """
        self._validate_string_input(task_name, task_description)
        
        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description.strip())
        self._tasks[task_id] = new_task
        self._next_id += 1
        
        print(f"✅ Task '{task_name}' added with ID {task_id}.")
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            print("❌ Error: Task ID must be a positive integer.")
            return False

        if task_id in self._tasks:
            del self._tasks[task_id]
            print(f"✅ Task with ID {task_id} removed.")
            return True
        
        print(f"❌ Error: Task with ID {task_id} not found.")
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by name or description.

        The search is case-insensitive.

        Args:
            search_term: The term to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.

        Raises:
            ValueError: If the search_term is empty.
        """
        self._validate_string_input(search_term)
        
        lower_term = search_term.lower()
        results = [
            self._task_to_dict(task) for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]
        
        print(f"🔎 Found {len(results)} task(s) matching '{search_term}'.")
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            print("❌ Error: Task ID must be a positive integer.")
            return False
            
        task = self._tasks.get(task_id)
        if task:
            if task.is_finished:
                print(f"ℹ️ Task with ID {task_id} is already marked as finished.")
            else:
                task.is_finished = True
                print(f"✅ Task '{task.name}' (ID: {task_id}) marked as finished.")
            return True

        print(f"❌ Error: Task with ID {task_id} not found.")
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, where each task is a dictionary.
        """
        if not self._tasks:
            print("ℹ️ The todo list is empty.")
            return []
            
        return [self._task_to_dict(task) for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset ID counter
        print("🗑️ All tasks have been cleared.")
        return True

# --- Presentation Layer / Command-Line Interface ---

def print_tasks(tasks: List[Dict[str, Any]]):
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        return
    print("-" * 50)
    for task in tasks:
        status = "✅ Finished" if task['is_finished'] else "⏳ Pending"
        print(f"ID: {task['id']} | {task['name']} | Status: {status}")
        print(f"   Description: {task['description']}")
        print("-" * 50)

def print_help():
    """Prints the help menu for the CLI."""
    print("\n--- Todo List Menu ---")
    print("  add    - Add a new task")
    print("  list   - List all tasks")
    print("  search - Search for a task")
    print("  finish - Mark a task as finished")
    print("  remove - Remove a task")
    print("  clear  - Clear all tasks")
    print("  help   - Show this help menu")
    print("  exit   - Exit the application")
    print("----------------------\n")

def main():
    """Main function to run the console-based UI."""
    task_manager = TaskManager()
    print("Welcome to the Console Todo List App!")
    print_help()
    
    while True:
        command = input("> ").lower().strip()

        try:
            if command == "add":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_manager.add(name, desc)

            elif command == "list":
                all_tasks = task_manager.get_all()
                print_tasks(all_tasks)

            elif command == "search":
                term = input("Enter search term: ")
                found_tasks = task_manager.search(term)
                print_tasks(found_tasks)

            elif command == "finish":
                task_id_str = input("Enter task ID to mark as finished: ")
                if task_id_str.isdigit():
                    task_manager.finish(int(task_id_str))
                else:
                    print("❌ Error: Invalid ID. Please enter a number.")

            elif command == "remove":
                task_id_str = input("Enter task ID to remove: ")
                if task_id_str.isdigit():
                    task_manager.remove(int(task_id_str))
                else:
                    print("❌ Error: Invalid ID. Please enter a number.")
            
            elif command == "clear":
                confirm = input("Are you sure you want to clear all tasks? (y/n): ").lower()
                if confirm == 'y':
                    task_manager.clear_all()
                else:
                    print("ℹ️ Operation cancelled.")

            elif command == "help":
                print_help()

            elif command == "exit":
                print("👋 Goodbye!")
                sys.exit(0)

            else:
                print(f"❌ Unknown command: '{command}'. Type 'help' for a list of commands.")

        except ValueError as e:
            print(f"❌ Input Error: {e}")
        except Exception as e:
            # Generic catch-all for unexpected errors, promoting reliability.
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
