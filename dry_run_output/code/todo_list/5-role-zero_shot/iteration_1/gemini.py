
import uuid

class TaskManager:
    """
    Manages a collection of tasks, providing functionalities to add, remove, search,
    finish, retrieve, and clear tasks. Adheres to ISO/IEC 25010 principles for
    software quality, focusing on functional suitability, performance efficiency,
    usability, reliability, security, maintainability, and portability.
    """

    def __init__(self):
        """
        Initializes the TaskManager with an empty dictionary to store tasks.
        Each task is stored as a dictionary with keys:
        'name', 'description', and 'is_finished'.
        """
        self._tasks: dict[int, dict] = {}
        self._next_id: int = 1

    def _validate_task_id(self, task_id: int) -> None:
        """
        Internal helper to validate a task ID.

        Args:
            task_id: The ID of the task to validate.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If task_id does not exist.
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise ValueError("Task ID must be a positive integer.")
        if task_id not in self._tasks:
            raise KeyError(f"Task with ID {task_id} not found.")

    def _validate_string_input(self, input_string: str, field_name: str) -> None:
        """
        Internal helper to validate string inputs.

        Args:
            input_string: The string to validate.
            field_name: The name of the field being validated (for error messages).

        Raises:
            ValueError: If the input_string is empty or not a string.
        """
        if not isinstance(input_string, str) or not input_string.strip():
            raise ValueError(f"{field_name} cannot be empty.")

    def add(self, task_name: str, task_description: str) -> int:
        """
        Adds a new task to the manager.

        Args:
            task_name: The name of the task.
            task_description: A description of the task.

        Returns:
            The unique ID of the newly added task.

        Raises:
            ValueError: If task_name or task_description are empty.
        """
        self._validate_string_input(task_name, "Task name")
        self._validate_string_input(task_description, "Task description")

        task_id = self._next_id
        self._tasks[task_id] = {
            "id": task_id,
            "name": task_name.strip(),
            "description": task_description.strip(),
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
            Note: This method is designed to return False on failure,
            but internal validation raises specific errors for clarity.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If task_id does not exist.
        """
        try:
            self._validate_task_id(task_id)
            del self._tasks[task_id]
            return True
        except (ValueError, KeyError):
            # For external API, return False to indicate failure if preferred,
            # but raising is generally better for debugging.
            # Here, we re-raise to indicate a more specific failure.
            raise

    def search(self, task_term: str) -> list[dict]:
        """
        Searches for tasks whose name or description contains the given term (case-insensitive).

        Args:
            task_term: The term to search for.

        Returns:
            A list of dictionaries, where each dictionary represents a matching task
            and contains all task information. An empty list if no matches are found.

        Raises:
            ValueError: If task_term is an empty string.
        """
        self._validate_string_input(task_term, "Search term")

        search_lower = task_term.strip().lower()
        matching_tasks = []
        for task in self._tasks.values():
            if (search_lower in task["name"].lower() or
                    search_lower in task["description"].lower()):
                matching_tasks.append(task.copy())  # Return a copy to prevent external modification
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Marks a task as completed.

        Args:
            task_id: The ID of the task to mark as finished.

        Returns:
            True if the task was successfully marked as finished, False otherwise.
            Note: This method is designed to return False on failure,
            but internal validation raises specific errors for clarity.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If task_id does not exist.
        """
        try:
            self._validate_task_id(task_id)
            self._tasks[task_id]["is_finished"] = True
            return True
        except (ValueError, KeyError):
            # Re-raise for specific error indication.
            raise

    def get_all(self) -> list[dict]:
        """
        Retrieves all tasks currently managed by the TaskManager.

        Returns:
            A list of dictionaries, where each dictionary represents a task
            and contains all task information. Returns an empty list if no tasks exist.
        """
        return [task.copy() for task in self._tasks.values()]

    def clear_all(self) -> bool:
        """
        Deletes all tasks from the manager.

        Returns:
            True if all tasks were successfully cleared, False otherwise.
            (Always returns True if no errors occur during deletion).
        """
        self._tasks.clear()
        self._next_id = 1  # Reset ID counter
        return True

    def get_task_details(self, task_id: int) -> dict:
        """
        Internal helper to retrieve a task's full details.

        Args:
            task_id: The ID of the task.

        Returns:
            A dictionary containing the task's details.

        Raises:
            ValueError: If task_id is not a positive integer.
            KeyError: If task_id does not exist.
        """
        self._validate_task_id(task_id)
        return self._tasks[task_id].copy()


# Example Usage (Console-based interaction)
def display_task(task: dict):
    """Formats and prints task details."""
    status = "Finished" if task.get("is_finished", False) else "Pending"
    print(f"  ID: {task['id']}")
    print(f"  Name: {task['name']}")
    print(f"  Description: {task['description']}")
    print(f"  Status: {status}")
    print("-" * 30)

def main():
    """Main function to run the console-based todo list application."""
    manager = TaskManager()

    print("Welcome to the Console Todo List App!")

    while True:
        print("\n--- Menu ---")
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Finish Task")
        print("5. Get All Tasks")
        print("6. Clear All Tasks")
        print("7. Exit")
        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = manager.add(name, description)
                print(f"Task '{name}' added with ID: {task_id}")
            elif choice == '2':
                task_id_str = input("Enter task ID to remove: ")
                task_id = int(task_id_str)
                if manager.remove(task_id):
                    print(f"Task with ID {task_id} removed successfully.")
            elif choice == '3':
                term = input("Enter search term (name or description): ")
                results = manager.search(term)
                if results:
                    print("\n--- Search Results ---")
                    for task in results:
                        display_task(task)
                else:
                    print("No tasks found matching your search term.")
            elif choice == '4':
                task_id_str = input("Enter task ID to mark as finished: ")
                task_id = int(task_id_str)
                if manager.finish(task_id):
                    print(f"Task with ID {task_id} marked as finished.")
            elif choice == '5':
                all_tasks = manager.get_all()
                if all_tasks:
                    print("\n--- All Tasks ---")
                    for task in all_tasks:
                        display_task(task)
                else:
                    print("No tasks available.")
            elif choice == '6':
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ").lower()
                if confirm == 'yes':
                    if manager.clear_all():
                        print("All tasks cleared successfully.")
                    else:
                        print("Failed to clear all tasks.") # Should ideally not happen
                else:
                    print("Operation cancelled.")
            elif choice == '7':
                print("Exiting Todo List App. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyError as e:
            print(f"Error: {e}. Please ensure the ID is correct.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
