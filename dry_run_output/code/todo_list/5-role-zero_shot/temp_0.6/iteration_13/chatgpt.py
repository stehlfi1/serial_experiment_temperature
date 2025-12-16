
import sys
from typing import List, Dict, Optional

class TaskValidationError(ValueError):
    """Exception raised for errors in task input values."""
    pass

class TaskNotFoundError(KeyError):
    """Exception raised when a task ID is not found."""
    pass

class Task:
    """
    Represents a single todo task.

    Attributes:
        id (int): Unique identifier for the task.
        name (str): Name/title of the task.
        description (str): Description/details of the task.
        is_finished (bool): Completion status of the task.
    """
    __slots__ = ('id', 'name', 'description', 'is_finished')

    def __init__(self, task_id: int, name: str, description: str):
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """Returns the task as a dictionary."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }

class TaskManager:
    """
    Manages the collection of todo tasks, providing CRUD and query operations.
    Complies with ISO/IEC 25010 requirements for maintainability, robustness, and reliability.
    """

    def __init__(self):
        # In-memory storage mapping ID to Task for O(1) access.
        self._tasks: Dict[int, Task] = {}
        # Simple auto-incrementing integer for task IDs. Thread-safe alternatives can be used in production.
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task.

        Args:
            task_name (str): The name/title of the task.
            task_description (str): Description/details of the task.

        Returns:
            int: The unique ID assigned to the task.

        Raises:
            TaskValidationError: If name or description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description must be a non-empty string.")

        task_id = self._next_id
        task = Task(task_id, task_name.strip(), task_description.strip())
        self._tasks[task_id] = task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task existed and was removed, False otherwise.

        Raises:
            TaskValidationError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks matching a term in their name or description (case-insensitive).

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: List of all matching task dictionaries.

        Raises:
            TaskValidationError: If task_term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term must be a non-empty string.")
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

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if successful, False if task doesn't exist or is already finished.

        Raises:
            TaskValidationError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task and not task.is_finished:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks.

        Returns:
            list[dict]: List of all task dictionaries.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks in the system.

        Returns:
            bool: True if any tasks were deleted, False if no task existed.
        """
        had_tasks = bool(self._tasks)
        self._tasks.clear()
        return had_tasks

# Example interactive console functionality (test/demo purposes only)
if __name__ == "__main__":
    """
    Console-based demo for the TaskManager.
    This section is isolated from the core logic for modularity and testability.
    """
    manager = TaskManager()

    MENU = """
======= TODO LIST MENU =======
1. Add Task
2. Remove Task
3. Search Tasks
4. Finish Task
5. List All Tasks
6. Clear All Tasks
7. Exit
Select an option: """

    def print_tasks(tasks: List[Dict]):
        if not tasks:
            print("No tasks found.")
        else:
            for task in tasks:
                status = "✓" if task['is_finished'] else "✗"
                print(f"[{task['id']}] {task['task_name']} - {task['task_description']} (Finished: {status})")

    while True:
        try:
            choice = input(MENU).strip()
            if choice == "1":
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                try:
                    new_id = manager.add(name, description)
                    print(f"Task added with ID {new_id}.")
                except TaskValidationError as e:
                    print(f"Error: {e}")

            elif choice == "2":
                tid = input("Enter task ID to remove: ")
                try:
                    if manager.remove(int(tid)):
                        print("Task removed.")
                    else:
                        print("No such task.")
                except (ValueError, TaskValidationError):
                    print("Invalid ID.")

            elif choice == "3":
                term = input("Enter search term: ")
                try:
                    results = manager.search(term)
                    print_tasks(results)
                except TaskValidationError as e:
                    print(f"Error: {e}")

            elif choice == "4":
                tid = input("Enter task ID to finish: ")
                try:
                    if manager.finish(int(tid)):
                        print("Task marked as finished.")
                    else:
                        print("Task not found or already finished.")
                except (ValueError, TaskValidationError):
                    print("Invalid ID.")

            elif choice == "5":
                all_tasks = manager.get_all()
                print_tasks(all_tasks)

            elif choice == "6":
                confirmed = input("Are you sure you want to remove all tasks? (y/N): ").lower()
                if confirmed == "y":
                    if manager.clear_all():
                        print("All tasks cleared.")
                    else:
                        print("No tasks to clear.")

            elif choice == "7":
                print("Exiting. Goodbye!")
                break
            else:
                print("Please select a valid option (1-7).")
        except KeyboardInterrupt:
            print("\nExiting. Goodbye!")
            sys.exit(0)
