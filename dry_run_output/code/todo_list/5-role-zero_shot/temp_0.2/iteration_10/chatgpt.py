
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
    Manages a collection of todo tasks.
    Provides methods to add, remove, search, finish, retrieve, and clear tasks.
    """

    def __init__(self):
        # Internal storage: {task_id: Task}
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.
        :param task_name: Name of the task (non-empty).
        :param task_description: Description of the task (non-empty).
        :return: Unique ID of the created task.
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
        :return: True if removed, False if not found.
        :raises TaskValidationError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by name or description (case-insensitive).
        :param task_term: Search term (non-empty string).
        :return: List of matching task dictionaries.
        :raises TaskValidationError: If search term is invalid.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term must be a non-empty string.")

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
        :param task_id: ID of the task to mark as finished.
        :return: True if marked, False if not found.
        :raises TaskValidationError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.
        :return: List of all task dictionaries.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.
        :return: True if tasks were cleared, False if already empty.
        """
        if self._tasks:
            self._tasks.clear()
            return True
        return False

# Example usage (for testing and demonstration purposes)
if __name__ == "__main__":
    manager = TaskManager()

    def print_tasks(tasks):
        if not tasks:
            print("No tasks found.")
        else:
            for t in tasks:
                print(f"ID: {t['id']}, Name: {t['task_name']}, Description: {t['task_description']}, Finished: {t['is_finished']}")

    # Add tasks
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Eggs")
        id2 = manager.add("Read Book", "Read 'Clean Code'")
        print(f"Added tasks with IDs: {id1}, {id2}")
    except TaskValidationError as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    print("\nAll tasks:")
    print_tasks(manager.get_all())

    # Search tasks
    print("\nSearch for 'read':")
    print_tasks(manager.search("read"))

    # Finish a task
    print("\nMarking task as finished (ID 2):")
    if manager.finish(2):
        print("Task marked as finished.")
    else:
        print("Task not found.")

    # Remove a task
    print("\nRemoving task (ID 1):")
    if manager.remove(1):
        print("Task removed.")
    else:
        print("Task not found.")

    # Get all tasks after removal
    print("\nAll tasks after removal:")
    print_tasks(manager.get_all())

    # Clear all tasks
    print("\nClearing all tasks:")
    if manager.clear_all():
        print("All tasks cleared.")
    else:
        print("No tasks to clear.")

    # Get all tasks after clearing
    print("\nAll tasks after clearing:")
    print_tasks(manager.get_all())
