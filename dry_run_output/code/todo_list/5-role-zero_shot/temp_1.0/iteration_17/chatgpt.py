
"""
A console-based Todo List application meeting ISO/IEC 25010 requirements, built using OOP in Python.

Features:
- Add, remove, search, and finish tasks
- Retrieve or clear all tasks
- In-memory and efficient
- Inputs are validated, errors are handled gracefully
- Each task: (id, task_name, task_description, is_finished)

Author: Senior Software Developer
"""

from typing import List, Dict, Optional

class TaskValidationError(Exception):
    """Custom exception for validation errors in TaskManager."""
    pass


class TaskNotFoundError(Exception):
    """Custom exception for task not found errors."""
    pass


class TaskManager:
    """
    Manages tasks with operations to add, remove, search, finish, list, and clear them.
    Each task has a unique ID, name, description, and completion status.
    """

    def __init__(self):
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): Name of the task. Must be non-empty.
            task_description (str): Description of the task. Must be non-empty.

        Returns:
            int: Unique ID of the newly created task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty.")
        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if a task was removed, False if not found.

        Raises:
            ValueError: If the task_id is invalid (non-positive).
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by matching term in name or description (case-insensitive).

        Args:
            task_term (str): Term to search for.

        Returns:
            list[dict]: List of matching tasks.

        Raises:
            ValueError: If search term is empty.
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        term = task_term.strip().lower()
        results = [
            task.copy()
            for task in self._tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): Task ID.

        Returns:
            bool: True if task status changed, False if task was already finished or does not exist.

        Raises:
            ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if not task:
            return False
        if task["is_finished"]:
            return False  # Already finished
        task["is_finished"] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: List of all tasks (id, task_name, task_description, is_finished).
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if tasks were cleared, False if already empty.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True

# Example usage and minimal CLI for demonstration/testability.
if __name__ == "__main__":
    def print_tasks(tasks: List[Dict]) -> None:
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                print(
                    f"ID: {t['id']} | Name: {t['task_name']} | "
                    f"Description: {t['task_description']} | Finished: {t['is_finished']}"
                )

    tm = TaskManager()
    while True:
        print("\nTodo List Menu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Task")
        print("4. Finish Task")
        print("5. Show All Tasks")
        print("6. Clear All Tasks")
        print("0. Exit")
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "1":
                name = input("Task Name: ")
                desc = input("Task Description: ")
                task_id = tm.add(name, desc)
                print(f"Task added with ID {task_id}.")
            elif choice == "2":
                id_ = int(input("Enter Task ID to remove: "))
                if tm.remove(id_):
                    print("Task removed.")
                else:
                    print("Task not found.")
            elif choice == "3":
                term = input("Enter search term: ")
                results = tm.search(term)
                print_tasks(results)
            elif choice == "4":
                id_ = int(input("Enter Task ID to finish: "))
                if tm.finish(id_):
                    print("Task marked as finished.")
                else:
                    print("Task not found or already finished.")
            elif choice == "5":
                print_tasks(tm.get_all())
            elif choice == "6":
                if tm.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")
            elif choice == "0":
                print("Exiting.")
                break
            else:
                print("Invalid option.")
        except Exception as e:
            print(f"Error: {e}")
