
"""
A high-quality, maintainable implementation of a console-based Todo List Manager.

This module provides the TaskManager class, which follows best practices for
software design and adheres to the principles of the ISO/IEC 25010 standard.
"""

import dataclasses
from typing import Dict, List, Optional

# --- Data Model (Modularity, Readability) ---
# Using a dataclass provides a clear, concise, and robust way to represent
# the Task data structure. It's more readable and less error-prone than
# using raw dictionaries internally.

@dataclasses.dataclass
class Task:
    """Represents a single task in the todo list."""
    id: int
    name: str
    description: str
    is_finished: bool = False


# --- Core Application Logic (Functional Suitability, Performance) ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a clean interface to add, remove, search, and update tasks,
    ensuring data integrity and efficient operations.
    """

    def __init__(self):
        """Initializes the TaskManager with an empty task list."""
        # Using a dictionary for tasks allows for O(1) average time complexity
        # for lookups, insertions, and deletions by ID, which is highly efficient.
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, value: str, field_name: str):
        """
        Internal helper to validate string inputs. (Safety)
        
        Raises:
            TypeError: If the input is not a string.
            ValueError: If the input string is empty or only contains whitespace.
        """
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        if not value.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    def _get_task(self, task_id: int) -> Task:
        """
        Retrieves a task by its ID, handling validation and errors. (Reliability)

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            KeyError: If no task with the given ID is found.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        
        task = self._tasks.get(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found.")
        return task

    def _task_to_dict(self, task: Task) -> dict:
        """Converts a Task object to its dictionary representation. (Modularity)"""
        return {
            "id": task.id,
            "task_name": task.name,
            "task_description": task.description,
            "is_finished": task.is_finished,
        }

    # --- Public Interface (as per requirements) ---

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the new task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name or task_description are empty.
        """
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")

        new_id = self._next_id
        new_task = Task(id=new_id, name=task_name, description=task_description)
        self._tasks[new_id] = new_task
        self._next_id += 1
        return new_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.
        """
        try:
            self._get_task(task_id)  # Validate existence and ID format
            del self._tasks[task_id]
            return True
        except (TypeError, ValueError, KeyError):
            # Gracefully handle errors and return the required boolean status.
            return False

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.
        """
        try:
            task = self._get_task(task_id)
            task.is_finished = True
            return True
        except (TypeError, ValueError, KeyError):
            return False

    def search(self, search_term: str) -> List[dict]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.
        
        Raises:
            ValueError: If the search term is empty.
        """
        self._validate_string_input(search_term, "Search term")
        
        lower_term = search_term.lower()
        
        # A list comprehension is both readable and efficient for this operation.
        results = [
            self._task_to_dict(task)
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]
        return results

    def get_all(self) -> List[dict]:
        """
        Retrieves all tasks, sorted by ID.

        Returns:
            A list of all tasks (as dictionaries).
        """
        # Sorting by ID ensures a consistent and predictable output order.
        sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.id)
        return [self._task_to_dict(task) for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


# --- Example Usage (Testability, Documentation) ---
# The __main__ block demonstrates the class's functionality and serves as
# a basic, informal test suite.

if __name__ == "__main__":
    print("--- Todo List Application Demo ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n1. Adding tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"  - Added task with ID: {id1}")
        id2 = manager.add("Finish report", "Complete the Q3 financial report for the meeting.")
        print(f"  - Added task with ID: {id2}")
        id3 = manager.add("Call mom", "Wish her a happy birthday.")
        print(f"  - Added task with ID: {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    # 2. Get all tasks
    print("\n2. Current tasks:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"  - {task}")

    # 3. Finish a task
    print("\n3. Finishing task ID 2...")
    success = manager.finish(2)
    print(f"  - Operation successful: {success}")
    print("   Trying to finish a non-existent task (ID 99)...")
    success_fail = manager.finish(99)
    print(f"  - Operation successful: {success_fail}")


    # 4. Search for tasks
    print("\n4. Searching for 'report'...")
    search_results = manager.search("report")
    for task in search_results:
        print(f"  - Found: {task}")

    # 5. Remove a task
    print("\n5. Removing task ID 1...")
    removed = manager.remove(1)
    print(f"  - Operation successful: {removed}")
    print("   Trying to remove it again...")
    removed_fail = manager.remove(1)
    print(f"  - Operation successful: {removed_fail}")

    # 6. Show final list of tasks
    print("\n6. Final list of tasks:")
    final_tasks = manager.get_all()
    if final_tasks:
        for task in final_tasks:
            print(f"  - {task}")
    else:
        print("  - No tasks left.")

    # 7. Demonstrate error handling for adding
    print("\n7. Trying to add a task with invalid input...")
    try:
        manager.add("", "This should fail.")
    except ValueError as e:
        print(f"  - Caught expected error: {e}")

    # 8. Clear all tasks
    print("\n8. Clearing all tasks...")
    cleared = manager.clear_all()
    print(f"  - Operation successful: {cleared}")
    print("   Final list after clearing:")
    print(f"  - {manager.get_all()}")

    print("\n--- Demo Finished ---")

