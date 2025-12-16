
"""
A high-quality, console-based Todo List application.

This module provides a TaskManager class that encapsulates the core logic for
managing tasks, and a simple command-line interface (CLI) for user interaction.
The design adheres to ISO/IEC 25010 principles for software quality.
"""

from typing import List, Dict, Any, Union

# Define a type alias for a task dictionary for better readability and maintenance.
Task = Dict[str, Union[int, str, bool]]


class TaskManager:
    """
    Manages a collection of tasks with high-quality standards.

    This class handles all business logic for the todo list, including
    adding, removing, and querying tasks. It is designed to be decoupled
    from any specific user interface.

    Attributes:
        _tasks (dict[int, Task]): Internal storage for tasks, mapping task ID to task data.
        _next_id (int): A counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: A description of the task. Must be a non-empty string.

        Returns:
            The unique ID of the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name or task_description are empty or just whitespace.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip() or not task_description.strip():
            raise ValueError("Task name and description cannot be empty.")

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
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

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
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = search_term.lower()
        return [
            task for task in self._tasks.values()
            if term_lower in task["name"].lower() or term_lower in task["description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. Returns a copy to prevent
            mutation of internal data structure.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks and resets the ID counter.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


def print_tasks(tasks: List[Task]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("\nNo tasks found.")
        return
    print("\n--- Tasks ---")
    for task in tasks:
        status = "X" if task["is_finished"] else " "
        print(f"[{status}] ID: {task['id']} | {task['name']} - {task['description']}")
    print("-------------")


def print_menu() -> None:
    """Prints the main menu for the console application."""
    print("\n===== Todo List Menu =====")
    print("1. Add a new task")
    print("2. Remove a task")
    print("3. Mark a task as finished")
    print("4. List all tasks")
    print("5. Search for a task")
    print("6. Clear all tasks")
    print("7. Exit")
    print("==========================")


def main() -> None:
    """Main function to run the console-based UI for the TaskManager."""
    manager = TaskManager()
    print("Welcome to the Todo List App!")

    while True:
        print_menu()
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"\nSuccess: Task '{name}' added with ID {task_id}.")

            elif choice == "2":
                task_id_str = input("Enter task ID to remove: ")
                manager.remove(int(task_id_str))
                print(f"\nSuccess: Task with ID {task_id_str} has been removed.")

            elif choice == "3":
                task_id_str = input("Enter task ID to mark as finished: ")
                manager.finish(int(task_id_str))
                print(f"\nSuccess: Task with ID {task_id_str} marked as finished.")

            elif choice == "4":
                all_tasks = manager.get_all()
                print_tasks(all_tasks)

            elif choice == "5":
                term = input("Enter search term: ")
                found_tasks = manager.search(term)
                print(f"\nFound {len(found_tasks)} task(s) matching '{term}':")
                print_tasks(found_tasks)

            elif choice == "6":
                confirm = input("Are you sure you want to delete all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    manager.clear_all()
                    print("\nSuccess: All tasks have been cleared.")
                else:
                    print("\nOperation cancelled.")

            elif choice == "7":
                print("\nThank you for using the Todo List App. Goodbye!")
                break

            else:
                print("\nError: Invalid choice. Please select a valid option.")

        except (ValueError, TypeError, KeyError) as e:
            # Gracefully handle all expected errors from the TaskManager
            print(f"\nError: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
