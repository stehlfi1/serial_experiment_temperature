
import typing

class TaskManager:
    """
    Manages a collection of tasks in memory.

    This class provides a complete interface to add, remove, search, finish,
    and retrieve tasks, adhering to high-quality code standards. It uses a
    dictionary for efficient O(1) lookups, insertions, and deletions by ID.
    """

    def __init__(self):
        """
        Initializes the TaskManager.

        The internal data structure `_tasks` is a dictionary mapping unique
        integer IDs to task data dictionaries. `_next_id` ensures each new
        task receives a unique ID.
        """
        self._tasks: typing.Dict[int, typing.Dict[str, typing.Any]] = {}
        self._next_id: int = 1

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name of the task. Must be a non-empty string.
            task_description: A description for the task. Can be an empty string.

        Returns:
            The unique integer ID assigned to the new task.

        Raises:
            TypeError: If task_name or task_description are not strings.
            ValueError: If task_name is an empty or whitespace-only string.
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings.")
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or just whitespace.")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name,
            "description": task_description,
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
            True if the task was found and removed, False otherwise.

        Raises:
            TypeError: If task_id is not an integer.
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer.")

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
            task["is_finished"] = True
            return True
        return False

    def search(self, search_term: str) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        Searches for tasks by a search term in their name or description.

        The search is case-insensitive.

        Args:
            search_term: The string to search for.

        Returns:
            A list of task dictionaries that match the search term.
            Returns an empty list if no matches are found or the term is empty.

        Raises:
            TypeError: If search_term is not a string.
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string.")

        if not search_term.strip():
            return []

        normalized_term = search_term.lower()
        results = [
            task.copy() for task in self._tasks.values()
            if normalized_term in task["name"].lower() or \
               normalized_term in task["description"].lower()
        ]
        return results

    def get_all(self) -> typing.List[typing.Dict[str, typing.Any]]:
        """
        Retrieves all tasks.

        Returns:
            A list containing all task dictionaries. Returns a copy to prevent
            direct modification of the internal state.
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        This action is irreversible and also resets the ID counter.

        Returns:
            True, indicating the operation was successful.
        """
        self._tasks.clear()
        self._next_id = 1
        return True


# --- Example Usage ---
if __name__ == "__main__":
    # This block demonstrates the functionality of the TaskManager class.
    # It serves as a basic integration test and usage example.

    print("--- Initializing Task Manager ---")
    manager = TaskManager()

    # 1. Add tasks
    print("\n--- 1. Adding Tasks ---")
    try:
        id1 = manager.add("Buy groceries", "Milk, Bread, Cheese")
        print(f"Added task with ID: {id1}")
        id2 = manager.add("Code review", "Review PR #123 for the new feature.")
        print(f"Added task with ID: {id2}")
        id3 = manager.add("Plan weekend trip", "Look up destinations and book hotel.")
        print(f"Added task with ID: {id3}")
        # Add a task with an empty description
        id4 = manager.add("Call Mom", "")
        print(f"Added task with ID: {id4}")
    except (ValueError, TypeError) as e:
        print(f"Error adding task: {e}")

    # 2. Get all tasks
    print("\n--- 2. Getting All Tasks ---")
    all_tasks = manager.get_all()
    print("Current tasks:")
    for t in all_tasks:
        print(f"  - {t}")

    # 3. Finish a task
    print("\n--- 3. Finishing a Task ---")
    task_to_finish_id = id2
    success = manager.finish(task_to_finish_id)
    print(f"Marking task {task_to_finish_id} as finished: {'Success' if success else 'Failed'}")
    print("Tasks after finishing one:")
    for t in manager.get_all():
        print(f"  - {t}")

    # 4. Search for tasks
    print("\n--- 4. Searching for Tasks ---")
    search_results = manager.search("trip")
    print("Search results for 'trip':")
    for t in search_results:
        print(f"  - {t}")

    # 5. Remove a task
    print("\n--- 5. Removing a Task ---")
    task_to_remove_id = id1
    success = manager.remove(task_to_remove_id)
    print(f"Removing task {task_to_remove_id}: {'Success' if success else 'Failed'}")
    print("Tasks after removal:")
    for t in manager.get_all():
        print(f"  - {t}")

    # 6. Demonstrate Error Handling
    print("\n--- 6. Demonstrating Error Handling ---")
    # a) Invalid ID
    print("Attempting to remove a non-existent task (ID 999)...")
    success = manager.remove(999)
    print(f"Result: {'Success' if success else 'Failed (as expected)'}")

    # b) Invalid input type
    try:
        print("Attempting to add a task with a non-string name...")
        manager.add(12345, "This should fail")
    except TypeError as e:
        print(f"Caught expected error: {e}")
        
    # c) Invalid input value
    try:
        print("Attempting to add a task with an empty name...")
        manager.add("   ", "This should also fail")
    except ValueError as e:
        print(f"Caught expected error: {e}")

    # 7. Clear all tasks
    print("\n--- 7. Clearing All Tasks ---")
    manager.clear_all()
    print("All tasks cleared.")
    print("Final task list:", manager.get_all())
    
    # 8. Add a new task to show ID reset
    print("\n--- 8. Adding a new task after clearing ---")
    new_id = manager.add("Start fresh", "A new beginning")
    print(f"ID of the new task is {new_id} (should be 1).")
    print("Final tasks:", manager.get_all())
