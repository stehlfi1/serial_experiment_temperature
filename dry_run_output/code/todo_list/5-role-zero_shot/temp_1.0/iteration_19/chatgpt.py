
"""
Console-based Todo List Application

This module defines a TaskManager class for managing tasks using OOP principles.
It provides functionalities to add, remove, search, finish, retrieve, and clear tasks.
The implementation adheres to ISO/IEC 25010 quality attributes (e.g. maintainability, reliability, usability, efficiency).

Author: Example Senior Dev
"""

from typing import List, Dict


class Task:
    """
    Data class representing a single Task.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id: int = task_id
        self.name: str = name
        self.description: str = description
        self.is_finished: bool = False

    def to_dict(self) -> Dict:
        """
        Converts the task instance to a dictionary.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished,
        }


class TaskManager:
    """
    Manages a collection of tasks.
    Provides add, remove, search, finish, get_all, and clear_all methods.
    In-memory storage using dictionaries for efficient lookup and O(1) operations.
    """
    def __init__(self):
        # Internal dict: task_id -> Task
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1  # Auto-incremented task ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task and returns its unique ID.
        Raises ValueError for invalid input.

        :param task_name: Name of the task (non-empty string)
        :param task_description: Description (non-empty string)
        :return: Unique task ID
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.
        Returns True if successful, False otherwise.

        :param task_id: Positive integer task ID
        :return: Bool, success status
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def finish(self, task_id: int) -> bool:
        """
        Marks the specified task as finished.
        Returns True if successful, False if task not found.

        :param task_id: Task ID
        :return: Bool, success status
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is not None:
            task.is_finished = True
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks containing the term in their name or description (case-insensitive).
        Returns a list of matching tasks (as dicts).

        :param task_term: Search term (non-empty string)
        :return: List of task dicts
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        lower_term = task_term.lower()
        result = [
            task.to_dict()
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]
        return result

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks in the system, sorted by ID.

        :return: List of task dicts
        """
        return [task.to_dict() for task in sorted(self._tasks.values(), key=lambda t: t.id)]

    def clear_all(self) -> bool:
        """
        Removes all tasks.

        :return: Bool, success status (always True)
        """
        self._tasks.clear()
        return True


# Optional: Example usage (for testing):
if __name__ == "__main__":
    tm = TaskManager()
    # Add tasks
    first_id = tm.add("Buy groceries", "Buy milk, eggs, and bread.")
    second_id = tm.add("Read book", "Read 30 pages of the new novel.")
    # Finish a task
    tm.finish(first_id)
    # Search for "read"
    found = tm.search("read")
    print("Search for 'read':", found)
    # Get all tasks
    print("All tasks:", tm.get_all())
    # Remove a task
    tm.remove(second_id)
    print("All tasks after removal:", tm.get_all())
    # Clear all
    tm.clear_all()
    print("All tasks after clearing:", tm.get_all())
