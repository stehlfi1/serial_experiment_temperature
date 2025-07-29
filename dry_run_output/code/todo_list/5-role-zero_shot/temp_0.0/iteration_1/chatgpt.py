
import sys
from typing import List, Dict, Optional

class TaskValidationError(ValueError):
    """Custom exception for invalid task operations."""
    pass

class TaskNotFoundError(KeyError):
    """Custom exception for non-existent task IDs."""
    pass

class Task:
    """
    Represents a single todo task.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """
        Returns a dictionary representation of the task.
        """
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }

class TaskManager:
    """
    Manages a collection of todo tasks in memory.
    Provides methods to add, remove, search, finish, retrieve, and clear tasks.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name of the task (non-empty).
            task_description (str): The description of the task (non-empty).

        Returns:
            int: The unique ID of the newly added task.

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
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by name or description (case-insensitive substring match).

        Args:
            task_term (str): The search term.

        Returns:
            list[dict]: List of matching tasks in dictionary format.

        Raises:
            ValueError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = [
            task.to_dict()
            for task in self._tasks.values()
            if term in task.name.lower() or term in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if the task was marked as finished, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if task and not task.is_finished:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: List of all tasks in dictionary format.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if tasks were cleared, False if already empty.
        """
        if self._tasks:
            self._tasks.clear()
            return True
        return False

# Example usage (for testing and demonstration)
if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Eggs")
        id2 = manager.add("Read book", "Read 'Clean Code' by Robert C. Martin")
        print(f"Added tasks with IDs: {id1}, {id2}")
    except ValueError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    print("All tasks:")
    for task in manager.get_all():
        print(task)

    # Search tasks
    print("Search for 'read':")
    for task in manager.search("read"):
        print(task)

    # Finish a task
    if manager.finish(id2):
        print(f"Task {id2} marked as finished.")

    # Remove a task
    if manager.remove(id1):
        print(f"Task {id1} removed.")

    # Get all tasks after removal
    print("All tasks after removal:")
    for task in manager.get_all():
        print(task)

    # Clear all tasks
    if manager.clear_all():
        print("All tasks cleared.")

    # Try to get all tasks after clearing
    print("All tasks after clearing:")
    print(manager.get_all())
