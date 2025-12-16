
import threading

class TaskManager:
    """
    TaskManager provides an in-memory, thread-safe todo list management system,
    supporting adding, removing, searching, finishing, retrieving, and clearing tasks.

    Each task has a unique integer ID, name, description, and completion status.
    """

    def __init__(self):
        """Initialize the TaskManager with an empty task store and id counter."""
        self._tasks = {}  # task_id: task_dict
        self._id_counter = 1
        self._lock = threading.Lock()  # Ensures thread-safety if needed

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task.
        :param task_name: Name of the task (non-empty).
        :param task_description: Description of the task (non-empty).
        :return: Unique integer ID of the added task.
        :raises ValueError: If name or description is empty.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        with self._lock:
            task_id = self._id_counter
            self._id_counter += 1
            self._tasks[task_id] = {
                "id": task_id,
                "task_name": task_name.strip(),
                "task_description": task_description.strip(),
                "is_finished": False
            }
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.
        :param task_id: The integer ID of the task to remove.
        :return: True if removed, False if task ID not found.
        :raises ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            else:
                return False

    def search(self, task_term: str) -> list[dict]:
        """
        Search for tasks by term in name or description (case-insensitive).
        :param task_term: Term to search for (non-empty string).
        :return: List of matching task dicts.
        :raises ValueError: If task_term is empty.
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty.")
        term = task_term.lower()
        matches = []
        with self._lock:
            for task in self._tasks.values():
                if (term in task["task_name"].lower()) or (term in task["task_description"].lower()):
                    matches.append(task.copy())
        return matches

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished by ID.
        :param task_id: The integer ID of the task.
        :return: True if task was marked finished, False if ID not found.
        :raises ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        with self._lock:
            task = self._tasks.get(task_id)
            if task:
                if not task["is_finished"]:
                    task["is_finished"] = True
                return True
            else:
                return False

    def get_all(self) -> list[dict]:
        """
        Retrieve all tasks.
        :return: List of all task dicts (id, task_name, task_description, is_finished).
        """
        with self._lock:
            # Return a copy to prevent external mutation
            return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Remove all tasks.
        :return: True if tasks existed and were cleared, False if no tasks existed.
        """
        with self._lock:
            if self._tasks:
                self._tasks.clear()
                return True
            return False

# Example usage/testability (remove or comment out before production deployment)
if __name__ == "__main__":
    manager = TaskManager()

    # Add tasks
    tid1 = manager.add("Buy groceries", "Milk, Bread, Eggs")
    tid2 = manager.add("Write report", "Finish ISO/IEC 25010 documentation")
    print("Tasks after adding:", manager.get_all())

    # Search
    print("Search for 'buy':", manager.search("buy"))

    # Finish a task
    manager.finish(tid1)
    print("Tasks after finishing one:", manager.get_all())

    # Remove a task
    manager.remove(tid2)
    print("Tasks after removing one:", manager.get_all())

    # Clear all
    manager.clear_all()
    print("Tasks after clearing:", manager.get_all())
