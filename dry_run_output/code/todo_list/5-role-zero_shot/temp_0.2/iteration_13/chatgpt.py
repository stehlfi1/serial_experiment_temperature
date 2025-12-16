
import sys
from typing import Dict, List

class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass

class TaskNotFoundError(KeyError):
    """Custom exception for non-existent task IDs."""
    pass

class TaskManager:
    """
    A console-based Todo List manager, following ISO/IEC 25010 quality model principles.

    Methods:
        add(task_name: str, task_description: str) -> int
        remove(task_id: int) -> bool
        search(task_term: str) -> List[dict]
        finish(task_id: int) -> bool
        get_all() -> List[dict]
        clear_all() -> bool
    """
    def __init__(self):
        """Initialize the TaskManager with an empty in-memory task store."""
        self._tasks: Dict[int, dict] = {}
        self._next_id: int = 1

    def _validate_str(self, value: str, var_name: str):
        if not isinstance(value, str) or not value.strip():
            raise TaskValidationError(f"{var_name} must be a non-empty string.")

    def _validate_task_id(self, task_id: int):
        if not isinstance(task_id, int) or task_id < 0:
            raise TaskValidationError("Task ID must be a non-negative integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} does not exist.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task.

        Args:
            task_name (str): The name of the task (must not be empty).
            task_description (str): The task description (must not be empty).

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            TaskValidationError: If the name or description is invalid.
        """
        self._validate_str(task_name, "Task name")
        self._validate_str(task_description, "Task description")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": task_name.strip(),
            "task_description": task_description.strip(),
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if successfully removed, False otherwise.

        Raises:
            TaskValidationError: If the task_id is invalid.
            TaskNotFoundError: If task does not exist.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[dict]:
        """
        Search for tasks by name or description.

        Args:
            task_term (str): Case-insensitive term to search for.

        Returns:
            List[dict]: List of tasks matching the search criteria.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term must be a non-empty string.")

        term = task_term.lower()
        results = [
            task.copy()
            for task in self._tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished.

        Args:
            task_id (int): The unique ID of the task to mark as finished.

        Returns:
            bool: True if task exists and marked, False otherwise.

        Raises:
            TaskValidationError: If input is invalid.
            TaskNotFoundError: If task does not exist.
        """
        self._validate_task_id(task_id)
        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[dict]:
        """
        Retrieve all tasks.

        Returns:
            List[dict]: A list of all tasks with their details.
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if cleared successfully, False otherwise.
        """
        self._tasks.clear()
        return True

# ----------------------------------------------------------
# Optional: Example/test code for demonstration (Testability)
# ----------------------------------------------------------
def main():
    tm = TaskManager()
    try:
        # Add tasks
        id1 = tm.add("Buy groceries", "Milk, Bread, Eggs")
        id2 = tm.add("Read Book", "Finish reading ISO/IEC 25010 documentation")
        print("All tasks after addition:")
        print(tm.get_all())

        # Search tasks
        print("Search 'read':", tm.search("read"))
        print("Search '25010':", tm.search("25010"))

        # Finish task
        tm.finish(id2)
        print("All tasks after finishing one:")
        print(tm.get_all())

        # Remove task
        tm.remove(id1)
        print("All tasks after removal:")
        print(tm.get_all())

        # Clear all
        tm.clear_all()
        print("All tasks after clear_all:", tm.get_all())

        # Test error handling
        try:
            tm.remove(99)
        except TaskNotFoundError as e:
            print("Handled error:", e)

        try:
            tm.add("", "")
        except TaskValidationError as e:
            print("Handled error:", e)

    except Exception as e:
        print("Unexpected error:", e, file=sys.stderr)

if __name__ == "__main__":
    main()
