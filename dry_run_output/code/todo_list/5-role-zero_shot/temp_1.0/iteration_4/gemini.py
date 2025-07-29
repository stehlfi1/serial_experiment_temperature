
"""
A high-quality, maintainable implementation of a console-based Todo List Manager.

This module provides the TaskManager class, which adheres to the principles of
the ISO/IEC 25010 standard for software quality.
"""

import sys
from dataclasses import dataclass
from typing import Dict, List, Union

# Define a type alias for the dictionary representation of a task
TaskDict = Dict[str, Union[int, str, bool]]


@dataclass
class Task:
    """
    Represents a single task in the todo list.

    This data class encapsulates the attributes of a task, promoting
    code readability and type safety.

    Attributes:
        id (int): A unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> TaskDict:
        """Converts the Task object to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "is_finished": self.is_finished,
        }


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface for adding, removing, searching,
    and modifying tasks. It is designed for efficiency, reliability, and
    maintainability.

    Core Data Structure:
        A dictionary (_tasks) is used for storing tasks, mapping task IDs
        to Task objects. This allows for O(1) average time complexity for
        ID-based lookups, insertions, and deletions, ensuring high performance
        efficiency.
    """

    def __init__(self):
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is not a valid, existing task ID.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Cannot be empty.
            task_description: A description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            ValueError: If task_name is empty or consists only of whitespace.
            TypeError: If inputs are not strings.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        task_id = self._next_id
        new_task = Task(
            id=task_id,
            name=task_name.strip(),
            description=task_description.strip()
        )
        self._tasks[task_id] = new_task
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task by its ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If the task ID does not exist.
        """
        self._validate_task_id(task_id)
        del self._tasks[task_id]
        return True

    def search(self, search_term: str) -> List[TaskDict]:
        """
        Searches for tasks by a search term in the name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of tasks (as dictionaries) that match the search term.
            Returns an empty list if no matches are found.

        Raises:
            ValueError: If search_term is empty or consists only of whitespace.
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")
        if not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        normalized_term = search_term.lower()
        
        # Using a generator expression within the list constructor for efficiency
        return [
            task.to_dict() for task in self._tasks.values()
            if normalized_term in task.name.lower() or \
               normalized_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task's status was set to finished.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If the task ID does not exist.
        """
        self._validate_task_id(task_id)
        task = self._tasks[task_id]
        
        # This operation is idempotent: finishing an already finished task
        # succeeds without changing the state.
        task.is_finished = True
        return True

    def get_all(self) -> List[TaskDict]:
        """
        Retrieves all tasks.

        Returns:
            A list of all tasks (as dictionaries), sorted by ID.
        """
        # Sort by ID for consistent and predictable ordering
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [task.to_dict() for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        # Resetting the ID counter makes the state clean, as if new.
        self._next_id = 1
        return True


# --- Example Usage ---
def main():
    """
    A simple demonstration of the TaskManager functionality.
    This function showcases how to use the TaskManager class and handle
    potential errors gracefully.
    """
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n1. Adding new tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"- Added task with ID: {id1}")
        id2 = manager.add("Submit Project Report", "Final report for Q2")
        print(f"- Added task with ID: {id2}")
        id3 = manager.add("Call the client", "Discuss project updates")
        print(f"- Added task with ID: {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}", file=sys.stderr)

    print("\n2. Getting all tasks:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"- {task}")

    print("\n3. Finishing a task...")
    try:
        manager.finish(id2)
        print(f"- Marked task {id2} as finished.")
    except (ValueError, TypeError) as e:
        print(f"Error finishing task: {e}", file=sys.stderr)

    print("\n4. Removing a task...")
    try:
        manager.remove(id1)
        print(f"- Removed task {id1}.")
    except (ValueError, TypeError) as e:
        print(f"Error removing task: {e}", file=sys.stderr)

    print("\n5. Searching for tasks containing 'project':")
    search_results = manager.search("project")
    if search_results:
        for task in search_results:
            print(f"- Found: {task}")
    else:
        print("- No tasks found matching 'project'.")

    print("\n6. Current state of all tasks:")
    all_tasks = manager.get_all()
    for task in all_tasks:
        print(f"- {task}")
        
    print("\n7. Demonstrating Error Handling (removing non-existent task):")
    try:
        manager.remove(999)
    except ValueError as e:
        print(f"- Caught expected error: {e}")

    print("\n8. Clearing all tasks...")
    manager.clear_all()
    print("- All tasks have been cleared.")

    print("\n9. Final state:")
    all_tasks = manager.get_all()
    if not all_tasks:
        print("- Task list is empty.")
    else:
        for task in all_tasks:
            print(f"- {task}")


if __name__ == "__main__":
    main()
