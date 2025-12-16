
import sys
from typing import List, Dict

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
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }

class TaskManager:
    """
    Manages tasks for a todo list application.

    Methods:
        add(task_name, task_description): Adds a new task.
        remove(task_id): Removes a task by ID.
        search(task_term): Searches for tasks by name or description.
        finish(task_id): Marks a task as completed.
        get_all(): Retrieves all tasks.
        clear_all(): Removes all tasks.
    """

    def __init__(self):
        # Store task_id -> Task for O(1) lookup, insert and delete
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a task and returns its unique ID.

        Raises:
            ValueError: If task_name or task_description is empty.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name must be a non-empty string.")
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string.")

        tid = self._next_id
        task = Task(tid, task_name.strip(), task_description.strip())
        self._tasks[tid] = task
        self._next_id += 1
        return tid

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by ID and returns success status.

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        return self._tasks.pop(task_id, None) is not None

    def search(self, task_term: str) -> List[Dict]:
        """
        Searches tasks by name or description (case-insensitive) 
        and returns matching task dicts.

        Raises:
            ValueError: If task_term is not a non-empty string.
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

        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict]:
        """
        Retrieves all tasks as a list of dicts.
        """
        return [task.to_dict() for task in sorted(self._tasks.values(), key=lambda t: t.id)]

    def clear_all(self) -> bool:
        """
        Deletes all tasks and returns success status.
        """
        self._tasks.clear()
        return len(self._tasks) == 0

def main():
    """
    Console-based UI for the todo list app.
    """
    tm = TaskManager()

    MENU = """\nTodo List Menu:
1. Add Task
2. Remove Task
3. Search Tasks
4. Finish Task
5. List All Tasks
6. Clear All Tasks
7. Exit
"""

    while True:
        print(MENU)
        choice = input("Enter choice (1-7): ").strip()
        try:
            if choice == '1':
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = tm.add(name, desc)
                print(f"Task added with ID {task_id}.")
            elif choice == '2':
                tid = int(input("Enter Task ID to remove: "))
                if tm.remove(tid):
                    print("Task removed.")
                else:
                    print("Task not found.")
            elif choice == '3':
                term = input("Enter search term: ")
                results = tm.search(term)
                if not results:
                    print("No tasks found.")
                else:
                    for t in results:
                        print(f"ID:{t['id']} | Name:{t['task_name']} | "
                              f"Description:{t['task_description']} | Finished:{t['is_finished']}")
            elif choice == '4':
                tid = int(input("Enter Task ID to mark as finished: "))
                if tm.finish(tid):
                    print("Task marked as finished.")
                else:
                    print("Task not found.")
            elif choice == '5':
                tasks = tm.get_all()
                if not tasks:
                    print("No tasks to display.")
                else:
                    for t in tasks:
                        print(f"ID:{t['id']} | Name:{t['task_name']} | "
                              f"Description:{t['task_description']} | Finished:{t['is_finished']}")
            elif choice == '6':
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").strip().lower()
                if confirm == 'yes':
                    tm.clear_all()
                    print("All tasks cleared.")
                else:
                    print("Operation cancelled.")
            elif choice == '7':
                print("Exiting Todo List. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 7.")
        except ValueError as ve:
            print(f"Input error: {ve}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
