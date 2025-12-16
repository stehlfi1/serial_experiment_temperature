
"""
A module for managing a collection of tasks in memory.

This module provides the TaskManager class, which offers a clean, efficient,
and robust interface for a todo list application, adhering to high-quality
software standards.
"""

from __future__ import annotations
import threading
from typing import List, Dict, Any, Union

# --- Custom Exceptions for Domain-Specific Errors ---
# This improves Fault Tolerance and Maintainability by providing clear,
# specific error types that can be handled by the client code.

class TaskError(Exception):
    """Base exception for errors related to task management."""
    pass

class TaskNotFound(TaskError):
    """Raised when a task with a specific ID is not found."""
    def __init__(self, task_id: int):
        super().__init__(f"Error: Task with ID '{task_id}' not found.")
        self.task_id = task_id

class InvalidTaskData(TaskError, ValueError):
    """Raised when provided task data (e.g., name) is invalid."""
    pass


# --- Type Definition for a Task ---
# Using a type alias improves Readability and Maintainability. It provides a
# single source of truth for the structure of a task dictionary.
Task = Dict[str, Union[int, str, bool]]


class TaskManager:
    """
    Manages a collection of tasks in-memory with thread-safe operations.

    This class provides a complete interface for adding, removing, searching,
    and updating tasks. It is designed for correctness, efficiency, and safety.

    Attributes:
        _tasks (Dict[int, Task]): A dictionary to store tasks, keyed by task ID.
                                  This provides O(1) average time complexity for
                                  lookups, insertions, and deletions.
        _next_id (int): An auto-incrementing counter for generating unique task IDs.
        _lock (threading.Lock): A lock to ensure thread safety for all operations
                                modifying the internal state, ensuring data integrity
                                in concurrent environments (Reliability).
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        # A lock is used to make the class thread-safe, a key aspect of
        # Reliability in concurrent applications.
        self._lock = threading.Lock()

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description for the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            InvalidTaskData: If task_name is empty or not a string.
        """
        # --- Input Validation (Security & Correctness) ---
        if not isinstance(task_name, str) or not task_name.strip():
            raise InvalidTaskData("Task name cannot be empty.")
        if not isinstance(task_description, str):
            raise InvalidTaskData("Task description must be a string.")

        with self._lock:
            task_id = self._next_id
            self._tasks[task_id] = {
                'id': task_id,
                'name': task_name.strip(),
                'description': task_description,
                'is_finished': False
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
            TaskNotFound: If no task with the given ID exists.
            ValueError: If the task_id is not a positive integer.
        """
        self._validate_id(task_id)
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFound(task_id)
            del self._tasks[task_id]
            return True

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks by a search term in their name or description.
        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries matching the search term. An empty
            list is returned if no matches are found or the term is empty.
        
        Raises:
            InvalidTaskData: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise InvalidTaskData("Search term must be a string.")
            
        if not search_term.strip():
            return []

        term_lower = search_term.lower()
        with self._lock:
            # List comprehension is a Pythonic and performant way to filter.
            # Time complexity is O(n), which is optimal for this operation.
            return [
                task for task in self._tasks.values()
                if term_lower in task['name'].lower() or \
                   term_lower in task['description'].lower()
            ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TaskNotFound: If no task with the given ID exists.
            ValueError: If the task_id is not a positive integer.
        """
        self._validate_id(task_id)
        with self._lock:
            if task_id not in self._tasks:
                raise TaskNotFound(task_id)
            
            # Avoid re-finishing an already finished task, though not strictly required.
            if self._tasks[task_id]['is_finished']:
                # Optionally, you could raise an error or return False here.
                # For idempotency, we'll allow it and return True.
                pass

            self._tasks[task_id]['is_finished'] = True
            return True

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all task dictionaries. Returns a copy to prevent
            unintended modification of the internal state (Encapsulation).
        """
        with self._lock:
            # Returning a list of values ensures O(n) performance.
            # list() creates a shallow copy, preserving encapsulation.
            return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            True upon successful deletion.
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1
            return True

    def _validate_id(self, task_id: Any) -> None:
        """
        Internal helper for ID validation. (Modularity & Reusability)
        
        Raises:
            ValueError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")


# --- Example Usage (Demonstration & Testability) ---
# This block demonstrates how to use the TaskManager class and also serves as
# a basic, runnable smoke test. This improves Testability and Usability for
# other developers.
if __name__ == "__main__":
    def print_tasks(tasks: List[Task]):
        """Helper function to pretty-print a list of tasks."""
        if not tasks:
            print("No tasks to display.")
            return
        for task in tasks:
            status = "Finished" if task['is_finished'] else "Pending"
            print(
                f"  ID: {task['id']}, Name: {task['name']}, "
                f"Desc: '{task['description']}', Status: {status}"
            )
        print("-" * 20)

    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n--- Adding Tasks ---")
    try:
        id1 = manager.add("Implement feature A", "Core logic for feature A")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Write documentation", "Document the new TaskManager class")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Create unit tests", "Write tests for the TaskManager")
        print(f"Added task with ID: {id3}")
    except TaskError as e:
        print(e)
    
    print("\n--- All Tasks ---")
    print_tasks(manager.get_all())

    print("\n--- Finishing a Task (ID 2) ---")
    try:
        manager.finish(id2)
        print("Task 2 marked as finished.")
    except TaskError as e:
        print(e)

    print("\n--- All Tasks After Finishing ---")
    print_tasks(manager.get_all())
    
    print("\n--- Searching for 'task' ---")
    results = manager.search("task")
    print("Search results:")
    print_tasks(results)
    
    print("\n--- Searching for 'documentation' ---")
    results = manager.search("documentation")
    print("Search results:")
    print_tasks(results)

    print("\n--- Removing a Task (ID 1) ---")
    try:
        manager.remove(id1)
        print("Task 1 removed.")
    except TaskError as e:
        print(e)

    print("\n--- All Tasks After Removal ---")
    print_tasks(manager.get_all())
    
    print("\n--- Handling Errors: Removing a non-existent task (ID 99) ---")
    try:
        manager.remove(99)
    except TaskNotFound as e:
        print(f"Caught expected error: {e}")

    print("\n--- Handling Errors: Adding task with invalid name ---")
    try:
        manager.add("", "This should fail.")
    except InvalidTaskData as e:
        print(f"Caught expected error: {e}")

    print("\n--- Clearing All Tasks ---")
    manager.clear_all()
    print("All tasks have been cleared.")
    
    print("\n--- All Tasks After Clearing ---")
    print_tasks(manager.get_all())
