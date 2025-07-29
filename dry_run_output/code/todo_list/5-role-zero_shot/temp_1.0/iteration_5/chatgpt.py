
import threading
from typing import List, Dict, Optional

class TaskNotFoundError(Exception):
    """Custom exception for handling non-existent tasks."""
    pass

class InvalidInputError(Exception):
    """Custom exception for handling invalid input data."""
    pass

class Task:
    """
    Represents a Task in the todo list.
    """
    __slots__ = ['id', 'name', 'description', 'is_finished']

    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def as_dict(self) -> Dict:
        """
        Represent task data as a dictionary.
        """
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }

class TaskManager:
    """
    Manages todo list tasks, providing methods to add, remove, search,
    finish, retrieve all, and clear tasks, ensuring high code quality,
    performance, and safety.
    """
    def __init__(self):
        # Protect shared resources in multithreaded environments.
        self._lock = threading.Lock()
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Parameters:
            task_name (str): Name of the task (non-empty)
            task_description (str): Description of the task (non-empty)
            
        Returns:
            int: The unique task ID.
            
        Raises:
            ValueError: If task_name or task_description are empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        with self._lock:
            task_id = self._next_id
            self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
            self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its ID.

        Parameters:
            task_id (int): The task's unique ID (must be positive integer)
        
        Returns:
            bool: True if task was removed, False if not found.

        Raises:
            ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        with self._lock:
            return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Search tasks by task name or description (case-insensitive substring search).

        Parameters:
            task_term (str): The term to search in task names/descriptions.

        Returns:
            List[Dict]: A list of dictionaries of matching tasks.

        Raises:
            ValueError: If task_term is empty or not a string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        with self._lock:
            return [
                task.as_dict()
                for task in self._tasks.values()
                if term in task.name.lower() or term in task.description.lower()
            ]

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished.

        Parameters:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if successful, False if not found.

        Raises:
            ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return False
            task.is_finished = True
            return True

    def get_all(self) -> List[Dict]:
        """
        Get all tasks in the task manager.

        Returns:
            List[Dict]: A list of dictionaries containing all task details.
        """
        with self._lock:
            return [task.as_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.

        Returns:
            bool: True if tasks were cleared (i.e., there were tasks), False otherwise.
        """
        with self._lock:
            had_tasks = bool(self._tasks)
            self._tasks.clear()
            return had_tasks

# ===== Example Usage and Test Cases (Remove or comment for deployment) =====
if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    tid1 = tm.add("Buy milk", "Get 2 liters of milk from the store")
    tid2 = tm.add("Read book", "Finish reading 'Clean Code'")
    assert isinstance(tid1, int) and isinstance(tid2, int)
    print("Added task IDs:", tid1, tid2)

    # List all tasks
    tasks = tm.get_all()
    assert len(tasks) == 2
    print("All tasks:", tasks)

    # Search for a task
    results = tm.search("milk")
    assert len(results) == 1 and results[0]['task_name'] == "Buy milk"
    print("Search results for 'milk':", results)

    # Finish a task
    assert tm.finish(tid1) == True
    finished_task = [t for t in tm.get_all() if t['id'] == tid1][0]
    assert finished_task['is_finished'] == True
    print("Finished task ID:", tid1)

    # Remove a task
    assert tm.remove(tid2) == True
    assert tm.remove(999) == False  # Removing non-existent ID

    # Clear all
    assert tm.clear_all() == True
    assert tm.get_all() == []
    assert tm.clear_all() == False  # Already empty

    # Validation tests
    try:
        tm.add("", "desc")
    except ValueError:
        print("Caught expected ValueError on empty task_name.")

    try:
        tm.finish(-1)
    except ValueError:
        print("Caught expected ValueError on negative task_id.")

    try:
        tm.search("")
    except ValueError:
        print("Caught expected ValueError on empty search term.")

    print("All tests passed.")
