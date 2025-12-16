
from typing import List, Dict


class TaskNotFoundError(Exception):
    """Custom exception for non-existent task operations."""
    pass


class InvalidTaskInputError(Exception):
    """Custom exception for invalid task data."""
    pass


class TaskManager:
    """
    Console-based To-Do List Application Manager.
    Implements CRUD and search operations for task management.

    Adheres to ISO/IEC 25010 standards: modularity, correctness, safety,
    maintainability, testability, and performance.
    """

    def __init__(self):
        """Initialize an empty task store and ID counter."""
        self._tasks: Dict[int, Dict] = {}  # id: task dict
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task with the provided name and description.

        Args:
            task_name (str): Name of the task (must be non-empty).
            task_description (str): Description of the task (must be non-empty).

        Returns:
            int: Unique identifier for the added task.

        Raises:
            InvalidTaskInputError: If either argument is empty.
        """
        if not task_name.strip():
            raise InvalidTaskInputError("Task name cannot be empty.")
        if not task_description.strip():
            raise InvalidTaskInputError("Task description cannot be empty.")

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
        Remove a task by its unique identifier.

        Args:
            task_id (int): Task unique identifier (must be positive).

        Returns:
            bool: True if the task existed and was removed, False otherwise.

        Raises:
            InvalidTaskInputError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskInputError("Task ID must be a positive integer.")

        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Search tasks by a term in the name or description (case-insensitive).

        Args:
            task_term (str): Search string.

        Returns:
            List[Dict]: List of tasks (id, task_name, task_description, is_finished) that match the search.

        Raises:
            InvalidTaskInputError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise InvalidTaskInputError("Search term cannot be empty.")

        term = task_term.strip().lower()
        results = [
            task.copy()
            for task in self._tasks.values()
            if term in task["task_name"].lower()
            or term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished by its unique identifier.

        Args:
            task_id (int): Task unique identifier.

        Returns:
            bool: True if the task was marked as finished, False if it was already finished.

        Raises:
            InvalidTaskInputError: If task_id is invalid.
            TaskNotFoundError: If the task does not exist.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskInputError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        if task["is_finished"]:
            return False
        task["is_finished"] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.

        Returns:
            List[Dict]: List of all tasks (id, task_name, task_description, is_finished).
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Remove all tasks from the task manager.

        Returns:
            bool: True if any task was deleted, False if already empty.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


if __name__ == "__main__":
    manager = TaskManager()
    # Test adding a task
    try:
        task_id = manager.add("Code Review", "Review the latest PR on GitHub")
        print(f"Added task with ID: {task_id}")
    except InvalidTaskInputError as e:
        print(f"Error: {e}")

    # Test get all
    print(manager.get_all())

    # Test search
    print(manager.search("review"))

    # Test finish
    try:
        manager.finish(task_id)
    except (InvalidTaskInputError, TaskNotFoundError) as e:
        print(f"Error: {e}")

    # Test remove
    manager.remove(task_id)
    print(manager.get_all())

    # Test clear all
    manager.add("Task 1", "Description 1")
    manager.add("Task 2", "Description 2")
    manager.clear_all()
    print(manager.get_all())
