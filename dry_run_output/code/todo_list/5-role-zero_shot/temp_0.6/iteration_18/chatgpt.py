
from typing import List, Dict, Optional


class Task:
    """
    Represents a single todo task.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id: int = task_id
        self.name: str = name
        self.description: str = description
        self.is_finished: bool = False

    def to_dict(self) -> Dict:
        """
        Return a dictionary representation of the task.
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Task Manager provides a console-based todo list following ISO/IEC 25010 quality standards.
    Supports add, remove, search, finish, get_all, and clear_all operations.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}  # Efficient lookups by task ID
        self._next_id: int = 1  # Incremental ID for unique tasks

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a task to the todo list.

        Args:
            task_name (str): Name of the task (non-empty)
            task_description (str): Description of the task (non-empty)
        Returns:
            int: Unique ID of the newly added task

        Raises:
            ValueError: If task_name or task_description are empty
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._next_id += 1
        new_task = Task(task_id, task_name.strip(), task_description.strip())
        self._tasks[task_id] = new_task
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): The ID of the task to remove

        Returns:
            bool: True if the task was removed, False if not found

        Raises:
            ValueError: If the task_id is not positive
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks containing the term in their name or description.

        Args:
            task_term (str): The search term (non-empty string)

        Returns:
            list[dict]: List of matching tasks in the required format

        Raises:
            ValueError: If task_term is empty
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.lower().strip()
        results = []
        for task in self._tasks.values():
            if term in task.name.lower() or term in task.description.lower():
                results.append(task.to_dict())
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished by its ID.

        Args:
            task_id (int): The ID of the task to finish

        Returns:
            bool: True if the task is now finished, False if task not found

        Raises:
            ValueError: If the task_id is not positive
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is not None:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Gets all tasks in the todo list.

        Returns:
            list[dict]: All tasks with their details
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Clears all tasks from the todo list.

        Returns:
            bool: True if tasks were cleared, False if already empty
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


# Example usage and rudimentary testing (can be adjusted or expanded for unit testing)

if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    try:
        id1 = tm.add("Buy groceries", "Milk, Eggs, Bread")
        id2 = tm.add("Read book", "Finish 'Clean Code'")
        id3 = tm.add("Workout", "Go for a 30 minute run")
    except ValueError as e:
        print(f"Input Error: {e}")

    # Get all tasks
    print("All tasks:")
    print(tm.get_all())

    # Search tasks
    print("\nSearch for 'book':")
    print(tm.search("book"))

    # Finish a task
    print("\nFinish task ID 2:")
    print(tm.finish(2))
    print(tm.get_all())

    # Remove a task
    print("\nRemove task ID 1:")
    print(tm.remove(1))
    print(tm.get_all())

    # Clear all tasks
    print("\nClear all tasks:")
    print(tm.clear_all())
    print(tm.get_all())
