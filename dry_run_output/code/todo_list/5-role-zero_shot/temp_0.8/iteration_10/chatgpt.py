
"""
Console-based Todo List Application

This application follows ISO/IEC 25010 quality standards by emphasizing
correctness, reliability, maintainability, usability, and efficiency.

Author: Senior Software Developer
"""

from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception for invalid task input."""
    pass


class TaskNotFoundError(LookupError):
    """Custom exception for non-existent tasks."""
    pass


class Task:
    """
    Represents a single todo task.
    
    Attributes:
        id (int): Unique ID for the task.
        name (str): Name/title of the task.
        description (str): Description/details of the task.
        is_finished (bool): Completion status of the task.
    """

    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """
        Serializes the task to a dictionary.

        Returns:
            dict: Dictionary with task details.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Manages todo tasks in-memory.

    Interface methods:
        - add(task_name: str, task_description: str) -> int
        - remove(task_id: int) -> bool
        - search(task_term: str) -> list[dict]
        - finish(task_id: int) -> bool
        - get_all() -> list[dict]
        - clear_all() -> bool
    """

    def __init__(self):
        # Mapping from task_id to Task object for efficient operations
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_name(self, name: str):
        if not isinstance(name, str) or not name.strip():
            raise TaskValidationError("Task name must be a non-empty string.")

    def _validate_task_description(self, description: str):
        if not isinstance(description, str) or not description.strip():
            raise TaskValidationError("Task description must be a non-empty string.")

    def _validate_task_id(self, task_id: int):
        if not isinstance(task_id, int) or task_id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")

    def _get_task(self, task_id: int) -> Task:
        self._validate_task_id(task_id)
        task = self._tasks.get(task_id)
        if not task:
            raise TaskNotFoundError(f"Task with ID {task_id} not found.")
        return task

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.

        Args:
            task_name (str): Name of the task.
            task_description (str): Description of the task.

        Returns:
            int: Unique ID assigned to the new task.

        Raises:
            TaskValidationError: If task_name or task_description is invalid.
        """
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)

        task_id = self._next_id
        self._next_id += 1

        task = Task(task_id, task_name.strip(), task_description.strip())
        self._tasks[task_id] = task
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed, False otherwise.

        Raises:
            TaskValidationError: If task_id is invalid.
        """
        try:
            self._validate_task_id(task_id)
        except TaskValidationError:
            return False

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by name or description (case-insensitive, substring match).

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: List of matching task details, empty if none match.

        Raises:
            TaskValidationError: If search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        matches = [
            task.to_dict()
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
        ]
        return matches

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The ID of the task to finish.

        Returns:
            bool: True if the task was marked as finished, False if not found.

        Raises:
            TaskValidationError: If task_id is invalid.
        """
        try:
            task = self._get_task(task_id)
        except (TaskValidationError, TaskNotFoundError):
            return False

        if task.is_finished:
            return True  # Already finished

        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: List of all task details, sorted by ID.
        """
        return [task.to_dict() for task in sorted(self._tasks.values(), key=lambda t: t.id)]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if tasks were cleared (even if already empty).
        """
        self._tasks.clear()
        return True


# Example usage and simple test cases (for self-testability)
if __name__ == "__main__":
    tm = TaskManager()
    # Add tasks
    id1 = tm.add("Buy groceries", "Buy milk, eggs, and bread.")
    id2 = tm.add("Read Book", "Finish reading the Python book.")
    # Search tasks
    print("Search 'buy':", tm.search("buy"))
    # Mark as finished
    print("Finish id1:", tm.finish(id1))
    # Remove task
    print("Remove id2:", tm.remove(id2))
    # Get all tasks
    print("All tasks:", tm.get_all())
    # Clear all tasks
    print("Clear all:", tm.clear_all())
    print("All tasks after clear:", tm.get_all())
