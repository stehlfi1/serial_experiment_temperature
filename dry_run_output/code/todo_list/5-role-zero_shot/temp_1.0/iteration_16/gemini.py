
"""
A high-quality, console-based Todo List application.

This module contains the core logic for managing tasks in a TaskManager class
and a simple command-line interface for user interaction.
"""

from __future__ import annotations
import sys

# Define a type alias for a task dictionary for better readability and maintenance.
Task = dict[str, int | str | bool]


class TaskManager:
    """Manages a collection of tasks with CRUD-like operations.

    This class provides a clean, object-oriented interface for interacting with
    a list of tasks stored in memory. It is designed to be decoupled from any
    specific user interface, focusing solely on business logic.

    Attributes:
        _tasks (dict[int, Task]): A dictionary to store tasks, mapping task IDs
                                  to task data dictionaries. Using a dictionary
                                  provides efficient O(1) lookups for ID-based
                                  operations.
        _next_id (int): A counter to generate unique, sequential integer IDs
                        for new tasks.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """Adds a new task to the list.

        Args:
            task_name: The name or title of the task. Cannot be empty or
                       just whitespace.
            task_description: A detailed description of the task. Can be empty.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If `task_name` is empty or only contains whitespace.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty or contain only whitespace.")
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False if no task with the
            given ID was found.

        Raises:
            ValueError: If `task_id` is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> list[Task]:
        """Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for within task names and
                         descriptions.

        Returns:
            A list of task dictionaries that match the search term. Returns an
            empty list if the search term is empty or no tasks match.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            return []

        lower_term = search_term.lower()
        
        # List comprehension provides a concise and efficient way to filter
        return [
            task for task in self._tasks.values()
            if lower_term in task["name"].lower() or
               lower_term in task["description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False if no
            task with the given ID was found.

        Raises:
            ValueError: If `task_id` is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if task:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> list[Task]:
        """Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. The list is a copy, so
            modifying it will not affect the internal task storage.
        """
        return list(self._tasks.values())
        
    def clear_all(self) -> bool:
        """Deletes all tasks and resets the ID counter.
        
        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        print("\nAll tasks have been cleared.")
        return True


def _print_task(task: Task) -> None:
    """Helper function to print a single task in a formatted way."""
    status = "Finished" if task["is_finished"] else "Pending"
    print(
        f"  ID: {task['id']} | Status: {status}\n"
        f"  Name: {task['name']}\n"
        f"  Description: {task['description']}\n"
        f"  -------------------------------------"
    )

def _print_tasks(tasks: list[Task]) -> None:
    """Helper function to print a list of tasks."""
    if not tasks:
        print("\nNo tasks found.")
        return
    
    print("\n--- Your Tasks ---")
    for task in tasks:
        _print_task(task)

def main() -> None:
    """Main function to run the console-based UI for the Todo List app."""
    task_manager = TaskManager()
    
    # Pre-populate with some data for demonstration
    task_manager.add("Finish project report", "Complete the Q3 financial report for the board meeting.")
    task_manager.add("Buy groceries", "Milk, bread, eggs, and cheese.")
    task_manager.finish(2) # Mark 'Buy groceries' as finished

    menu = """
    Todo List Application
    =====================
    1. Add Task
    2. Remove Task
    3. Search Tasks
    4. Finish Task
    5. Show All Tasks
    6. Clear All Tasks
    7. Exit
    """

    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = task_manager.add(name, desc)
                print(f"\nSuccess: Task '{name}' added with ID {task_id}.")

            elif choice == "2":
                task_id_str = input("Enter the ID of the task to remove: ")
                task_id = int(task_id_str)
                if task_manager.remove(task_id):
                    print(f"\nSuccess: Task {task_id} removed.")
                else:
                    print(f"\nError: Task with ID {task_id} not found.")

            elif choice == "3":
                term = input("Enter search term: ")
                results = task_manager.search(term)
                _print_tasks(results)

            elif choice == "4":
                task_id_str = input("Enter the ID of the task to finish: ")
                task_id = int(task_id_str)
                if task_manager.finish(task_id):
                    print(f"\nSuccess: Task {task_id} marked as finished.")
                else:
                    print(f"\nError: Task with ID {task_id} not found.")

            elif choice == "5":
                all_tasks = task_manager.get_all()
                _print_tasks(all_tasks)
            
            elif choice == "6":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ").lower()
                if confirm == 'y':
                    task_manager.clear_all()
                else:
                    print("\nOperation cancelled.")

            elif choice == "7":
                print("Exiting application. Goodbye!")
                sys.exit(0)

            else:
                print("\nInvalid choice. Please enter a number between 1 and 7.")

        except ValueError as e:
            # Handles both invalid integer parsing and validation errors from TaskManager
            print(f"\nError: {e}")
        except Exception as e:
            # Generic catch-all for any other unexpected errors
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
