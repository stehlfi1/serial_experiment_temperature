
"""
A module for managing a collection of tasks in memory.

This module provides a TaskManager class that implements a full CRUD
(Create, Read, Update, Delete) interface for a todo list, designed
with the ISO/IEC 25010 standard in mind.
"""

import dataclasses
from typing import List, Dict, Any, Union

# --- Custom Exceptions for Enhanced Reliability ---

class TaskNotFoundError(KeyError):
    """Raised when a task with the specified ID is not found."""
    def __init__(self, task_id: int):
        super().__init__(f"Task with ID '{task_id}' not found.")
        self.task_id = task_id

class InvalidTaskDataError(ValueError):
    """Raised when provided task data (e.g., name) is invalid."""
    pass

# --- Data Model for Modularity and Readability ---

@dataclasses.dataclass
class Task:
    """
    Represents a single task item.

    Using a dataclass provides type safety, readability, and a clear
    structure for our core data entity.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> Dict[str, Union[int, str, bool]]:
        """Converts the Task object to a dictionary for external representation."""
        return dataclasses.asdict(self)

# --- Core Logic with a Focus on Maintainability and Performance ---

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a high-level API to interact with a todo list. It is
    designed for correctness, efficiency, and safety, adhering to principles
    of high-quality software development.

    ISO/IEC 25010 Alignment:
    - Functional Suitability: Implements all required functionalities correctly.
    - Performance Efficiency: Uses a dictionary for O(1) average time complexity
      on ID-based operations.
    - Reliability: Employs robust error handling with custom, specific exceptions.
    - Security (Safety): Protects against invalid inputs through rigorous validation.
    - Maintainability: Highly modular with a separate data model (Task) and
      clear, documented methods.
    - Testability: Self-contained with no external dependencies.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Private helper to validate a task ID.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a positive integer.
            TaskNotFoundError: If no task with the given ID exists.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Cannot be empty.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            InvalidTaskDataError: If task_name is empty or just whitespace.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise InvalidTaskDataError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            raise InvalidTaskDataError("Task description must be a string.")

        task_id = self._next_id
        new_task = Task(
            id=task_id,
            name=task_name.strip(),
            description=task_description
        )
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
            TypeError, ValueError, TaskNotFoundError: See _validate_task_id.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished.

        Raises:
            TypeError, ValueError, TaskNotFoundError: See _validate_task_id.
        """
        self._validate_task_id(task_id)
        self._tasks[task_id].is_finished = True
        return True

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by a case-insensitive term in their name or description.

        Args:
            search_term: The string to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.

        Raises:
            InvalidTaskDataError: If search_term is empty or not a string.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise InvalidTaskDataError("Search term cannot be empty.")

        lower_term = search_term.lower()
        return [
            task.to_dict()
            for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
            The list is sorted by task ID.
        """
        return [self._tasks[task_id].to_dict() for task_id in sorted(self._tasks.keys())]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


if __name__ == '__main__':
    # --- Example Usage and Demonstration ---
    # This block demonstrates how to use the TaskManager class and serves as
    # a basic, informal test of its functionality.

    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    try:
        # Add tasks
        print("\n--- Adding Tasks ---")
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Finish report", "Complete the Q3 financial report for review.")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Call plumber", "Fix the leaky faucet in the kitchen.")
        print(f"Added task with ID: {id3}")

        # Get all tasks
        print("\n--- Current Tasks ---")
        all_tasks = manager.get_all()
        for task in all_tasks:
            print(task)

        # Finish a task
        print("\n--- Finishing a Task ---")
        manager.finish(id2)
        print(f"Task {id2} marked as finished.")

        # Search for tasks
        print("\n--- Searching for 'report' ---")
        search_results = manager.search("report")
        for task in search_results:
            print(task)

        # Remove a task
        print("\n--- Removing a Task ---")
        manager.remove(id3)
        print(f"Task {id3} removed.")

        # Get all tasks again to see changes
        print("\n--- Final Task List ---")
        all_tasks = manager.get_all()
        for task in all_tasks:
            print(task)

        # Demonstrate error handling
        print("\n--- Demonstrating Error Handling ---")
        try:
            manager.remove(999)
        except TaskNotFoundError as e:
            print(f"Caught expected error: {e}")

        try:
            manager.add("", "This should fail")
        except InvalidTaskDataError as e:
            print(f"Caught expected error: {e}")

        # Clear all tasks
        print("\n--- Clearing All Tasks ---")
        manager.clear_all()
        print("All tasks cleared.")
        print(f"Final task list: {manager.get_all()}")

    except (TaskNotFoundError, InvalidTaskDataError, TypeError, ValueError) as e:
        print(f"\nAn unexpected error occurred: {e}")

