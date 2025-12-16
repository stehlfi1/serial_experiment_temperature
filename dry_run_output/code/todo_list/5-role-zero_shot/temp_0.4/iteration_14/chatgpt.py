
"""
Console-based Todo List App
Author: [Your Name]
Date: [Current Date]
Description: An OOP-based, high-quality Python implementation of a todo list manager
meeting ISO/IEC 25010 requirements for software quality: maintainability, correctness, performance,
modularity, safety, testability, readability, and documentation.
"""

from typing import Dict, List


class Task:
    """
    Represents a single todo task.
    """
    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> dict:
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
    TaskManager provides an interface for managing todo tasks.
    """

    def __init__(self):
        # Internal storage for tasks: {task_id: Task}
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task. Returns the unique task ID.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by ID.

        Returns:
            bool: True if the task was removed, False if not found.
        Raises:
            ValueError: If task_id is not positive.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[dict]:
        """
        Searches for tasks by name or description.

        Returns:
            List[dict]: List of matching tasks in dict format.

        Raises:
            ValueError: If task_term is empty.
        """
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = task_term.strip().lower()
        results = [
            task.to_dict() for task in self._tasks.values()
            if term_lower in task.name.lower() or term_lower in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Returns:
            bool: True if successful, False if task does not exist.
        Raises:
            ValueError: If task_id is not positive.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[dict]:
        """
        Retrieves all tasks.

        Returns:
            List[dict]: All tasks in (id, name, desc, is_finished) format.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if tasks cleared, False if already empty.
        """
        if self._tasks:
            self._tasks.clear()
            self._next_id = 1
            return True
        return False


# --- Optional: Simple console demo / test driver (For testability & demonstration) ---
if __name__ == "__main__":
    def print_tasks(tasks):
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            print(f"ID: {task['id']} | Name: {task['task_name']} | Desc: {task['task_description']} | Finished: {task['is_finished']}")

    # Sample usage:
    manager = TaskManager()

    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        id2 = manager.add("Read a book", "Read 'Clean Code'")
        print("Tasks after adding:")
        print_tasks(manager.get_all())

        print("\nSearching for 'read':")
        print_tasks(manager.search("read"))

        manager.finish(id2)
        print("\nTasks after finishing task 2:")
        print_tasks(manager.get_all())

        manager.remove(id1)
        print("\nTasks after removing task 1:")
        print_tasks(manager.get_all())

        manager.clear_all()
        print("\nTasks after clearing all:")
        print_tasks(manager.get_all())
    except Exception as e:
        print(f"Error: {e}")
