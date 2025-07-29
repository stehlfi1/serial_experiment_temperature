
"""
A high-quality, maintainable console-based To-Do list application.

This module contains the TaskManager class, which encapsulates all the logic
for managing tasks, and a simple command-line interface for user interaction.
The design adheres to the principles of the ISO/IEC 25010 standard for
software quality.
"""

from typing import List, Dict, Any

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a clean interface for adding, removing, searching,
    and updating tasks. It is designed for correctness, efficiency, and
    testability.

    Attributes:
        _tasks (dict[int, dict[str, Any]]): A private dictionary to store tasks,
            mapping a unique task ID to a dictionary of task details.
            Using a dictionary provides O(1) average time complexity for
            ID-based lookups, insertions, and deletions.
        _next_id (int): A private counter to ensure unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Dict[str, Any]] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is an empty or whitespace-only string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        normalized_term = search_term.lower().strip()
        
        # Return copies to prevent external modification of internal state
        return [
            task.copy() for task in self._tasks.values()
            if normalized_term in task["name"].lower()
            or normalized_term in task["description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. Returns copies to
            ensure data encapsulation.
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


def print_task(task: Dict[str, Any]) -> None:
    """Helper function to format and print a single task."""
    status = "Finished" if task["is_finished"] else "Pending"
    print(
        f"  ID: {task['id']} | Status: {status}\n"
        f"  Name: {task['name']}\n"
        f"  Description: {task['description']}\n"
        f"{'-'*30}"
    )

def main() -> None:
    """Main function to run the console-based UI for the To-Do list app."""
    task_manager = TaskManager()
    print("--- Console To-Do List Application ---")

    # Pre-populate with some data for demonstration
    task_manager.add("Buy groceries", "Milk, Bread, Cheese")
    task_manager.add("Finish report", "Complete the Q3 financial report for review.")
    task_manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Mark Task as Finished")
        print("5. List All Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                desc = input("Enter task description: ")
                task_id = task_manager.add(name, desc)
                print(f"Success: Task added with ID: {task_id}")

            elif choice == '2':
                task_id_str = input("Enter task ID to remove: ")
                task_manager.remove(int(task_id_str))
                print(f"Success: Task {task_id_str} removed.")

            elif choice == '3':
                term = input("Enter search term: ")
                results = task_manager.search(term)
                print(f"\nFound {len(results)} matching task(s):")
                if not results:
                    print("No tasks found matching your search.")
                for task in results:
                    print_task(task)

            elif choice == '4':
                task_id_str = input("Enter task ID to mark as finished: ")
                task_manager.finish(int(task_id_str))
                print(f"Success: Task {task_id_str} marked as finished.")

            elif choice == '5':
                all_tasks = task_manager.get_all()
                print(f"\n--- All Tasks ({len(all_tasks)}) ---")
                if not all_tasks:
                    print("Your to-do list is empty.")
                for task in all_tasks:
                    print_task(task)

            elif choice == '6':
                confirm = input("Are you sure you want to delete all tasks? (y/n): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("Success: All tasks have been cleared.")
                else:
                    print("Operation cancelled.")

            elif choice == '7':
                print("Exiting application. Goodbye!")
                break

            else:
                print("Error: Invalid choice. Please select a valid option.")

        except (ValueError, TypeError, KeyError) as e:
            # Gracefully handle errors raised by the TaskManager
            print(f"Error: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
