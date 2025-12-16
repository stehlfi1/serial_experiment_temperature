
from typing import List, Dict

class TaskValidationError(ValueError):
    """Custom exception for invalid task operations."""
    pass

class TaskNotFoundError(KeyError):
    """Custom exception for non-existent task IDs."""
    pass

class Task:
    """
    Represents a Todo Task.

    Attributes:
        id (int): Unique identifier for the task.
        name (str): Task name.
        description (str): Task description.
        is_finished (bool): Completion status.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> dict:
        """Returns the task details as a dictionary."""
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }

class TaskManager:
    """
    Manages a collection of Todo tasks with operations to add, remove,
    search, finish, retrieve, and clear tasks.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}  # Stores tasks keyed by their ID
        self._next_id: int = 1             # Autoincrementing ID

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.
        Args:
            task_name (str): Name of the task (must be non-empty).
            task_description (str): Description of the task (must be non-empty).
        Returns:
            int: ID of the newly created task.
        Raises:
            ValueError: If task_name or task_description is empty.
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
            bool: True if the task was removed, False otherwise.
        Raises:
            ValueError: If the id is invalid (not a positive integer).
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[dict]:
        """
        Searches tasks by name or description (case-insensitive).
        Args:
            task_term (str): Search term.
        Returns:
            list[dict]: List of matching task dicts.
        Raises:
            ValueError: If search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")
        results = []
        lower_term = task_term.lower()
        for task in self._tasks.values():
            if lower_term in task.name.lower() or lower_term in task.description.lower():
                results.append(task.to_dict())
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished by its ID.
        Args:
            task_id (int): ID of the task to finish.
        Returns:
            bool: True if task was marked finished, False if not found or already finished.
        Raises:
            ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if not task or task.is_finished:
            return False
        task.is_finished = True
        return True

    def get_all(self) -> List[dict]:
        """
        Retrieves all tasks with their details.
        Returns:
            list[dict]: List of all tasks in (id, task_name, task_description, is_finished) format.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.
        Returns:
            bool: True if any tasks were deleted, False if already empty.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True

# Example usage (commented for testability):

# if __name__ == "__main__":
#     tm = TaskManager()
#     tid1 = tm.add("Shop", "Buy milk and bread")
#     tid2 = tm.add("Read", "Read ISO/IEC 25010 documentation")
#     print(tm.get_all())
#     print(tm.search("shop"))
#     tm.finish(tid1)
#     print(tm.get_all())
#     tm.remove(tid2)
#     print(tm.get_all())
#     tm.clear_all()
#     print(tm.get_all())
