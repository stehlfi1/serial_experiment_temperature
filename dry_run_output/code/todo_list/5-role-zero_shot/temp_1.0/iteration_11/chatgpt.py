
from typing import List, Dict


class TaskManager:
    """
    TaskManager manages a simple in-memory todo list, supporting add, remove, search, finish, get_all, and clear_all
    operations on tasks.

    Each task is represented as a dictionary:
        {
            "id": int,
            "task_name": str,
            "task_description": str,
            "is_finished": bool
        }
    """

    def __init__(self):
        """
        Initialize the task manager with an empty task store and the next available task ID.
        """
        self._tasks: Dict[int, Dict] = {}  # Task storage: { task_id: task_dict }
        self._next_id: int = 1  # Next task ID to assign

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.

        :param task_name: Name/title of the task (must be non-empty).
        :param task_description: Description/details of the task (must be non-empty).
        :return: The unique ID assigned to the added task.
        :raises ValueError: If inputs are invalid.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

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
        Remove a task from the todo list by ID.

        :param task_id: The ID of the task to remove (must be positive integer).
        :return: True if removal was successful, False if task does not exist.
        :raises ValueError: If ID is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks whose name or description includes the search term (case-insensitive).

        :param task_term: Search keyword (must be non-empty string).
        :return: List of matching task dictionaries.
        :raises ValueError: If search term is invalid.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        matches = [
            {**task}  # Return a copy of the task dict
            for task in self._tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return matches

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed by ID.

        :param task_id: The ID of the task to mark as finished.
        :return: True if the task was updated, False if task does not exist.
        :raises ValueError: If ID is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if task is None:
            return False
        if not task["is_finished"]:
            task["is_finished"] = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks.

        :return: List of task dictionaries.
        """
        return [
            {**task} for task in sorted(self._tasks.values(), key=lambda t: t["id"])
        ]

    def clear_all(self) -> bool:
        """
        Delete all tasks.

        :return: True if any tasks were present and have been cleared, False if already empty.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


if __name__ == "__main__":
    # Sample usage and demonstration of TaskManager functionalities

    manager = TaskManager()

    # Adding tasks
    print("Adding tasks...")
    tid1 = manager.add("Buy groceries", "Milk, Eggs, Bread, Fruit")
    tid2 = manager.add("Read a book", "Finish reading 'Clean Code'")
    print(manager.get_all())

    # Searching tasks
    print("\nSearching for 'read':")
    print(manager.search("read"))

    # Finishing a task
    print(f"\nFinishing task with ID {tid2}:")
    print(manager.finish(tid2))
    print(manager.get_all())

    # Removing a task
    print(f"\nRemoving task with ID {tid1}:")
    print(manager.remove(tid1))
    print(manager.get_all())

    # Attempting to remove non-existent task
    print(f"\nTrying to remove a non-existent task with ID 999:")
    print(manager.remove(999))

    # Clearing all tasks
    print("\nClearing all tasks...")
    print(manager.clear_all())
    print(manager.get_all())

    # Input validation examples (should raise ValueError)
    try:
        manager.add("", "desc")
    except ValueError as ex:
        print(f"\nException: {ex}")

    try:
        manager.remove(-5)
    except ValueError as ex:
        print(f"Exception: {ex}")

    try:
        manager.search("")
    except ValueError as ex:
        print(f"Exception: {ex}")
