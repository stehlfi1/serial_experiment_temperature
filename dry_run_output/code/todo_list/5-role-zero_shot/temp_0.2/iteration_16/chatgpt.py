
"""
Console-based TODO List Application

Author: AI Assistant
Standard: ISO/IEC 25010:2011 (Quality Model Conformance)

This application defines a TaskManager class for managing a todo list with support for
adding, removing, searching, finishing, listing, and clearing tasks. The code is robust,
modular, and adheres to Python best practices for maintainability and testability.
"""

from typing import List, Dict


class TaskNotFoundError(ValueError):
    """Raised when a specified task ID does not exist in the task list."""


class InvalidTaskInputError(ValueError):
    """Raised when an invalid input is provided to a task operation."""


class TaskManager:
    """
    TaskManager provides operations to manage a set of tasks in-memory.

    Tasks are stored as a dictionary keyed by integer IDs.
    Each task is represented as a dictionary with the following keys:
        - id: int
        - task_name: str
        - task_description: str
        - is_finished: bool
    """

    def __init__(self) -> None:
        """Initialize the task manager with empty task storage."""
        self._tasks: Dict[int, Dict] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task.

        Args:
            task_name (str): Name of the task (non-empty).
            task_description (str): Description of the task (non-empty).

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            InvalidTaskInputError: If task_name or task_description are invalid.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise InvalidTaskInputError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
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
        Remove a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was removed, False if it didn't exist.

        Raises:
            InvalidTaskInputError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskInputError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description (case-insensitive substring match).

        Args:
            task_term (str): The term to search for (non-empty).

        Returns:
            list[dict]: List of matching tasks (as dictionaries).

        Raises:
            InvalidTaskInputError: If the search term is invalid.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise InvalidTaskInputError("Search term cannot be empty.")

        term_lower = task_term.lower()
        results = [
            task.copy()
            for task in self._tasks.values()
            if term_lower in task['task_name'].lower() or term_lower in task['task_description'].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if task is successfully marked as finished, False if it doesn't exist.

        Raises:
            InvalidTaskInputError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskInputError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if not task:
            return False
        if not task['is_finished']:
            task['is_finished'] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Get a list of all tasks.

        Returns:
            list[dict]: All tasks, each with (id, task_name, task_description, is_finished).
        """
        # Return deep copies so callers cannot mutate our internal structures
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Remove all tasks from the list.

        Returns:
            bool: True if any tasks existed and were cleared, False if already empty.
        """
        has_tasks = bool(self._tasks)
        self._tasks.clear()
        return has_tasks


# Example usage and simple test cases
if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    task1_id = tm.add("Write Unit Tests", "Write unit tests for the todo list app.")
    task2_id = tm.add("Review Code", "Perform code review against ISO/IEC 25010.")

    # List all tasks
    print("All tasks:", tm.get_all())

    # Search tasks
    print("Search 'unit':", tm.search("unit"))

    # Mark as finished
    print("Finish task1:", tm.finish(task1_id))
    print("All tasks after finishing task1:", tm.get_all())

    # Remove a task
    print("Remove task2:", tm.remove(task2_id))
    print("All tasks after removing task2:", tm.get_all())

    # Clear all tasks
    print("Clear all:", tm.clear_all())
    print("All tasks after clear:", tm.get_all())

    # Try invalid additions (should raise exceptions)
    try:
        tm.add("", "")
    except InvalidTaskInputError as e:
        print("Add error:", e)

    # Try removing non-existent task (returns False)
    print("Remove non-existent task:", tm.remove(999))
