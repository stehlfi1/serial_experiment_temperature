
import threading
from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception raised when task validation fails."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception raised when a task is not found."""
    pass


class Task:
    """
    Data class representing a todo task.

    Attributes:
        id (int): Unique identifier for the task.
        name (str): Name of the task.
        description (str): Description of the task.
        is_finished (bool): Status flag indicating if the task is completed.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """
        Converts the Task object into a dictionary.
        :return: dict with task properties.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Manages a collection of todo tasks with add, remove, search, finish, get_all, and clear_all operations.

    Operations are thread-safe.
    """

    def __init__(self):
        """
        Initializes TaskManager with an empty task list and task ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.Lock()

    def _validate_task_name(self, task_name: str):
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name must be a non-empty string.")

    def _validate_task_description(self, description: str):
        if not isinstance(description, str) or not description.strip():
            raise TaskValidationError("Task description must be a non-empty string.")

    def _validate_task_id(self, task_id: int):
        if not isinstance(task_id, int) or task_id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.

        :param task_name: The name/title of the task.
        :param task_description: The description of the task.
        :return: The unique ID of the new task.
        :raises TaskValidationError: for invalid input.
        """
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        with self._lock:
            task_id = self._next_id
            self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
            self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes the task with the given ID.

        :param task_id: The unique ID of the task to remove.
        :return: True if successfully removed, False if task does not exist.
        :raises TaskValidationError: for invalid ID.
        """
        self._validate_task_id(task_id)
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by term in name or description (case-insensitive).

        :param task_term: The search term.
        :return: List of matching task dicts.
        :raises TaskValidationError: for invalid search term.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term must be a non-empty string.")
        term = task_term.strip().lower()
        with self._lock:
            results = [
                task.to_dict()
                for task in self._tasks.values()
                if term in task.name.lower() or term in task.description.lower()
            ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        :param task_id: The unique ID of the task.
        :return: True if operation succeeded, False if not.
        :raises TaskValidationError: for invalid ID.
        """
        self._validate_task_id(task_id)
        with self._lock:
            task = self._tasks.get(task_id)
            if task is not None:
                task.is_finished = True
                return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks with their details.

        :return: List of task dicts.
        """
        with self._lock:
            return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        :return: True if successfully cleared (always succeeds).
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1
        return True


# Example of how to use TaskManager in a testable way
if __name__ == "__main__":
    # Initialize TaskManager
    manager = TaskManager()
    # Add tasks
    try:
        task_id1 = manager.add("Buy groceries", "Milk, eggs, bread")
        task_id2 = manager.add("Read book", "Read at least 30 pages today.")
        print(f"Added tasks with IDs: {task_id1}, {task_id2}\n")
    except TaskValidationError as ve:
        print(f"Validation error: {ve}")

    # Get all tasks
    print("All Tasks:", manager.get_all())

    # Finish a task
    if manager.finish(task_id1):
        print(f"Task {task_id1} marked as finished.")
    
    # Search tasks
    search_result = manager.search("read")
    print("Search 'read':", search_result)

    # Remove a task
    if manager.remove(task_id2):
        print(f"Task {task_id2} removed.")

    # Get all tasks after removal
    print("All Tasks after removal:", manager.get_all())

    # Clear all tasks
    if manager.clear_all():
        print("All tasks cleared.")

    # Display tasks after clearing
    print("All Tasks after clear:", manager.get_all())
