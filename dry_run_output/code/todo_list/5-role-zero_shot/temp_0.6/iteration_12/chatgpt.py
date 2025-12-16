
"""
Console-based Todo List App

This module implements a console-based todo list application with high
code quality adhering to ISO/IEC 25010 quality model principles.
It provides a maintainable, testable, and efficient TaskManager class
for managing todo tasks.

Author: AI Assistant
"""

from typing import List, Dict, Optional


class Task:
    """
    Represents a single Todo task.

    Attributes:
        id (int): Unique identifier.
        name (str): Name of the task.
        description (str): Description/details of the task.
        is_finished (bool): Completion status.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation for output consistency.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Manages Todo tasks, providing CRUD operations and search functionality.

    Adheres to ISO/IEC 25010 for correctness, performance, reliability,
    and maintainability.

    Methods:
        add(task_name, task_description) -> int
        remove(task_id) -> bool
        search(task_term) -> list[dict]
        finish(task_id) -> bool
        get_all() -> list[dict]
        clear_all() -> bool
    """

    def __init__(self):
        # Tasks stored as {task_id: Task} for O(1) access by ID
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the todo list.

        Args:
            task_name (str): Name/title of the task. Must not be empty.
            task_description (str): Description/details. Must not be empty.

        Returns:
            int: Unique identifier of the created task.

        Raises:
            ValueError: If input strings are empty.
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

        Args:
            task_id (int): ID of the task to remove.

        Returns:
            bool: True if removed, False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        return bool(self._tasks.pop(task_id, None))

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks containing a term in the name or description.

        Args:
            task_term (str): Search keyword.

        Returns:
            list[dict]: List of matching tasks, each as a dict.

        Raises:
            ValueError: If search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")
        term = task_term.strip().lower()
        results = []
        for task in self._tasks.values():
            if term in task.name.lower() or term in task.description.lower():
                results.append(task.to_dict())
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished/completed.

        Args:
            task_id (int): ID of the task to mark as finished.

        Returns:
            bool: True if marked, False if not found or already finished.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task and not task.is_finished:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Gets all tasks.

        Returns:
            list[dict]: List of all tasks as dicts.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if tasks existed and deleted, False if already empty.
        """
        had_tasks = bool(self._tasks)
        self._tasks.clear()
        return had_tasks


# Sample test code for demonstration (can be placed under __main__ for actual use)
def _demo():
    """
    Minimal sample console test run for TaskManager.
    """
    tm = TaskManager()
    try:
        # Add tasks
        t1 = tm.add("Buy groceries", "Milk, Bread, Eggs")
        t2 = tm.add("Read book", "Finish reading DIY book")
        t3 = tm.add("Exercise", "Run 5km in the park")

        # Display all tasks
        print("All tasks:")
        for task in tm.get_all():
            print(task)

        # Search for tasks
        print("\nSearch for 'book':")
        print(tm.search("book"))

        # Finish a task
        print("\nFinish task:", t2)
        print(tm.finish(t2))
        print("Updated task:", [t for t in tm.get_all() if t["id"] == t2][0])

        # Remove a task
        print("\nRemove task:", t1)
        print(tm.remove(t1))
        print("All tasks after removal:")
        for task in tm.get_all():
            print(task)

        # Clear all tasks
        print("\nClear all tasks:")
        print(tm.clear_all())
        print("All tasks after clearing:", tm.get_all())

    except ValueError as e:
        print("Error:", e)


if __name__ == "__main__":
    _demo()
