
"""
A high-quality, maintainable implementation of a Todo List Manager.

This module provides the TaskManager class, which encapsulates all logic
for managing a collection of tasks in memory. It is designed with the
ISO/IEC 25010 standard in mind, focusing on correctness, efficiency,
and maintainability.
"""

from typing import List, Dict, Any

# --- Custom Exceptions for Clear Error Handling ---

class TaskManagerError(Exception):
    """Base exception for all TaskManager related errors."""
    pass

class TaskNotFoundError(TaskManagerError, KeyError):
    """Raised when a task with the given ID is not found."""
    pass

class InvalidTaskDataError(TaskManagerError, ValueError):
    """Raised when provided task data is invalid (e.g., empty strings)."""
    pass


# --- Main Task Management Logic ---

class TaskManager:
    """
    Manages a collection of tasks in an in-memory data store.

    This class provides a clean, object-oriented interface for adding,
    removing, searching, and updating tasks.

    Attributes:
        _tasks (Dict[int, Dict[str, Any]]): A private dictionary to store tasks.
            The key is the task ID, and the value is a dictionary
            containing task details.
        _next_id (int): A private counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be an empty string.
            task_description: A short description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            InvalidTaskDataError: If task_name is empty or whitespace.
        """
        if not task_name or not task_name.strip():
            raise InvalidTaskDataError("Task name cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False
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
            TaskNotFoundError: If no task with the given ID is found.
            InvalidTaskDataError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskDataError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term. An empty
            list is returned if no matches are found.

        Raises:
            InvalidTaskDataError: If the search_term is empty or whitespace.
        """
        if not search_term or not search_term.strip():
            raise InvalidTaskDataError("Search term cannot be empty.")

        term = search_term.lower().strip()
        results = []
        for task_id, details in self._tasks.items():
            if term in details["name"].lower() or term in details["description"].lower():
                results.append(self._format_task(task_id, details))
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TaskNotFoundError: If no task with the given ID is found.
            InvalidTaskDataError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskDataError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID '{task_id}' not found.")

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries.
        """
        return [self._format_task(task_id, details)
                for task_id, details in self._tasks.items()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True

    def _format_task(self, task_id: int, details: Dict[str, Any]) -> Dict[str, Any]:
        """
        A helper method to consistently format task output.

        Args:
            task_id: The ID of the task.
            details: The dictionary containing task details.

        Returns:
            A formatted dictionary including the ID.
        """
        return {
            "id": task_id,
            "name": details["name"],
            "description": details["description"],
            "is_finished": details["is_finished"]
        }



# --- Example Command-Line Interface ---

def print_task(task: Dict[str, Any]):
    """Helper function to print a single task in a user-friendly format."""
    status = "✓" if task["is_finished"] else "✗"
    print(f"[{status}] ID: {task['id']} | {task['name']} - {task['description']}")

def run_cli():
    """Runs the command-line interface for the TaskManager."""
    manager = TaskManager()
    print("--- Console Todo List App ---")

    # Pre-populate with some data for demonstration
    try:
        manager.add("Buy groceries", "Milk, Bread, Cheese")
        manager.add("Finish report", "Complete the Q3 financial report.")
        manager.add("Call dentist", "Schedule a check-up for next week.")
    except InvalidTaskDataError as e:
        print(f"Initialization Error: {e}")

    while True:
        print("\nCommands: add, remove, search, finish, all, clear, exit")
        command = input("Enter command: ").strip().lower()

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
                if not results:
                    print("No tasks found matching your search.")
                else:
                    print("--- Search Results ---")
                    for task in results:
                        print_task(task)
                    print("----------------------")

            elif command == "finish":
                task_id = int(input("Enter task ID to finish: "))
                manager.finish(task_id)
                print(f"Success: Task {task_id} marked as finished.")

            elif command == "all":
                tasks = manager.get_all()
                if not tasks:
                    print("The todo list is empty.")
                else:
                    print("\n--- All Tasks ---")
                    for task in tasks:
                        print_task(task)
                    print("-----------------")

            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    manager.clear_all()
                    print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif command == "exit":
                print("Exiting application. Goodbye!")
                break

            else:
                print("Unknown command. Please try again.")

        except (TaskNotFoundError, InvalidTaskDataError) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Please enter a valid number for the task ID.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_cli()
