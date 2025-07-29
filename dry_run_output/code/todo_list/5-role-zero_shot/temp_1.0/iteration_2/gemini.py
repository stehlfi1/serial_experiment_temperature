
"""
A high-quality, console-based To-Do list application.

This module provides a TaskManager class to handle the core logic of a to-do list,
adhering to best practices for maintainability, reliability, and efficiency.
"""

from typing import Any, Dict, List

# Define a type alias for a Task dictionary for better readability and maintenance.
Task = Dict[str, Any]


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class encapsulates all the logic for adding, removing, searching,
    and modifying tasks. It is designed to be decoupled from any specific UI,
    making it reusable and easily testable.

    Attributes:
        _tasks (Dict[int, Task]): A dictionary to store tasks, mapping task ID to task data.
        _next_id (int): A counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID.

        Args:
            task_id: The ID of the task to validate.

        Raises:
            TypeError: If the task_id is not an integer.
            ValueError: If the task_id does not exist.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name or title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name is empty or just whitespace.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            # Ensure description is a string, even if empty.
            task_description = ""

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
        """
        Removes a task by its ID.

        Args:
            task_id: The unique ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID exists.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term.

        Raises:
            ValueError: If the search_term is empty or just whitespace.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower()
        results = [
            task.copy() for task in self._tasks.values()
            if lower_term in task['name'].lower() or lower_term in task['description'].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The unique ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID exists.
        """
        self._validate_task_id(task_id)
        if self._tasks[task_id]['is_finished']:
            # Task is already finished, an idempotent success.
            return True
        self._tasks[task_id]['is_finished'] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. Returns copies to prevent
            direct modification of internal data.
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        # Resetting the ID counter is a good practice when clearing all data.
        self._next_id = 1
        return True


# --- User Interface (UI) Layer ---
# This part is separate from the core logic to ensure modularity.

def print_tasks(tasks: List[Task]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return

    for task in tasks:
        status = "Finished" if task['is_finished'] else "Pending"
        print(
            f"  ID: {task['id']} | Status: {status}\n"
            f"  Name: {task['name']}\n"
            f"  Description: {task['description']}\n"
            f"  -------------------------------------"
        )


def main() -> None:
    """Main function to run the console-based UI for the To-Do app."""
    manager = TaskManager()
    print("--- Console To-Do List Application ---")

    # Pre-populate with some sample data for demonstration
    manager.add("Buy groceries", "Milk, Bread, Cheese")
    manager.add("Finish report", "Complete the Q3 financial report for the meeting.")
    manager.add("Call mom", "")

    while True:
        print("\nAvailable commands: add, remove, search, finish, all, clear, exit")
        command = input("Enter command: ").lower().strip()

        try:
            if command == "add":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"Success: Task added with ID {task_id}.")

            elif command == "remove":
                task_id_str = input("Enter task ID to remove: ")
                task_id = int(task_id_str)
                if manager.remove(task_id):
                    print(f"Success: Task with ID {task_id} removed.")

            elif command == "search":
                term = input("Enter search term: ")
                results = manager.search(term)
                print(f"\n--- Search results for '{term}' ---")
                print_tasks(results)

            elif command == "finish":
                task_id_str = input("Enter task ID to finish: ")
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"Success: Task with ID {task_id} marked as finished.")

            elif command == "all":
                print("\n--- All Tasks ---")
                all_tasks = manager.get_all()
                print_tasks(all_tasks)

            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ").lower()
                if confirm == 'yes':
                    if manager.clear_all():
                        print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif command == "exit":
                print("Exiting application. Goodbye!")
                break

            else:
                print("Error: Unknown command. Please try again.")

        except (ValueError, TypeError) as e:
            # Gracefully handle errors raised by the TaskManager
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

