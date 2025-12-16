
"""
Module for managing a collection of tasks in memory.

This module provides the TaskManager class, which offers a clean, efficient,
and robust interface for creating, retrieving, updating, and deleting tasks.
It is designed with the principles of the ISO/IEC 25010 standard in mind,
prioritizing reliability, performance efficiency, and maintainability.
"""

import dataclasses
from typing import Dict, List, Any, Optional

# Using a dataclass to represent a task provides type safety, immutability
# benefits (if frozen=True), and boilerplate reduction. It enhances
# maintainability and readability.
@dataclasses.dataclass
class Task:
    """Represents a single task item."""
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Task object to a dictionary."""
        return dataclasses.asdict(self)


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides the core functionality for a todo list application,
    including adding, removing, searching, and modifying tasks.

    Attributes:
        _tasks (Dict[int, Task]): A private dictionary to store tasks.
            Using a dictionary provides O(1) average time complexity for
            lookups, insertions, and deletions by task ID, ensuring high
*           performance efficiency.
        _next_id (int): A private counter to generate unique task IDs.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID of the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
        """
        # Safety and Reliability: Input validation protects against invalid data.
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty.")

        # Correctness: Ensures each task has a unique, sequential ID.
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
        Removes a task by its unique ID.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        # Reliability: Gracefully handles requests for non-existent tasks.
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks by name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for in task names and descriptions.

        Returns:
            A list of dictionaries, where each dictionary represents a
            matching task. Returns an empty list if no matches are found.

        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        lower_term = search_term.lower()
        
        # Performance Efficiency: This is an O(n) operation, which is
        # optimal for this type of search without a more complex indexing
        # system. A list comprehension is a Pythonic and efficient way to build
        # the result list.
        return [
            task.to_dict() for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries, where each dictionary represents a task.
        """
        # Modularity: The conversion to a dictionary is handled by the Task
        # class itself, adhering to the Single Responsibility Principle.
        return [task.to_dict() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Example Usage ---
# This block demonstrates how to use the TaskManager class and serves as a
# basic functional test. It showcases the public API and expected outputs.
# Testability: The class can be easily instantiated and its methods tested
# in isolation, as shown here.
if __name__ == "__main__":
    print("--- Senior Developer's Todo List App ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n1. Adding tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        id2 = manager.add("Finish report", "Complete the Q3 financial report.")
        id3 = manager.add("Call mom", "Check in and see how she's doing.")
        print(f"Added task with ID: {id1}")
        print(f"Added task with ID: {id2}")
        print(f"Added task with ID: {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    # 2. Get all tasks
    print("\n2. Current tasks:")
    all_tasks = manager.get_all()
    for t in all_tasks:
        print(f"  - {t}")

    # 3. Finish a task
    print("\n3. Finishing task 2...")
    success = manager.finish(id2)
    print(f"  - Operation successful: {success}")
    print("   Attempting to finish a non-existent task (ID 99)...")
    success_fail = manager.finish(99)
    print(f"  - Operation successful: {success_fail}")


    # 4. Search for tasks
    print("\n4. Searching for 'report'...")
    report_tasks = manager.search("report")
    print(f"  - Found {len(report_tasks)} matching task(s):")
    for t in report_tasks:
        print(f"    - {t}")

    # 5. Remove a task
    print("\n5. Removing task 1...")
    removed = manager.remove(id1)
    print(f"  - Operation successful: {removed}")
    print("   Attempting to remove it again...")
    removed_fail = manager.remove(id1)
    print(f"  - Operation successful: {removed_fail}")

    # 6. Get all tasks again to see the final state
    print("\n6. Final list of tasks:")
    final_tasks = manager.get_all()
    for t in final_tasks:
        print(f"  - {t}")

    # 7. Test validation
    print("\n7. Testing input validation...")
    try:
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"  - Correctly caught error: {e}")
    try:
        manager.remove("abc") # type: ignore
    except TypeError as e:
        print(f"  - Correctly caught error: {e}")

    # 8. Clear all tasks
    print("\n8. Clearing all tasks...")
    cleared = manager.clear_all()
    print(f"  - Operation successful: {cleared}")
    print(f"  - Number of tasks after clearing: {len(manager.get_all())}")
