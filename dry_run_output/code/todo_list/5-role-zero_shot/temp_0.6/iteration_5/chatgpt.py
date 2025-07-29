
from typing import List, Dict, Optional

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
        Returns the task as a dictionary.
        """
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages a list of tasks with add, remove, search, finish, get_all, and clear_all operations.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty task list and an internal ID counter.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task and returns its unique ID.

        :param task_name: The name of the task (non-empty string).
        :param task_description: The description of the task (non-empty string).
        :return: The unique ID of the added task.
        :raises ValueError: If inputs are invalid.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._next_id += 1
        task = Task(task_id, task_name.strip(), task_description.strip())
        self._tasks[task_id] = task
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        :param task_id: The ID of the task to remove.
        :return: True if removal was successful, False otherwise.
        :raises ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks whose name or description contains the search term (case-insensitive).

        :param task_term: The search term (non-empty string).
        :return: List of matching task dictionaries.
        :raises ValueError: If search term is invalid.
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
        Marks a task as completed.

        :param task_id: The ID of the task to finish.
        :return: True if the task was marked as finished, False otherwise.
        :raises ValueError: If task_id is invalid.
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

        :return: List of all tasks as dictionaries.
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


if __name__ == "__main__":
    # Example usage and demonstration of TaskManager functionality.
    tm = TaskManager()

    # Add tasks
    task1_id = tm.add("Buy groceries", "Milk, Bread, Eggs")
    task2_id = tm.add("Read book", "Read 30 pages of a novel")

    # Get all tasks
    print("All tasks:", tm.get_all())

    # Finish a task
    tm.finish(task1_id)
    print("After finishing task 1:", tm.get_all())

    # Search for tasks
    print("Search for 'read':", tm.search("read"))

    # Remove a task
    tm.remove(task2_id)
    print("After removing task 2:", tm.get_all())

    # Clear all tasks
    tm.clear_all()
    print("After clearing all:", tm.get_all())
