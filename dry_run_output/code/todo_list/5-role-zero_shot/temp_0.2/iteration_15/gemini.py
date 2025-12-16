
"""
Module for managing a collection of tasks in memory.

This module provides a TaskManager class that offers a complete interface for
a todo list application, including adding, removing, searching, and updating tasks.
It is designed for high performance and maintainability.
"""

import dataclasses
from typing import Dict, List, Any

# For Python < 3.9, use typing.List and typing.Dict instead of list and dict
# in type hints within the class.


@dataclasses.dataclass
class Task:
    """
    Represents a single task in the todo list.

    Using a dataclass provides type safety, automatic __init__ and __repr__,
    and a clear, structured way to handle task data.

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name or title of the task.
        description (str): A detailed description of the task.
        is_finished (bool): The completion status of the task.
    """
    id: int
    name: str
    description: str
    is_finished: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Task object to a dictionary."""
        return dataclasses.asdict(self)


class TaskManager:
    """

    Manages a collection of tasks, providing an OOP interface for a todo list.

    This class handles all logic for creating, retrieving, updating, and deleting
    tasks. It stores tasks in-memory using an efficient dictionary-based structure
    for rapid access.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager.

        It sets up an in-memory data store for tasks and a counter for
        generating unique task IDs.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, input_str: str, field_name: str) -> None:
        """
        Internal helper to validate that a string input is not empty.

        Args:
            input_str: The string to validate.
            field_name: The name of the field being validated (for error messages).

        Raises:
            TypeError: If the input is not a string.
            ValueError: If the input string is empty or only whitespace.
        """
        if not isinstance(input_str, str):
            raise TypeError(f"{field_name} must be a string.")
        if not input_str.strip():
            raise ValueError(f"{field_name} cannot be empty or just whitespace.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name/title of the task.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name or task_description are empty.
        """
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")

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
            True if the task was found and removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is a non-positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """
        Searches for tasks where the name or description contains the search term.

        The search is case-insensitive.

        Args:
            search_term: The string to search for within task names and descriptions.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task.
            Returns an empty list if no matches are found.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is empty.
        """
        self._validate_string_input(search_term, "Search term")
        lower_term = search_term.lower()

        return [
            task.to_dict() for task in self._tasks.values()
            if lower_term in task.name.lower() or lower_term in task.description.lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
            ValueError: If task_id is a non-positive integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")

        task = self._tasks.get(task_id)
        if task:
            task.is_finished = True
            return True
        return False

    def get_all(self) -> List[Dict[str, Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list of dictionaries representing all tasks. The list is sorted by task ID.
        """
        # Sorting by ID provides a consistent and predictable order.
        sorted_tasks = sorted(self._tasks.values(), key=lambda t: t.id)
        return [task.to_dict() for task in sorted_tasks]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1  # Reset the ID counter
        return True


# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates how to use the TaskManager class.
    # It serves as a basic, interactive console client.

    def print_tasks(tasks: List[Dict[str, Any]]):
        """Helper function to print a list of tasks."""
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            status = "Finished" if task['is_finished'] else "Pending"
            print(
                f"ID: {task['id']} | Name: {task['name']} | "
                f"Description: {task['description']} | Status: {status}"
            )

    print("--- Task Manager Console Demo ---")
    manager = TaskManager()

    # Add tasks
    print("\n1. Adding tasks...")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        id2 = manager.add("Code review", "Review the new feature branch for project X.")
        id3 = manager.add("Clean the house", "Vacuum and dust all rooms.")
        print(f"Added tasks with IDs: {id1}, {id2}, {id3}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    # Get all tasks
    print("\n2. Listing all tasks:")
    all_tasks = manager.get_all()
    print_tasks(all_tasks)

    # Finish a task
    print("\n3. Marking task 2 as finished...")
    if manager.finish(2):
        print("Task 2 marked as finished.")
    else:
        print("Task 2 not found.")

    # Search for tasks
    print("\n4. Searching for tasks containing 'review':")
    search_results = manager.search("review")
    print_tasks(search_results)

    # Remove a task
    print("\n5. Removing task 3...")
    if manager.remove(3):
        print("Task 3 removed successfully.")
    else:
        print("Task 3 not found.")

    # List all tasks again
    print("\n6. Listing all tasks after updates:")
    all_tasks = manager.get_all()
    print_tasks(all_tasks)

    # Demonstrate error handling
    print("\n7. Demonstrating error handling...")
    try:
        manager.add("", "This will fail")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        manager.remove(-5)
    except ValueError as e:
        print(f"Caught expected error: {e}")

    if not manager.remove(999):
        print("Caught expected result: Cannot remove non-existent task 999.")

    # Clear all tasks
    print("\n8. Clearing all tasks...")
    manager.clear_all()
    print("All tasks have been cleared.")

    # Final list
    print("\n9. Final task list:")
    print_tasks(manager.get_all())
