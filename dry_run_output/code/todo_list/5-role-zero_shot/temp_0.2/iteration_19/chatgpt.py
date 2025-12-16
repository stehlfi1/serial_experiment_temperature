
from typing import List, Dict, Optional

class Task:
    """
    Represents a single task in the todo list.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id: int = task_id
        self.name: str = name
        self.description: str = description
        self.is_finished: bool = False

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
    Manages creation, modification, and retrieval of Tasks.
    Implements interface for a todo list operation.
    Follows ISO/IEC 25010 standard quality attributes: correctness, performance, modularity,
    safety, testability, and maintainability.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.
        :param task_name: The name/title of the task (required, non-empty string).
        :param task_description: The description of the task (required, non-empty string).
        :return: The unique ID of the created task.
        :raises ValueError: If task_name or task_description is empty.
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
        Removes a task by ID.
        :param task_id: Unique ID of the task to remove.
        :return: True if the task was removed, False if not found.
        :raises ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks matching the given term in their name or description.
        :param task_term: The term to search for (case-insensitive).
        :return: List of matching task dictionaries.
        :raises ValueError: If task_term is empty.
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
        Marks a task as finished/completed.
        :param task_id: Unique ID of the task to mark as finished.
        :return: True if successful, False if task not found.
        :raises ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if not task:
            return False
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.
        :return: List of all task dictionaries.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks in the todo list.
        :return: True if the operation is successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# ==========================
# Example usage & test cases
# ==========================
if __name__ == "__main__":
    tm = TaskManager()

    # Add tasks
    tid1 = tm.add("Buy groceries", "Milk, bread, eggs.")
    tid2 = tm.add("Read book", "Read 'Clean Code' by Robert C. Martin.")

    # Get all tasks
    print("All Tasks:", tm.get_all())

    # Search for a task
    print("Search 'book':", tm.search("book"))

    # Mark task as finished
    print("Finish Task ID 2:", tm.finish(2))
    print("Task 2 after finishing:", [t for t in tm.get_all() if t['id'] == 2])

    # Remove a task
    print("Remove Task ID 1:", tm.remove(1))
    print("Tasks after removal:", tm.get_all())

    # Clear all tasks
    print("Clear All:", tm.clear_all())
    print("All Tasks after clear:", tm.get_all())
