
"""
This module provides a TaskManager class for a console-based todo list application.

It adheres to high-quality code standards, focusing on maintainability, efficiency,
and robustness as outlined by ISO/IEC 25010.
"""

from typing import Any, Dict, List

# Define a type alias for a task dictionary for better readability and maintenance.
Task = Dict[str, Any]


class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a clean interface to add, remove, search, and update tasks,
    ensuring data integrity and efficient operations.

    Attributes:
        _tasks (Dict[int, Task]): A dictionary to store tasks, mapping task ID to task data.
        _next_id (int): A counter to generate unique IDs for new tasks.
    """

    def __init__(self) -> None:
        """Initializes the TaskManager with an empty task list."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_string_input(self, value: str, field_name: str) -> str:
        """
        Validates that a given input is a non-empty string.

        Args:
            value: The input value to validate.
            field_name: The name of the field being validated (for error messages).

        Returns:
            The validated, stripped string.

        Raises:
            TypeError: If the value is not a string.
            ValueError: If the value is an empty or whitespace-only string.
        """
        if not isinstance(value, str):
            raise TypeError(f"{field_name} must be a string.")
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError(f"{field_name} cannot be empty or just whitespace.")
        return stripped_value

    def _validate_task_id(self, task_id: int) -> None:
        """
        Validates that a task ID is a valid integer and exists.

        Args:
            task_id: The ID of the task to validate.

        Raises:
            TypeError: If the task_id is not an integer.
            ValueError: If the task_id does not exist in the task list.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
        if task_id not in self._tasks:
            raise ValueError(f"Task with ID {task_id} not found.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Cannot be empty.
            task_description: A description of the task.

        Returns:
            The unique ID assigned to the new task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is empty or whitespace.
        """
        validated_name = self._validate_string_input(task_name, "Task name")
        validated_desc = self._validate_string_input(task_description, "Task description")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "task_name": validated_name,
            "task_description": validated_desc,
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
            True if the task was successfully removed, False otherwise.
        
        Raises:
            TypeError: If the task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")
            
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks where the search term appears in the name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search criteria.

        Raises:
            TypeError: If search_term is not a string.
            ValueError: If search_term is empty or whitespace.
        """
        validated_term = self._validate_string_input(search_term, "Search term").lower()

        return [
            task
            for task in self._tasks.values()
            if validated_term in task["task_name"].lower()
            or validated_term in task["task_description"].lower()
        ]

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was found and marked as finished, False otherwise.
            
        Raises:
            TypeError: If the task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

        task = self._tasks.get(task_id)
        if task:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Task]:
        """

        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. Returns a copy to prevent
            external modification of the internal task list.
        """
        return list(self._tasks.values())

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


if __name__ == "__main__":
    # This block demonstrates the usage of the TaskManager class.
    # It serves as a basic, informal test and usage example.

    def print_tasks(tasks: List[Task]):
        """Helper function to print a list of tasks."""
        if not tasks:
            print("No tasks found.")
            return
        for task in tasks:
            status = "Finished" if task["is_finished"] else "Pending"
            print(
                f"ID: {task['id']}, Name: {task['task_name']}, "
                f"Desc: {task['task_description']}, Status: {status}"
            )
        print("-" * 20)

    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    print("\n--- Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Code review", "Review the new feature branch")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Plan weekend trip", "Research destinations and book hotel")
        print(f"Added task with ID: {id3}")
        # Example of invalid input
        # manager.add("  ", "This will fail")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    print("\n--- All Tasks ---")
    print_tasks(manager.get_all())

    print("\n--- Finishing a Task (ID 2) ---")
    if manager.finish(2):
        print("Task 2 marked as finished.")
    else:
        print("Failed to finish task 2.")
    print_tasks(manager.get_all())

    print("\n--- Searching for 'review' ---")
    results = manager.search("review")
    print_tasks(results)
    
    print("\n--- Searching for 'book' ---")
    results = manager.search("book")
    print_tasks(results)

    print("\n--- Removing a Task (ID 1) ---")
    if manager.remove(1):
        print("Task 1 removed.")
    else:
        print("Failed to remove task 1.")
    print_tasks(manager.get_all())
    
    print("\n--- Attempting to remove non-existent task (ID 99) ---")
    if not manager.remove(99):
        print("Task 99 not found, as expected.")

    print("\n--- Clearing All Tasks ---")
    manager.clear_all()
    print("All tasks cleared.")
    print_tasks(manager.get_all())
