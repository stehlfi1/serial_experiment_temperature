
import sys
from typing import List, Dict, Optional


class TaskValidationError(ValueError):
    """Custom exception for invalid task operations."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception for missing tasks."""
    pass


class Task:
    """
    Represents a single todo task.
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
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Manages a collection of todo tasks with operations to add, remove, search, finish, list, and clear tasks.
    """

    def __init__(self):
        # Internal storage: id -> Task
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1  # monotonically increasing unique task IDs

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task and returns its unique ID.

        :param task_name: Name of the task (non-empty string)
        :param task_description: Description of the task (non-empty string)
        :return: Unique integer ID of the created task
        :raises TaskValidationError: If input is invalid
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description must be a non-empty string.")

        task_id = self._next_id
        self._tasks[task_id] = Task(task_id, task_name.strip(), task_description.strip())
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        :param task_id: Integer ID of the task to remove
        :return: True if task was removed, False otherwise
        :raises TaskValidationError: If task_id is invalid
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches for tasks by name or description (case-insensitive substring match).

        :param task_term: Search term string (non-empty)
        :return: List of matching task dictionaries
        :raises TaskValidationError: If search term is invalid
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

        :param task_id: Integer ID of the task to finish
        :return: True if the task was marked as finished, False otherwise
        :raises TaskValidationError: If task_id is invalid
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task is None:
            return False
        if not task.is_finished:
            task.is_finished = True
            return True
        return False  # Already finished

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks with their details.

        :return: List of all task dictionaries
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks.

        :return: True if tasks were cleared, False if already empty
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


def main():
    """
    Console-based interface for the todo list application.
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
        "7. Exit\n"
        "Select an option (1-7): "
    )

    def print_tasks(tasks: List[Dict]):
        if not tasks:
            print("No tasks found.")
            return
        print("\nTasks:")
        for t in tasks:
            status = "Finished" if t['is_finished'] else "Pending"
            print(f"ID: {t['id']} | Name: {t['task_name']} | Description: {t['task_description']} | Status: {status}")

    while True:
        try:
            choice = input(menu).strip()
            if choice == '1':
                name = input("Enter task name: ").strip()
                desc = input("Enter task description: ").strip()
                try:
                    task_id = manager.add(name, desc)
                    print(f"Task added with ID {task_id}.")
                except TaskValidationError as e:
                    print(f"Error: {e}")

            elif choice == '2':
                try:
                    task_id = int(input("Enter task ID to remove: ").strip())
                    if manager.remove(task_id):
                        print("Task removed.")
                    else:
                        print("Task not found.")
                except (ValueError, TaskValidationError) as e:
                    print(f"Error: {e}")

            elif choice == '3':
                term = input("Enter search term: ").strip()
                try:
                    results = manager.search(term)
                    print_tasks(results)
                except TaskValidationError as e:
                    print(f"Error: {e}")

            elif choice == '4':
                try:
                    task_id = int(input("Enter task ID to finish: ").strip())
                    if manager.finish(task_id):
                        print("Task marked as finished.")
                    else:
                        print("Task not found or already finished.")
                except (ValueError, TaskValidationError) as e:
                    print(f"Error: {e}")

            elif choice == '5':
                print_tasks(manager.get_all())

            elif choice == '6':
                if manager.clear_all():
                    print("All tasks cleared.")
                else:
                    print("No tasks to clear.")

            elif choice == '7':
                print("Exiting. Goodbye!")
                break

            else:
                print("Invalid option. Please select a number between 1 and 7.")

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting.")
            break
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
