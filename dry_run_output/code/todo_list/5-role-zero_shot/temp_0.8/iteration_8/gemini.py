
import sys
from typing import Any, Dict, List

# For Python < 3.9, use Dict and List from typing
if sys.version_info < (3, 9):
    from typing import Dict, List

# Define a type alias for a task dictionary for better readability and maintainability.
Task = Dict[str, Any]


class TaskManager:
    """
    Manages a collection of tasks in memory, adhering to high-quality standards.

    This class provides a clean, object-oriented interface for a todo list.
    It is designed for correctness, efficiency, and testability.

    Attributes:
        _tasks (dict[int, dict]): A private dictionary to store tasks.
            The key is the task ID, and the value is a dictionary
            containing task details. Using a dictionary provides O(1) average
            time complexity for lookups, insertions, and deletions by ID.
        _next_id (int): A private counter to generate unique, sequential task IDs.
    """

    def __init__(self) -> None:
        """
        Initializes the TaskManager with an empty task list.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _format_task_output(self, task_id: int, task_data: Task) -> Task:
        """
        Helper method to format a task for external representation.

        This ensures a consistent output format for all methods returning
        task details, promoting maintainability.

        Args:
            task_id: The unique identifier of the task.
            task_data: The dictionary containing the task's internal data.

        Returns:
            A dictionary including the task ID and all its details.
        """
        return {
            "id": task_id,
            "name": task_data["name"],
            "description": task_data["description"],
            "is_finished": task_data["is_finished"],
        }

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the list.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A detailed description of the task.

        Returns:
            The unique ID assigned to the newly created task.

        Raises:
            ValueError: If task_name is not a non-empty string.
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise ValueError("Task name cannot be empty.")
        if not isinstance(task_description, str):
            # Ensure description is a string for type safety.
            raise ValueError("Task description must be a string.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "name": task_name.strip(),
            "description": task_description.strip(),
            "is_finished": False,
        }
        self._next_id += 1
        return task_id

    def remove(self, task_id: int) -> bool:
        """
        Removes a task from the list by its ID.

        This operation is fault-tolerant and will not raise an error for
        non-existent IDs, instead returning a boolean status.

        Args:
            task_id: The ID of the task to remove.

        Returns:
            True if the task was successfully removed, False otherwise (e.g.,
            if the task_id does not exist).
        """
        if not isinstance(task_id, int) or task_id <= 0:
            return False  # Invalid ID format
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def search(self, search_term: str) -> List[Task]:
        """
        Searches for tasks where the search term appears in the name or description.

        The search is case-insensitive for better usability.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search criteria.
            Returns an empty list if no matches are found.

        Raises:
            ValueError: If search_term is not a non-empty string.
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise ValueError("Search term cannot be empty.")

        term_lower = search_term.lower()
        results = []
        for task_id, task_data in self._tasks.items():
            if term_lower in task_data["name"].lower() or term_lower in task_data["description"].lower():
                results.append(self._format_task_output(task_id, task_data))
        return results

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as finished.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise
            (e.g., if the task_id does not exist or task is already finished).
        """
        if not isinstance(task_id, int) or task_id <= 0:
            return False  # Invalid ID format

        task = self._tasks.get(task_id)
        if task and not task["is_finished"]:
            task["is_finished"] = True
            return True
        return False

    def get_all(self) -> List[Task]:
        """
        Retrieves all tasks currently in the list.

        Returns:
            A list of all task dictionaries. Returns an empty list if there
            are no tasks. The order of tasks is not guaranteed.
        """
        return [self._format_task_output(task_id, task_data) for task_id, task_data in self._tasks.items()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the list and resets the ID counter.

        Returns:
            True to indicate the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Demonstration of Usage ---
if __name__ == "__main__":
    # This block demonstrates how to use the TaskManager class.
    # It also serves as a basic, informal test suite.
    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # --- 1. Add Tasks ---
    print("\n--- Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task 'Buy groceries' with ID: {id1}")
        id2 = manager.add("Clean the house", "Vacuum, dust, and mop all rooms.")
        print(f"Added task 'Clean the house' with ID: {id2}")
        id3 = manager.add("Python project", "Complete the todo list application.")
        print(f"Added task 'Python project' with ID: {id3}")
        # Add a task with an empty description
        id4 = manager.add("Call mom", "")
        print(f"Added task 'Call mom' with ID: {id4}")
    except ValueError as e:
        print(f"Error: {e}")

    # --- 2. Get All Tasks ---
    print("\n--- Current Tasks ---")
    all_tasks = manager.get_all()
    if all_tasks:
        for task in all_tasks:
            print(task)
    else:
        print("No tasks in the list.")

    # --- 3. Search for a Task ---
    print("\n--- Searching for 'python' ---")
    search_results = manager.search("python")
    if search_results:
        for task in search_results:
            print(f"Found: {task}")
    else:
        print("No tasks found matching 'python'.")

    # --- 4. Finish a Task ---
    print("\n--- Finishing Task with ID 3 ---")
    success = manager.finish(3)
    print(f"Task 3 finishing status: {'Success' if success else 'Failed'}")

    # Try to finish it again
    print("--- Finishing Task with ID 3 again ---")
    success_again = manager.finish(3)
    print(f"Task 3 finishing status: {'Success' if success_again else 'Failed (already finished or does not exist)'}")

    # --- 5. View All Tasks After Update ---
    print("\n--- Current Tasks After Update ---")
    for task in manager.get_all():
        print(task)

    # --- 6. Remove a Task ---
    print("\n--- Removing Task with ID 1 ---")
    removed = manager.remove(1)
    print(f"Task 1 removal status: {'Success' if removed else 'Failed'}")

    # Try to remove a non-existent task
    print("--- Removing non-existent Task with ID 99 ---")
    removed_non_existent = manager.remove(99)
    print(f"Task 99 removal status: {'Success' if removed_non_existent else 'Failed'}")

    # --- 7. View All Tasks After Removal ---
    print("\n--- Current Tasks After Removal ---")
    for task in manager.get_all():
        print(task)

    # --- 8. Test Invalid Inputs ---
    print("\n--- Testing Invalid Inputs ---")
    try:
        manager.add("", "This should fail")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    try:
        manager.search("   ")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # --- 9. Clear All Tasks ---
    print("\n--- Clearing All Tasks ---")
    cleared = manager.clear_all()
    print(f"All tasks cleared: {cleared}")

    # --- 10. Final State ---
    print("\n--- Final Task List ---")
    final_tasks = manager.get_all()
    if not final_tasks:
        print("Task list is empty, as expected.")
    else:
        print("Error: Tasks were not cleared correctly.")

