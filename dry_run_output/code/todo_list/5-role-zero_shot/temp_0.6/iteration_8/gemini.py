
import sys
from typing import List, Dict, Any, Union

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides functionalities to add, remove, search, and update tasks,
    adhering to high-quality code standards for maintainability and reliability.
    It is designed to be easily testable and modular, forming the core logic
    for a todo list application.

    Characteristics based on ISO/IEC 25010:
    - Functional Suitability: Implements all required functionalities correctly.
    - Performance Efficiency: Uses a dictionary for O(1) average time complexity
      for lookups, insertions, and deletions by ID.
    - Reliability: Employs robust error handling and input validation.
    - Maintainability: Code is modular, well-documented, and readable.
    - Testability: The class is self-contained with no external dependencies,
      making it easy to unit test.

    Attributes:
        _tasks (Dict[int, Dict[str, Union[int, str, bool]]]): A private dictionary
            to store tasks. The key is the task ID, and the value is a dictionary
            representing the task's properties.
        _next_id (int): A private counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Dict[str, Union[int, str, bool]]] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name of the task. Cannot be an empty string.
            task_description: The description of the task. Cannot be an empty string.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name or task_description is empty or contains only whitespace.
            TypeError: If task_name or task_description are not strings.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The integer ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a term in their name or description.

        The search is case-insensitive and matches partial strings.

        Args:
            search_term: The string to search for. Cannot be empty.

        Returns:
            A list of task dictionaries that match the search term.

        Raises:
            ValueError: If search_term is empty or contains only whitespace.
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower().strip()
        # A list comprehension offers a concise and readable way to filter tasks.
        return [
            task for task in self._tasks.values()
            if lower_term in task['name'].lower() or lower_term in task['description'].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The integer ID of the task to mark as finished.

        Returns:
            True if the task's status was successfully updated.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

        self._tasks[task_id]['is_finished'] = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks currently in the manager.

        Returns:
            A list of all task dictionaries. The list is a copy, so modifications
            to it will not affect the internal task list.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager and resets the ID counter.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Console User Interface ---

def print_task(task: Dict[str, Any]) -> None:
    """Helper function to print a single task in a formatted way."""
    status = "Finished" if task['is_finished'] else "Pending"
    print("-" * 20)
    print(f"  ID: {task['id']} | Status: {status}")
    print(f"  Name: {task['name']}")
    print(f"  Description: {task['description']}")
    print("-" * 20)

def main() -> None:
    """A simple console-based UI to demonstrate TaskManager functionality."""
    manager = TaskManager()
    print("--- Console Todo List App ---")
    print("Commands: add, remove, search, finish, list, clear, help, exit")

    # Pre-populate with some data for demonstration
    try:
        manager.add("Learn Python", "Study advanced Python concepts like OOP and decorators.")
        manager.add("Write a report", "Complete the quarterly performance report.")
        manager.add("Go to the gym", "Workout session focusing on cardio.")
    except (ValueError, TypeError) as e:
        print(f"Error during app initialization: {e}", file=sys.stderr)

    while True:
        try:
            command_line = input("> ").strip().lower()
            if not command_line:
                continue

            command = command_line.split()[0]

            if command == "add":
                name = input("  Enter task name: ")
                desc = input("  Enter task description: ")
                task_id = manager.add(name, desc)
                print(f"\nSuccess: Task added with ID {task_id}.")
            elif command == "remove":
                task_id_str = input("  Enter task ID to remove: ")
                task_id = int(task_id_str)
                if manager.remove(task_id):
                    print(f"\nSuccess: Task {task_id} removed.")
            elif command == "search":
                term = input("  Enter search term: ")
                results = manager.search(term)
                if not results:
                    print("\nNo tasks found matching your search.")
                else:
                    print(f"\nFound {len(results)} task(s):")
                    for task in results:
                        print_task(task)
            elif command == "finish":
                task_id_str = input("  Enter task ID to finish: ")
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"\nSuccess: Task {task_id} marked as finished.")
            elif command == "list":
                all_tasks = manager.get_all()
                if not all_tasks:
                    print("\nNo tasks in the list.")
                else:
                    print("\nAll tasks:")
                    for task in all_tasks:
                        print_task(task)
            elif command == "clear":
                confirm = input("  Are you sure you want to delete all tasks? (yes/no): ").lower()
                if confirm == 'yes':
                    if manager.clear_all():
                        print("\nSuccess: All tasks have been cleared.")
                else:
                    print("\nOperation cancelled.")
            elif command == "help":
                print("\nAvailable commands:")
                print("  add     - Add a new task.")
                print("  remove  - Remove a task by its ID.")
                print("  search  - Search for tasks by a keyword.")
                print("  finish  - Mark a task as finished by its ID.")
                print("  list    - Show all tasks.")
                print("  clear   - Remove all tasks.")
                print("  exit    - Exit the application.")
            elif command == "exit":
                print("Exiting application. Goodbye!")
                break
            else:
                print(f"Unknown command: '{command}'. Type 'help' for a list of commands.")

        except (ValueError, TypeError) as e:
            print(f"Error: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()
