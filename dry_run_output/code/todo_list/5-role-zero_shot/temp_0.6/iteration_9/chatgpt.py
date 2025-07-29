
import sys
from typing import List, Dict, Optional

class Task:
    """
    Represents a single task in the todo list.
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
    Manages tasks: add, remove, search, finish, get_all, clear_all.
    Tasks are stored in-memory using a dictionary for efficient access.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a task and returns its unique ID.

        :param task_name: Name of the task (non-empty string).
        :param task_description: Description of the task (non-empty string).
        :return: Unique ID of the added task.
        :raises ValueError: If inputs are invalid.
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
        Removes a task by ID and returns success status.

        :param task_id: ID of the task to remove (positive integer).
        :return: True if the task was removed, False otherwise.
        :raises ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by name or description and returns matching results.

        :param task_term: Search term (non-empty string).
        :return: List of matching task dictionaries.
        :raises ValueError: If search term is invalid.
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
        Marks a task as completed.

        :param task_id: ID of the task to finish (positive integer).
        :return: True if task was marked as finished, False otherwise.
        :raises ValueError: If task_id is invalid.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        task = self._tasks.get(task_id)
        if task and not task.is_finished:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks with their details.

        :return: List of all task dictionaries.
        """
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks and returns success status.

        :return: True if tasks were cleared, False if already empty.
        """
        if not self._tasks:
            return False
        self._tasks.clear()
        return True


def main():
    """
    Simple console interface for TaskManager.
    """
    tm = TaskManager()
    menu = (
        "\nTodo List App\n"
        "1. Add Task\n"
        "2. Remove Task\n"
        "3. Search Tasks\n"
        "4. Finish Task\n"
        "5. Show All Tasks\n"
        "6. Clear All Tasks\n"
        "7. Exit\n"
    )

    def print_tasks(tasks):
        if not tasks:
            print("No tasks found.")
            return
        for t in tasks:
            status = "Finished" if t['is_finished'] else "Pending"
            print(f"ID: {t['id']} | Name: {t['task_name']} | Description: {t['task_description']} | Status: {status}")

    while True:
        print(menu)
        choice = input("Select an option: ").strip()
        try:
            if choice == '1':
                name = input("Enter task name: ").strip()
                desc = input("Enter task description: ").strip()
                task_id = tm.add(name, desc)
                print(f"Task added with ID: {task_id}")

            elif choice == '2':
                tid = int(input("Enter task ID to remove: "))
                if tm.remove(tid):
                    print("Task removed.")
                else:
                    print("Task not found.")

            elif choice == '3':
                term = input("Enter search term: ").strip()
                results = tm.search(term)
                print_tasks(results)

            elif choice == '4':
                tid = int(input("Enter task ID to finish: "))
                if tm.finish(tid):
                    print("Task marked as finished.")
                else:
                    print("Task not found or already finished.")

            elif choice == '5':
                print_tasks(tm.get_all())

            elif choice == '6':
                if tm.clear_all():
                    print("All tasks cleared.")
                else:
                    print("Task list is already empty.")

            elif choice == '7':
                print("Exiting. Goodbye!")
                break
            else:
                print("Invalid option. Please select from 1-7.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()
