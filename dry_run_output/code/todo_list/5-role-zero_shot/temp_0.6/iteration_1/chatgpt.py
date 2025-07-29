
import sys
from typing import List, Dict, Optional

class TaskManager:
    """
    TaskManager provides an in-memory todo list manager with operations to add, remove,
    search, finish, retrieve, and clear tasks. Each task is represented as a dictionary
    with the following fields:
        - id (int): Unique identifier for the task
        - task_name (str): Name/title of the task
        - task_description (str): Description of the task
        - is_finished (bool): Completion status
    """

    def __init__(self):
        """Initialize the TaskManager with empty storage and task ID counter."""
        self._tasks: Dict[int, Dict] = {}  # Maps task_id to task dict
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.

        Args:
            task_name (str): Name/title of the task. Must not be empty.
            task_description (str): Description of the task. Must not be empty.

        Returns:
            int: The unique ID assigned to the new task.

        Raises:
            ValueError: If task_name or task_description is empty.
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
        Remove a task by its ID.

        Args:
            task_id (int): The unique ID of the task to remove.

        Returns:
            bool: True if the task was removed, False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description (case-insensitive, substring match).

        Args:
            task_term (str): The search term to look for.

        Returns:
            List[Dict]: List of matching tasks (each as a dict).

        Raises:
            ValueError: If task_term is empty or not a string.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise ValueError("Search term must be a non-empty string.")

        term = task_term.strip().lower()
        results = [
            task.copy() for task in self._tasks.values()
            if term in task["task_name"].lower() or term in task["task_description"].lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished.

        Args:
            task_id (int): The unique ID of the task to complete.

        Returns:
            bool: True if the task was marked as finished, False if not found.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the todo list.

        Returns:
            List[Dict]: List of all task dictionaries.
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.

        Returns:
            bool: True if tasks were cleared (even if already empty).
        """
        self._tasks.clear()
        return True

# Optional: Example usage for console interaction (testability & demonstration)
def main():
    """
    Simple console interface for TaskManager.
    """
    manager = TaskManager()

    MENU = """
    ==== Todo List Menu ====
    1. Add Task
    2. Remove Task
    3. Search Tasks
    4. Finish Task
    5. Show All Tasks
    6. Clear All Tasks
    7. Exit
    ========================
    """

    def print_tasks(tasks: List[Dict]):
        if not tasks:
            print("No tasks found.")
            return
        print(f"{'ID':<5} {'Finished':<10} {'Name':<20} {'Description'}")
        print("-" * 60)
        for t in tasks:
            print(f"{t['id']:<5} {str(t['is_finished']):<10} {t['task_name']:<20} {t['task_description']}")

    while True:
        print(MENU)
        try:
            choice = input("Choose an option [1-7]: ").strip()
            if choice == '1':
                name = input("Task Name: ").strip()
                desc = input("Task Description: ").strip()
                try:
                    task_id = manager.add(name, desc)
                    print(f"Task added with ID {task_id}.")
                except ValueError as ve:
                    print(f"Error: {ve}")
            elif choice == '2':
                tid = input("Task ID to remove: ").strip()
                try:
                    tid = int(tid)
                    if manager.remove(tid):
                        print("Task removed.")
                    else:
                        print("Task not found.")
                except ValueError as ve:
                    print(f"Error: {ve}")
            elif choice == '3':
                term = input("Search term: ").strip()
                try:
                    results = manager.search(term)
                    print_tasks(results)
                except ValueError as ve:
                    print(f"Error: {ve}")
            elif choice == '4':
                tid = input("Task ID to finish: ").strip()
                try:
                    tid = int(tid)
                    if manager.finish(tid):
                        print("Task marked as finished.")
                    else:
                        print("Task not found.")
                except ValueError as ve:
                    print(f"Error: {ve}")
            elif choice == '5':
                tasks = manager.get_all()
                print_tasks(tasks)
            elif choice == '6':
                manager.clear_all()
                print("All tasks cleared.")
            elif choice == '7':
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-7.")
        except KeyboardInterrupt:
            print("\nExiting.")
            break

if __name__ == "__main__":
    main()
