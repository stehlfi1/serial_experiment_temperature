
"""
A high-quality, maintainable implementation of a console-based Todo List application.

This module provides a TaskManager class that handles all the core logic for managing tasks,
adhering to best practices and the principles of the ISO/IEC 25010 standard.
"""

import dataclasses
from typing import List, Dict, Any, Optional

# For enhanced readability and type safety, a dataclass is used to represent a task.
# This aligns with the 'Maintainability' and 'Reliability' characteristics.
@dataclasses.dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Task object to a dictionary."""
        return dataclasses.asdict(self)

class TaskManager:
    """
    Manages a collection of tasks with high-performance and robust error handling.

    This class encapsulates all the logic for the todo list application, ensuring
    modularity, testability, and maintainability. It uses a dictionary for
    in-memory storage to provide efficient O(1) average time complexity for
    ID-based lookups, insertions, and deletions.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_inputs(self, task_name: str, task_description: str) -> None:
        """
        Internal helper to validate string inputs.
        Raises:
            TypeError: If inputs are not strings.
            ValueError: If task_name is empty or only contains whitespace.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or just whitespace.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be empty.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is empty or contains only whitespace.
        """
        self._validate_inputs(task_name, task_description)
        
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
            True if the task was successfully removed, False otherwise (e.g., task not found).
        
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description (case-insensitive).

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.
            Returns an empty list if no matches are found or the search term is empty.

        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        if not search_term.strip():
            return []

        lower_term = search_term.lower()
        
        # List comprehension provides a concise and readable way to filter tasks.
        return [
            task.to_dict()
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise (e.g., task not found).

        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, where each task is represented as a dictionary.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter for a clean state
        return True


# --- Example Usage: Console Interface ---
# This section demonstrates how to use the TaskManager class and provides a
# simple, user-friendly console interface. It is kept separate from the core
# class logic to ensure modularity and testability.

def print_task(task: Dict[str, Any]):
    """Helper function to print a single task in a readable format."""
    status = "Finished" if task['is_finished'] else "Pending"
    print(f"  ID: {task['id']}, Status: {status}")
    print(f"  Name: {task['name']}")
    print(f"  Description: {task['description']}")
    print("-" * 20)

def main():
    """Main function to run the console-based todo list application."""
    manager = TaskManager()
    print("--- Console Todo List Application ---")

    # Pre-populate with some data for demonstration
    manager.add("Groceries", "Buy milk, bread, and eggs")
    manager.add("Project", "Finish the report for the Q3 meeting")
    manager.add("Clean Garage", "Organize tools and sweep the floor")

    while True:
        print("\nAvailable commands: add, remove, search, finish, list, clear, exit")
        command = input("Enter command: ").lower().strip()

        try:
            if command == "add":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Successfully added task with ID: {task_id}")

            elif command == "remove":
                task_id_str = input("Enter task ID to remove: ")
                task_id = int(task_id_str)
                if manager.remove(task_id):
                    print(f"Task {task_id} removed successfully.")
                else:
                    print(f"Error: Task with ID {task_id} not found.")

            elif command == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                if not results:
                    print("No tasks found matching your search.")
                else:
                    print(f"Found {len(results)} matching task(s):")
                    for task in results:
                        print_task(task)

            elif command == "finish":
                task_id_str = input("Enter task ID to mark as finished: ")
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"Task {task_id} marked as finished.")
                else:
                    print(f"Error: Task with ID {task_id} not found.")

            elif command == "list":
                all_tasks = manager.get_all()
                if not all_tasks:
                    print("Your todo list is empty.")
                else:
                    print("\n--- All Tasks ---")
                    for task in all_tasks:
                        print_task(task)

            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    manager.clear_all()
                    print("All tasks have been cleared.")
                else:
                    print("Operation cancelled.")
            
            elif command == "exit":
                print("Exiting application. Goodbye!")
                break

            else:
                print("Invalid command. Please try again.")

        except (ValueError, TypeError) as e:
            # Gracefully handle validation errors from the TaskManager
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
