
"""
A console-based Todo List application adhering to high-quality code standards.

This module contains the core logic for managing tasks and a simple command-line
interface (CLI) for user interaction.
"""

from __future__ import annotations
import sys
from typing import TypedDict, List

# --- Data Structures and Custom Exceptions ---

class TaskDict(TypedDict):
    """A type definition for the dictionary representation of a task."""
    id: int
    task_name: str
    task_description: str
    is_finished: bool

class TaskNotFoundError(Exception):
    """Custom exception raised when a task ID is not found."""
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Error: Task with ID '{task_id}' not found.")


# --- Core Business Logic ---

class TaskManager:
    """
    Manages all operations related to tasks in a todo list.

    This class encapsulates the data storage and business logic, ensuring that
    the core functionality is decoupled from the user interface. It uses a
    dictionary for efficient task lookups, insertions, and deletions.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an in-memory data store."""
        self._tasks: dict[int, dict] = {}
        self._next_id: int = 1

    def _generate_id(self) -> int:
        """Generates a unique, sequential ID for a new task."""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name or task_description are empty or just whitespace.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            # Allow empty description, but not other types
            raise TypeError("Task description must be a string.")

        task_id = self._generate_id()
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
        }
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            ValueError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[TaskDict]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.

        Raises:
            ValueError: If the search_term is empty or just whitespace.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        lower_term = search_term.lower().strip()
        
        return [
            task for task in self._tasks.values()
            if lower_term in task["task_name"].lower() or \
               lower_term in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            ValueError: If the task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[TaskDict]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks, where each task is a dictionary.
            The list is sorted by task ID.
        """
        # Return a list of copies to prevent external modification of internal state
        return sorted(list(self._tasks.values()), key=lambda t: t['id'])

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful deletion of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


# --- Console User Interface (Presentation Layer) ---

def print_task(task: TaskDict) -> None:
    """Formats and prints a single task to the console."""
    status = "✅ Finished" if task["is_finished"] else "◻️ Pending"
    print(
        f"  ID: {task['id']} | Status: {status}\n"
        f"  Name: {task['task_name']}\n"
        f"  Description: {task['task_description']}\n"
        f"  ----------------------------------------"
    )

def print_menu() -> None:
    """Prints the main menu of the application."""
    print("\n===== Todo List Menu =====")
    print("1. Add Task")
    print("2. Remove Task")
    print("3. Mark Task as Finished")
    print("4. Search Tasks")
    print("5. List All Tasks")
    print("6. Clear All Tasks")
    print("7. Exit")
    print("==========================")

def main() -> None:
    """The main entry point and run loop for the console application."""
    task_manager = TaskManager()
    print("Welcome to the Console Todo List App!")

    while True:
        print_menu()
        choice = input("Enter your choice (1-7): ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = task_manager.add(name, desc)
                print(f"\n✅ Success: Task '{name}' added with ID {task_id}.")

            elif choice == '2':
                task_id_str = input("Enter task ID to remove: ")
                task_manager.remove(int(task_id_str))
                print(f"\n✅ Success: Task {task_id_str} removed.")

            elif choice == '3':
                task_id_str = input("Enter task ID to mark as finished: ")
                task_manager.finish(int(task_id_str))
                print(f"\n✅ Success: Task {task_id_str} marked as finished.")

            elif choice == '4':
                term = input("Enter search term: ")
                results = task_manager.search(term)
                print(f"\n🔎 Found {len(results)} matching task(s):")
                if not results:
                    print("  No tasks found matching your search.")
                else:
                    for task in results:
                        print_task(task)

            elif choice == '5':
                all_tasks = task_manager.get_all()
                print(f"\n📋 All Tasks ({len(all_tasks)}):")
                if not all_tasks:
                    print("  Your todo list is empty.")
                else:
                    for task in all_tasks:
                        print_task(task)

            elif choice == '6':
                confirm = input("Are you sure you want to delete ALL tasks? (y/n): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("\n✅ Success: All tasks have been cleared.")
                else:
                    print("\nℹ️ Info: Operation cancelled.")

            elif choice == '7':
                print("Goodbye!")
                sys.exit(0)

            else:
                print("\n❌ Error: Invalid choice. Please enter a number between 1 and 7.")

        except (ValueError, TypeError, TaskNotFoundError) as e:
            print(f"\n❌ Error: {e}")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
