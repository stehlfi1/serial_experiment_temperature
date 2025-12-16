
"""
A high-quality, maintainable, and efficient console-based todo list application.

This module provides a TaskManager class that adheres to the principles of
ISO/IEC 25010, focusing on reliability, performance, and maintainability.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# --- Data Model (Modularity) ---

@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Using a dataclass provides a structured, readable, and type-safe way
    to handle task data.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False


# --- Core Logic (Encapsulation, Efficiency, Reliability) ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface to add, remove, search, and
    update tasks, with a focus on performance and data integrity.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an in-memory data store.

        A dictionary is used for O(1) average time complexity for lookups,
        insertions, and deletions by task ID, which is highly efficient.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Private helper to validate a task ID. (Safety & Reusability)

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            KeyError: If task_id does not exist in the task list.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID '{task_id}' not found.")

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to its dictionary representation. (Maintainability)
        
        This ensures a consistent output format for all public methods.
        """
        return asdict(task)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be empty.
            task_description: A description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

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
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError, ValueError, KeyError: Propagated from _validate_task_id.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty or whitespace-only string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower()
        return [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError, ValueError, KeyError: Propagated from _validate_task_id.
        """
        self._validate_task_id(task_id)
        self._tasks[task_id].is_finished = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
            The list is sorted by task ID.
        """
        # Sorting by ID provides a predictable and user-friendly order.
        sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.id)
        return [self._task_to_dict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        This operation is irreversible. It also resets the ID counter.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Console UI (Example Usage & Testability) ---

def print_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return
    
    print("-" * 60)
    print(f"{'ID':<5} {'Status':<10} {'Name':<20} {'Description'}")
    print("-" * 60)
    for task in tasks:
        status = "Done" if task['is_finished'] else "Pending"
        print(
            f"{task['id']:<5} {status:<10} {task['name']:<20} {task['description']}"
        )
    print("-" * 60)


def main() -> None:
    """Main function to run the console-based todo list application."""
    manager = TaskManager()
    print("--- Console Todo List Application ---")

    # Pre-populate with some data for demonstration
    manager.add("Buy groceries", "Milk, Bread, Cheese")
    manager.add("Finish report", "Complete the Q3 financial report")
    manager.add("Call plumber", "Fix the leaky faucet in the kitchen")

    while True:
        print("\nAvailable commands: add, remove, search, finish, list, clear, exit")
        command = input("Enter command: ").lower().strip()

        try:
            if command == "add":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Success: Task added with ID {task_id}.")
            
            elif command == "remove":
                task_id = int(input("Enter task ID to remove: "))
                manager.remove(task_id)
                print(f"Success: Task {task_id} removed.")

            elif command == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\n--- Search Results for '{term}' ---")
                print_tasks(results)

            elif command == "finish":
                task_id = int(input("Enter task ID to finish: "))
                manager.finish(task_id)
                print(f"Success: Task {task_id} marked as finished.")

            elif command == "list":
                print("\n--- All Tasks ---")
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
                break
            
            else:
                print("Invalid command. Please try again.")

        except (ValueError, TypeError, KeyError) as e:
            # Graceful error handling
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
