
"""
A high-quality, maintainable console-based Todo List application.

This module contains the core logic for managing tasks in a TaskManager class,
adhering to OOP principles and best practices for code quality.

ISO/IEC 25010 Considerations:
- Functional Suitability: Implements all specified functionalities (add, remove, etc.).
- Performance Efficiency: Uses a dictionary for efficient O(1) lookups by ID.
- Maintainability: Code is modular, documented, and uses clear naming.
- Reliability: Robust validation and error handling are implemented.
- Usability: The class API is clean and predictable.
- Security: Input validation protects against invalid data states.
"""

import sys
from typing import List, Dict, Any, Union

# Define a type alias for a task dictionary for better readability and maintenance.
Task = Dict[str, Union[int, str, bool]]


class TaskManager:
    """
    Manages a collection of tasks with functionalities to add, remove, and query.

    Attributes:
        _tasks (dict[int, Task]): A private dictionary to store tasks,
                                  mapping task IDs to task data.
        _next_id (int): A private counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task list and sets the
        initial ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name/title of the task. Must be a non-empty string.
            task_description (str): A detailed description of the task.

        Returns:
            int: The unique ID assigned to the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is empty or contains only whitespace.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name,
            "task_description": task_description,
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was successfully removed, False otherwise.
        
        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        if task_id in self._tasks:
            self._tasks[task_id]["is_finished"] = True
            return True
        return False

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks where the search term appears in the name or description.
        The search is case-insensitive.

        Args:
            search_term (str): The string to search for.

        Returns:
            list[dict]: A list of tasks matching the search criteria. Returns an
                        empty list if the search term is empty or no tasks match.
        
        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        
        if not search_term.strip():
            return []

        lower_search_term = search_term.lower()
        
        return [
            task for task in self._tasks.values()
            if lower_search_term in task["task_name"].lower()
            or lower_search_term in task["task_description"].lower()
        ]

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks currently in the manager.

        Returns:
            list[dict]: A list of all task dictionaries.
        """
        # Return a copy of the list of values to prevent external modification
        # of the internal state.
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Removes all tasks from the manager.

        Returns:
            bool: True indicating the operation was successful.
        """
        self._tasks.clear()
        # Resetting the ID counter can be a design choice. Here we reset it
        # for simplicity when all tasks are cleared.
        self._next_id = 1
        return True


# --- Console User Interface (for demonstration) ---

def print_tasks(tasks: List[Task]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return

    print("-" * 60)
    print(f"{'ID':<5} | {'Status':<10} | {'Name':<20} | {'Description'}")
    print("-" * 60)
    for task in tasks:
        status = "Finished" if task["is_finished"] else "Pending"
        print(
            f"{task['id']:<5} | {status:<10} | {task['task_name']:<20} | {task['task_description']}"
        )
    print("-" * 60)


def main() -> None:
    """Main function to run the console-based UI for the TaskManager."""
    task_manager = TaskManager()
    print("--- Console Todo List App ---")

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Finish Task")
        print("4. List All Tasks")
        print("5. Search Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = task_manager.add(name, desc)
                print(f"Success: Task added with ID: {task_id}")

            elif choice == '2':
                task_id_str = input("Enter task ID to remove: ")
                if task_manager.remove(int(task_id_str)):
                    print(f"Success: Task with ID {task_id_str} removed.")
                else:
                    print(f"Error: Task with ID {task_id_str} not found.")

            elif choice == '3':
                task_id_str = input("Enter task ID to finish: ")
                if task_manager.finish(int(task_id_str)):
                    print(f"Success: Task with ID {task_id_str} marked as finished.")
                else:
                    print(f"Error: Task with ID {task_id_str} not found.")

            elif choice == '4':
                print("\n--- All Tasks ---")
                print_tasks(task_manager.get_all())

            elif choice == '5':
                term = input("Enter search term: ")
                results = task_manager.search(term)
                print(f"\n--- Search Results for '{term}' ---")
                print_tasks(results)

            elif choice == '6':
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ")
                if confirm.lower() == 'yes':
                    task_manager.clear_all()
                    print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == '7':
                print("Exiting application. Goodbye!")
                sys.exit(0)

            else:
                print("Invalid choice. Please enter a number between 1 and 7.")

        except (ValueError, TypeError) as e:
            # Gracefully handle validation errors from the TaskManager or int() conversion
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
