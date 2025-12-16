
"""
Todo List Console Application
============================

A high-quality, maintainable Python application for managing a todo list.

Design adheres to the ISO/IEC 25010 standard with attention to correctness, performance,
modularity, safety, testability, and documentation.

Author: [Your Name]
Date: 2024-06

"""

from typing import List, Dict


class TaskValidationError(ValueError):
    """Custom error for invalid task operations."""
    pass


class TaskNotFoundError(KeyError):
    """Custom error raised when a task is not found."""
    pass


class Task:
    """Represents a single task in the todo list."""

    def __init__(self, task_id: int, name: str, description: str):
        """
        Initialize a new Task.

        :param task_id: Unique integer ID of the task.
        :param name: Name of the task (non-empty).
        :param description: Description of the task (non-empty).
        """
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """Convert Task object to dictionary format."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages tasks in the todo list.

    Implements the required interface:
        - add, remove, search, finish, get_all, clear_all
    """

    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task and returns its unique ID.

        :param task_name: Name of the task (must be a non-empty string).
        :param task_description: Description of the task (must be a non-empty string).
        :return: ID of the newly added task.
        :raises TaskValidationError: If inputs are invalid.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        :param task_id: ID of the task to remove.
        :return: True if removed successfully, False if not found.
        :raises TaskValidationError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")

        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by name or description (case-insensitive substring match).

        :param task_term: Search term as a non-empty string.
        :return: List of tasks (as dicts) matching the search.
        :raises TaskValidationError: If search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term must be a non-empty string.")

        term_lower = task_term.strip().lower()
        results = [
            task.to_dict() for task in self._tasks.values()
            if term_lower in task.name.lower() or term_lower in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.

        :param task_id: ID of the task to mark as finished.
        :return: True if marked as finished, False if not found.
        :raises TaskValidationError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if not task:
            return False
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.

        :return: List of all tasks, each task as a dict.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks.

        :return: True if tasks were cleared, False if already empty.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


# Console demo for manual testability
if __name__ == "__main__":
    def print_menu():
        print("\nTodo List App")
        print("[1] Add task")
        print("[2] Remove task")
        print("[3] Search tasks")
        print("[4] Finish task")
        print("[5] Show all tasks")
        print("[6] Clear all tasks")
        print("[0] Exit")

    task_mgr = TaskManager()

    while True:
        print_menu()
        try:
            choice = input("Choose an option: ").strip()
            if choice == '1':
                name = input("Task name: ")
                desc = input("Task description: ")
                task_id = task_mgr.add(name, desc)
                print(f"Task added with ID {task_id}")
            elif choice == '2':
                try:
                    tid = int(input("Task ID to remove: "))
                except ValueError:
                    print("Invalid ID format.")
                    continue
                if task_mgr.remove(tid):
                    print("Task removed.")
                else:
                    print("No such task.")
            elif choice == '3':
                term = input("Search term: ")
                results = task_mgr.search(term)
                if results:
                    for t in results:
                        print(t)
                else:
                    print("No matching tasks found.")
            elif choice == '4':
                try:
                    tid = int(input("Task ID to finish: "))
                except ValueError:
                    print("Invalid ID format.")
                    continue
                if task_mgr.finish(tid):
                    print("Task marked as finished.")
                else:
                    print("No such task to finish.")
            elif choice == '5':
                all_tasks = task_mgr.get_all()
                if not all_tasks:
                    print("No tasks available.")
                else:
                    for t in all_tasks:
                        print(t)
            elif choice == '6':
                if task_mgr.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")
            elif choice == '0':
                print("Exiting.")
                break
            else:
                print("Invalid choice.")
        except TaskValidationError as e:
            print(f"Input error: {e}")
        except Exception as ex:
            print(f"Unexpected error: {ex}")
