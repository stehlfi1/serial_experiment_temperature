
"""
A high-quality, console-based Todo List application.

This module provides a TaskManager class that handles the business logic for
a todo list, adhering to the principles of the ISO/IEC 25010 standard for
software quality.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# Define a structured data class for a Task to improve readability and type safety.
@dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int
    name: str
    description: str
    is_finished: bool = False

class TaskManager:
    """
    Manages a collection of tasks with high-quality, maintainable code.

    This class provides a clean interface for adding, removing, searching,
    and modifying tasks stored in memory. It is designed for efficiency,
    safety, and testability.

    Attributes:
        _tasks (Dict[int, Task]): A dictionary to store tasks, mapping task ID to Task object.
                                  This provides O(1) average time complexity for lookups.
        _next_id (int): A counter to generate unique IDs for new tasks.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: The description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name is empty or just whitespace.
            TypeError: If task_name or task_description are not strings.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description)
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
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            KeyError: If no task with the given ID exists.
        """
        self._validate_id(task_id)
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower()
        results = [
            asdict(task) for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            KeyError: If no task with the given ID exists.
        """
        self._validate_id(task_id)
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        self._tasks[task_id].is_finished = True
        return True

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
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True

    def _validate_id(self, task_id: Any) -> None:
        """
        Internal helper to validate a task ID.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")


def print_tasks(tasks: List[Dict[str, Any]]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return

    print("-" * 60)
    for task in tasks:
        status = "Finished" if task['is_finished'] else "Pending"
        print(f"ID: {task['id']} | Status: {status}")
        print(f"  Name: {task['name']}")
        print(f"  Description: {task['description']}")
        print("-" * 60)


def main() -> None:
    """Main function to run the console-based UI for the Todo List App."""
    manager = TaskManager()
    print("--- Console Todo List Application ---")

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Finish Task")
        print("5. List All Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"✅ Success: Task added with ID {task_id}.")

            elif choice == '2':
                task_id_str = input("Enter task ID to remove: ")
                manager.remove(int(task_id_str))
                print(f"✅ Success: Task with ID {task_id_str} removed.")

            elif choice == '3':
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\n--- Search Results for '{term}' ---")
                print_tasks(results)

            elif choice == '4':
                task_id_str = input("Enter task ID to finish: ")
                manager.finish(int(task_id_str))
                print(f"✅ Success: Task with ID {task_id_str} marked as finished.")

            elif choice == '5':
                all_tasks = manager.get_all()
                print("\n--- All Tasks ---")
                print_tasks(all_tasks)

            elif choice == '6':
                confirm = input("Are you sure you want to delete all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    manager.clear_all()
                    print("✅ Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == '7':
                print("Exiting application. Goodbye!")
                break
            else:
                print("❌ Error: Invalid choice. Please enter a number between 1 and 7.")

        except (ValueError, TypeError, KeyError) as e:
            # Gracefully handle all expected errors from the TaskManager
            print(f"❌ Error: {e}")
        except Exception as e:
            # Catch any unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
