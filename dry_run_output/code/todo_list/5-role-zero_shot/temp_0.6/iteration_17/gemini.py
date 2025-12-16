
"""
A module for managing a collection of tasks in memory.

This module provides the TaskManager class, which offers a clean, high-level API
for creating, retrieving, updating, and deleting tasks. It is designed for
reliability, efficiency, and maintainability.
"""

import dataclasses
from typing import Dict, List, Any

# Using a dataclass for a structured, readable, and type-safe way to hold task data.
# frozen=True makes instances of the class immutable, which prevents accidental
# modification of task objects outside the TaskManager's control methods.
# When a task needs to be changed (e.g., finished), a new instance is created.
@dataclasses.dataclass(frozen=True)
class Task:
    """Represents a single, immutable task item."""
    id: int
    name: str
    description: str
    is_finished: bool = False


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface for a todo list application,
    including adding, removing, searching, and modifying tasks. It is designed
    to be self-contained and easily testable.

    Attributes:
        _tasks (Dict[int, Task]): A private dictionary to store tasks, mapping task IDs to Task objects.
        _next_id (int): A private counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _task_to_dict(self, task: Task) -> Dict[str, Any]:
        """
        Converts a Task object to a dictionary.
        
        This helper ensures a consistent output format for all public methods.
        """
        return dataclasses.asdict(task)

    def _validate_task_exists(self, task_id: int) -> None:
        """
        Private helper to check if a task ID exists.

        Args:
            task_id: The ID of the task to validate.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description for the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name is empty or not a string.
            TypeError: If inputs are not of type string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        new_task = Task(id=task_id, name=task_name.strip(), description=task_description)
        self._tasks[task_id] = new_task
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
            KeyError: If the task_id does not exist.
        """
        self._validate_task_exists(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a search term in the name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.
        
        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
            
        lower_term = search_term.lower()
        
        # Using a list comprehension for a concise and efficient search.
        return [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        This method is idempotent; finishing an already finished task has no effect
        and still returns True.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the operation was successful.

        Raises:
            TypeError: If task_id is not an integer.
            KeyError: If the task_id does not exist.
        """
        self._validate_task_exists(task_id)
        
        task_to_finish = self._tasks[task_id]
        if not task_to_finish.is_finished:
            # Create a new, updated Task object to replace the old one.
            # This respects the immutability of the Task dataclass.
            finished_task = Task(
                id=task_to_finish.id,
                name=task_to_finish.name,
                description=task_to_finish.description,
                is_finished=True
            )
            self._tasks[task_id] = finished_task
            
        return True

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries representing all tasks, sorted by ID.
        """
        # Sorting by ID provides a consistent and predictable order.
        sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.id)
        return [self._task_to_dict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        This operation is irreversible.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


# --- Example Usage ---
def print_tasks(tasks: List[Dict[str, Any]]):
    """Helper function to neatly print a list of tasks."""
    if not tasks:
        print("No tasks to show.")
        return
    for task in tasks:
        status = "✓" if task['is_finished'] else "✗"
        print(
            f"[{status}] ID: {task['id']} | Name: {task['task_name']} | "
            f"Desc: {task['task_description']}"
        )

if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It acts as a simple command-line interface and a functional demonstration.
    
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n--- Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Code review", "Review the new feature branch for project X.")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Plan weekend trip", "Look up destinations and book a hotel.")
        print(f"Added task with ID: {id3}")
        # Example of invalid input
        # manager.add("", "This will fail")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    print("\n--- Current Tasks ---")
    print_tasks(manager.get_all())

    print("\n--- Finishing a Task (ID 2) ---")
    try:
        manager.finish(2)
        print("Task 2 marked as finished.")
    except (KeyError, TypeError) as e:
        print(f"Error: {e}")

    print("\n--- Current Tasks After Update ---")
    print_tasks(manager.get_all())

    print("\n--- Searching for 'trip' ---")
    results = manager.search("trip")
    print_tasks(results)

    print("\n--- Searching for 'project' ---")
    results = manager.search("project")
    print_tasks(results)

    print("\n--- Removing a Task (ID 1) ---")
    try:
        manager.remove(1)
        print("Task 1 removed.")
    except (KeyError, TypeError) as e:
        print(f"Error: {e}")

    print("\n--- Current Tasks After Removal ---")
    print_tasks(manager.get_all())

    print("\n--- Attempting to remove non-existent task (ID 99) ---")
    try:
        manager.remove(99)
    except KeyError as e:
        print(f"Caught expected error: {e}")

    print("\n--- Clearing All Tasks ---")
    manager.clear_all()
    print("All tasks have been cleared.")

    print("\n--- Final Task List ---")
    print_tasks(manager.get_all())
