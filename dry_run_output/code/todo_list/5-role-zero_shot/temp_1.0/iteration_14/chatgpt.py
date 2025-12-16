
import sys
from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception for invalid task operations."""


class Task:
    """
    Represents a single todo task.

    Attributes:
        id (int): Unique identifier for the task.
        name (str): Name of the task.
        description (str): Description of the task.
        is_finished (bool): Completion status.
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
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished,
        }


class TaskManager:
    """
    Manages todo tasks in memory.

    Provides interface for adding, removing, searching, finishing,
    retrieving all, and clearing all tasks.
    """

    def __init__(self):
        # Task ID to Task instance mapping.
        self._tasks: Dict[int, Task] = {}
        # Next task ID to use (auto increment).
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a task to the list.

        Args:
            task_name (str): Name of the task. Must be non-empty.
            task_description (str): Description. Must be non-empty.

        Returns:
            int: Unique ID of the added task.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id (int): ID of the task to remove.

        Returns:
            bool: True if removed, False if not found or invalid.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by name or description.

        Args:
            task_term (str): String to search for.

        Returns:
            List[dict]: List of matching task dictionaries.

        Raises:
            ValueError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term cannot be empty.")

        result = []
        search_term = task_term.strip().lower()
        for task in self._tasks.values():
            if (search_term in task.name.lower()) or (search_term in task.description.lower()):
                result.append(task.to_dict())
        return result

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id (int): Task ID.

        Returns:
            bool: True if successfully marked, False otherwise.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if not task:
            return False
        if task.is_finished:
            # Already finished, treat as success
            return True
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            List[dict]: All tasks in (id, task_name, task_description, is_finished) format.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        Returns:
            bool: True if tasks cleared, False if already empty.
        """
        cleared = bool(self._tasks)
        self._tasks.clear()
        return cleared


def main():
    """
    Example interactive console application for managing tasks.
    """
    import readline

    manager = TaskManager()
    menu = """
Todo List Console Application
----------------------------
1. Add Task
2. Remove Task
3. Search Tasks
4. Finish Task
5. Show All Tasks
6. Clear All Tasks
0. Exit
"""

    def input_int(prompt: str) -> Optional[int]:
        try:
            value = input(prompt)
            return int(value)
        except (ValueError, TypeError):
            print("Please enter a valid integer value.")
            return None

    while True:
        print(menu)
        choice = input("Enter your choice: ").strip()
        if choice == "1":
            name = input("Task name: ").strip()
            desc = input("Task description: ").strip()
            try:
                task_id = manager.add(name, desc)
                print(f"Task added successfully with ID {task_id}")
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "2":
            tid = input_int("Task ID to remove: ")
            if tid is not None:
                try:
                    success = manager.remove(tid)
                    if success:
                        print("Task removed successfully.")
                    else:
                        print("Task not found.")
                except ValueError as e:
                    print(f"Error: {e}")
        elif choice == "3":
            term = input("Enter search term: ").strip()
            try:
                results = manager.search(term)
                print(f"{len(results)} task(s) found:")
                for t in results:
                    print(t)
            except ValueError as e:
                print(f"Error: {e}")
        elif choice == "4":
            tid = input_int("Task ID to mark as finished: ")
            if tid is not None:
                try:
                    success = manager.finish(tid)
                    if success:
                        print("Task marked as finished.")
                    else:
                        print("Task not found.")
                except ValueError as e:
                    print(f"Error: {e}")
        elif choice == "5":
            all_tasks = manager.get_all()
            if not all_tasks:
                print("No tasks found.")
            else:
                print("All tasks:")
                for t in all_tasks:
                    print(t)
        elif choice == "6":
            if manager.clear_all():
                print("All tasks cleared.")
            else:
                print("No tasks to clear.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
