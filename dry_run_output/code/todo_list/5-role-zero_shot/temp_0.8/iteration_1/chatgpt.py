
import sys
from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception for invalid task operations."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception when a task is not found."""
    pass


class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task.
        name (str): Name/title of the task.
        description (str): Detailed description of the task.
        is_finished (bool): Completion status of the task.
    """
    def __init__(self, id: int, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """Return a dictionary representation of the task."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages a collection of tasks, providing CRUD and search operations.

    Methods:
        add(task_name: str, task_description: str) -> int
        remove(task_id: int) -> bool
        search(task_term: str) -> list[dict]
        finish(task_id: int) -> bool
        get_all() -> list[dict]
        clear_all() -> bool
    """

    def __init__(self):
        # Use a dict for O(1) lookup, insertion, and deletion by task ID
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name (str): The name/title of the task.
            task_description (str): The description of the task.

        Returns:
            int: The unique ID of the newly added task.

        Raises:
            TaskValidationError: If task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description cannot be empty.")

        task = Task(self._next_id, task_name.strip(), task_description.strip())
        self._tasks[task.id] = task
        self._next_id += 1
        return task.id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id (int): The ID of the task to remove.

        Returns:
            bool: True if the task was removed, False if not found.

        Raises:
            TaskValidationError: If the task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            return False
        del self._tasks[task_id]
        return True

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by name or description.

        Args:
            task_term (str): The term to search for.

        Returns:
            list[dict]: List of matching tasks (as dicts). Empty if none found.

        Raises:
            TaskValidationError: If the search term is invalid.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term cannot be empty.")

        term_lower = task_term.strip().lower()
        result = [
            task.to_dict()
            for task in self._tasks.values()
            if term_lower in task.name.lower() or term_lower in task.description.lower()
        ]
        return result

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id (int): The ID of the task to mark as finished.

        Returns:
            bool: True if successfully marked, False if task not found.

        Raises:
            TaskValidationError: If the task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id < 1:
            raise TaskValidationError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if not task:
            return False
        task.is_finished = True
        return True

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks, in order of addition.

        Returns:
            list[dict]: List of all tasks (as dicts).
        """
        # Sorted by task ID (order of addition)
        return [task.to_dict() for task in sorted(self._tasks.values(), key=lambda t: t.id)]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            bool: True if tasks were cleared, False if there were no tasks.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


# --- Minimal console interface for testing and demonstration purposes ---

def print_tasks(tasks: List[Dict]) -> None:
    """Helper function to print a list of tasks in a readable format."""
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        status = "✔" if task['is_finished'] else "✗"
        print(f"[{task['id']}] {task['task_name']} - {task['task_description']} [Finished: {status}]")


def main():
    """
    Minimal CLI interface for TaskManager.
    Allows demonstration and manual testing.
    """
    tm = TaskManager()

    menu = """
Todo List App Menu:
1. Add Task
2. Remove Task
3. Search Tasks
4. Finish Task
5. Show All Tasks
6. Clear All Tasks
0. Exit
"""

    while True:
        print(menu)
        choice = input("Select an option (0-6): ").strip()

        if choice == '1':
            name = input("Enter task name: ").strip()
            desc = input("Enter task description: ").strip()
            try:
                task_id = tm.add(name, desc)
                print(f"Task added with ID: {task_id}")
            except TaskValidationError as e:
                print(f"Error: {e}")

        elif choice == '2':
            try:
                tid = int(input("Enter task ID to remove: ").strip())
                success = tm.remove(tid)
                if success:
                    print("Task removed successfully.")
                else:
                    print("Task not found.")
            except (ValueError, TaskValidationError) as e:
                print(f"Error: {e}")

        elif choice == '3':
            term = input("Enter search term: ").strip()
            try:
                results = tm.search(term)
                print_tasks(results)
            except TaskValidationError as e:
                print(f"Error: {e}")

        elif choice == '4':
            try:
                tid = int(input("Enter task ID to finish: ").strip())
                success = tm.finish(tid)
                if success:
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            except (ValueError, TaskValidationError) as e:
                print(f"Error: {e}")

        elif choice == '5':
            tasks = tm.get_all()
            print_tasks(tasks)

        elif choice == '6':
            success = tm.clear_all()
            if success:
                print("All tasks cleared.")
            else:
                print("No tasks to clear.")

        elif choice == '0':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose between 0 and 6.")

if __name__ == "__main__":
    main()
