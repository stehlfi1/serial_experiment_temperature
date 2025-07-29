
import sys
from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(LookupError):
    """Custom exception for not found tasks."""
    pass


class Task:
    """
    Represents a single todo task.
    """

    def __init__(self, task_id: int, name: str, description: str) -> None:
        """
        Initialize a Task.

        :param task_id: Unique identifier for the task.
        :param name: Name of the task.
        :param description: Description of the task.
        """
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False

    def to_dict(self) -> Dict:
        """
        Return a dictionary representation of the task.

        :return: dict with keys: id, task_name, task_description, is_finished
        """
        return {
            "id": self.id,
            "task_name": self.name,
            "task_description": self.description,
            "is_finished": self.is_finished
        }


class TaskManager:
    """
    Manages tasks with add, remove, search, finish, get_all, and clear_all operations.
    """

    def __init__(self) -> None:
        """
        Initialize the TaskManager.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a task to the manager.

        :param task_name: The name of the task (non-empty).
        :param task_description: The description of the task (non-empty).
        :return: Unique integer ID of the newly added task.
        :raises TaskValidationError: If inputs are invalid.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name cannot be empty.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task by ID.

        :param task_id: The ID of the task to be removed.
        :return: True if removal succeeded, False otherwise.
        :raises TaskValidationError: If ID is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description (case-insensitive).

        :param task_term: The search term (non-empty).
        :return: List of matching tasks as dicts.
        :raises TaskValidationError: If search term is empty.
        """
        if not isinstance(task_term, str) or not task_term.strip():
            raise TaskValidationError("Search term cannot be empty.")
        term_lower = task_term.strip().lower()
        results = [
            task.to_dict()
            for task in self._tasks.values()
            if term_lower in task.name.lower() or term_lower in task.description.lower()
        ]
        return results

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as finished.

        :param task_id: The ID of the task to mark as finished.
        :return: True if operation succeeded, False otherwise.
        :raises TaskValidationError: If ID is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task:
            if not task.is_finished:
                task.is_finished = True
                return True
            return False  # Already finished
        return False

    def get_all(self) -> List[Dict]:
        """
        Get all tasks.

        :return: List of all tasks as dicts.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Delete all tasks.

        :return: True if operation succeeded, False otherwise.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


def _print_task(task: Dict) -> None:
    """
    Utility function to print a single task in a readable format.
    """
    status = "Finished" if task['is_finished'] else "Pending"
    print(f"ID: {task['id']}\nName: {task['task_name']}\nDescription: {task['task_description']}\nStatus: {status}\n")


def main() -> None:
    """
    Sample console interface for TaskManager. (For demonstration purposes & testability)
    """
    manager = TaskManager()
    menu = (
        "\nTodo List Menu:\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. List All Tasks\n"
        "6. Clear All Tasks\n"
        "0. Exit\n"
        "Select an option: "
    )

    while True:
        try:
            choice = input(menu).strip()
            if choice == "1":
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                try:
                    task_id = manager.add(name, desc)
                    print(f"Task added with ID: {task_id}")
                except TaskValidationError as e:
                    print(f"Error: {e}")

            elif choice == "2":
                try:
                    tid = int(input("Enter task ID to remove: "))
                    if manager.remove(tid):
                        print("Task removed.")
                    else:
                        print("No such task ID.")
                except (ValueError, TaskValidationError) as e:
                    print(f"Error: {e}")

            elif choice == "3":
                term = input("Enter search term: ")
                try:
                    results = manager.search(term)
                    if not results:
                        print("No matching tasks found.")
                    else:
                        print(f"Found {len(results)} matching task(s):")
                        for task in results:
                            _print_task(task)
                except TaskValidationError as e:
                    print(f"Error: {e}")

            elif choice == "4":
                try:
                    tid = int(input("Enter task ID to finish: "))
                    if manager.finish(tid):
                        print("Task marked as finished.")
                    else:
                        print("No such unfinished task ID.")
                except (ValueError, TaskValidationError) as e:
                    print(f"Error: {e}")

            elif choice == "5":
                tasks = manager.get_all()
                if not tasks:
                    print("No tasks in the list.")
                else:
                    print(f"Listing {len(tasks)} task(s):")
                    for task in tasks:
                        _print_task(task)

            elif choice == "6":
                if manager.clear_all():
                    print("All tasks have been cleared.")
                else:
                    print("No tasks to clear.")

            elif choice == "0":
                print("Goodbye!")
                break

            else:
                print("Invalid option. Please try again.")

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break


if __name__ == "__main__":
    main()
