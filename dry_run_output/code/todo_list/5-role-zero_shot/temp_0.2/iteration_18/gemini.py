
"""
A high-quality, maintainable, and efficient in-memory Todo list manager.

This module provides a TaskManager class that adheres to the principles of
ISO/IEC 25010, focusing on reliability, performance, and maintainability.
"""

from __future__ import annotations
import typing

# --- Custom Exceptions for Clear Error Handling ---
# Improves Reliability and Maintainability by providing specific error types.

class TaskError(Exception):
    """Base exception for task-related errors."""
    pass

class TaskNotFoundError(TaskError):
    """Exception raised when a task with a given ID is not found."""
    def __init__(self, task_id: int):
        super().__init__(f"Error: Task with ID '{task_id}' not found.")
        self.task_id = task_id

class InvalidTaskDataError(TaskError):
    """Exception raised for invalid task data, such as empty strings."""
    def __init__(self, message: str):
        super().__init__(f"Error: Invalid task data provided. {message}")


# --- Data Transfer Object (DTO) ---
# Using a TypedDict for clear, structured data representation.
# This improves Readability and Correctness.

class Task(typing.TypedDict):
    """Represents the structure of a task."""
    id: int
    name: str
    description: str
    is_finished: bool


class TaskManager:
    """
    Manages a collection of tasks in-memory.

    This class provides a complete interface for adding, removing, searching,
    and managing tasks, ensuring data integrity and efficient operations.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        The internal data structure is a dictionary for efficient O(1) lookups.
        _tasks: Stores task objects, keyed by their unique ID.
        _next_id: A counter to ensure unique and sequential task IDs.
        """
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description for the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            InvalidTaskDataError: If task_name is empty or not a string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise InvalidTaskDataError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            raise InvalidTaskDataError("Task description must be a string.")

        task_id = self._next_id
        new_task: Task = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False,
        }
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
            TaskNotFoundError: If no task with the given ID exists.
            InvalidTaskDataError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskDataError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> list[Task]:
        """
        Searches for tasks by a case-insensitive term in their name or description.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks that match the search term. The list is empty
            if no matches are found.

        Raises:
            InvalidTaskDataError: If search_term is empty or not a string.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise InvalidTaskDataError("Search term cannot be empty.")

        lower_term = search_term.lower()
        return [
            task.copy() for task in self._tasks.values()
            if lower_term in task["name"].lower() or \
               lower_term in task["description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TaskNotFoundError: If no task with the given ID exists.
            InvalidTaskDataError: If task_id is not a positive integer.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise InvalidTaskDataError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        self._tasks[task_id]["is_finished"] = True
        return True

    def get_all(self) -> list[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks. Returns a copy to prevent external modification
            of the internal state, ensuring data integrity.
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True upon successful clearing of all tasks.
        """
        self._tasks.clear()
        # Optionally reset the ID counter if you want fresh IDs after a clear
        # self._next_id = 1
        return True


# --- Example Usage (Demonstration & Basic Integration Test) ---
# This block demonstrates how to use the TaskManager class and also serves
# as a simple, runnable test of its functionality.

if __name__ == "__main__":
    print("--- Todo List App Demo ---")
    manager = TaskManager()

    try:
        # 1. Add tasks
        print("\n1. Adding tasks...")
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        id2 = manager.add("Finish report", "Complete the Q3 financial report.")
        id3 = manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")

        # 2. Get all tasks
        print("\n2. Current tasks:")
        all_tasks = manager.get_all()
        for task in all_tasks:
            print(f"  - {task}")

        # 3. Finish a task
        print(f"\n3. Finishing task with ID {id2}...")
        manager.finish(id2)
        print("Task finished successfully.")

        # 4. Search for tasks
        print("\n4. Searching for tasks containing 'report':")
        search_results = manager.search("report")
        for task in search_results:
            print(f"  - Found: {task}")

        # 5. Remove a task
        print(f"\n5. Removing task with ID {id1}...")
        manager.remove(id1)
        print("Task removed successfully.")

        # 6. Get all tasks again to see changes
        print("\n6. Current tasks after modifications:")
        all_tasks = manager.get_all()
        if not all_tasks:
            print("  - No tasks remaining.")
        for task in all_tasks:
            print(f"  - {task}")

        # 7. Demonstrate error handling
        print("\n7. Demonstrating error handling...")
        try:
            manager.remove(999)
        except TaskNotFoundError as e:
            print(f"  - Correctly caught expected error: {e}")

        try:
            manager.add("", "This should fail")
        except InvalidTaskDataError as e:
            print(f"  - Correctly caught expected error: {e}")

        # 8. Clear all tasks
        print("\n8. Clearing all tasks...")
        manager.clear_all()
        print("All tasks cleared.")
        print("Final task list:", manager.get_all())

    except TaskError as e:
        print(f"\nAn unexpected error occurred: {e}")

