
"""
Todo List Manager Application

A console-based todo list application implementing ISO/IEC 25010 quality standards.
Provides functionality to manage tasks with add, remove, search, finish, and retrieval operations.
"""

from typing import Dict, List, Optional
import logging
from dataclasses import dataclass, asdict
from threading import Lock


@dataclass
class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task
        task_name (str): Name/title of the task
        task_description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
    """
    id: int
    task_name: str
    task_description: str
    is_finished: bool = False
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary format."""
        return asdict(self)
    
    def matches_search_term(self, search_term: str) -> bool:
        """
        Check if task matches the given search term.
        
        Args:
            search_term (str): Term to search for in task name and description
            
        Returns:
            bool: True if task matches search term, False otherwise
        """
        if not search_term:
            return False
        
        search_term_lower = search_term.lower()
        return (search_term_lower in self.task_name.lower() or 
                search_term_lower in self.task_description.lower())


class TaskManager:
    """
    Manages a collection of tasks with CRUD operations.
    
    This class provides thread-safe operations for managing tasks including
    adding, removing, searching, marking as finished, and retrieving tasks.
    Implements efficient data structures for optimal performance.
    """
    
    def __init__(self):
        """Initialize TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = Lock()  # Thread safety for concurrent operations
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self._logger = logging.getLogger(__name__)
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name (str): Task name to validate
            task_description (str): Task description to validate
            
        Raises:
            ValueError: If task_name or task_description is empty or invalid
            TypeError: If inputs are not strings
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace only")
        
        if not task_description.strip():
            raise ValueError("Task description cannot be empty or whitespace only")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _task_exists(self, task_id: int) -> bool:
        """
        Check if a task exists in the storage.
        
        Args:
            task_id (int): ID of the task to check
            
        Returns:
            bool: True if task exists, False otherwise
        """
        return task_id in self._tasks
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (must not be empty)
            task_description (str): Description of the task (must not be empty)
            
        Returns:
            int: Unique ID assigned to the new task
            
        Raises:
            ValueError: If task_name or task_description is empty
            TypeError: If inputs are not strings
        """
        try:
            self._validate_task_input(task_name, task_description)
            
            with self._lock:
                task_id = self._next_id
                new_task = Task(
                    id=task_id,
                    task_name=task_name.strip(),
                    task_description=task_description.strip()
                )
                
                self._tasks[task_id] = new_task
                self._next_id += 1
                
                self._logger.info(f"Task added successfully with ID: {task_id}")
                return task_id
                
        except (ValueError, TypeError) as e:
            self._logger.error(f"Failed to add task: {e}")
            raise
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id (int): ID of the task to remove (must be positive)
            
        Returns:
            bool: True if task was successfully removed, False if task doesn't exist
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        try:
            self._validate_task_id(task_id)
            
            with self._lock:
                if self._task_exists(task_id):
                    del self._tasks[task_id]
                    self._logger.info(f"Task {task_id} removed successfully")
                    return True
                else:
                    self._logger.warning(f"Attempted to remove non-existent task: {task_id}")
                    return False
                    
        except (ValueError, TypeError) as e:
            self._logger.error(f"Failed to remove task: {e}")
            raise
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            search_term (str): Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is empty or whitespace only
        """
        try:
            if not isinstance(search_term, str):
                raise TypeError("Search term must be a string")
            
            if not search_term.strip():
                raise ValueError("Search term cannot be empty or whitespace only")
            
            search_term = search_term.strip()
            matching_tasks = []
            
            with self._lock:
                for task in self._tasks.values():
                    if task.matches_search_term(search_term):
                        matching_tasks.append(task.to_dict())
            
            self._logger.info(f"Search for '{search_term}' returned {len(matching_tasks)} results")
            return matching_tasks
            
        except (ValueError, TypeError) as e:
            self._logger.error(f"Failed to search tasks: {e}")
            raise
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task doesn't exist
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        try:
            self._validate_task_id(task_id)
            
            with self._lock:
                if self._task_exists(task_id):
                    self._tasks[task_id].is_finished = True
                    self._logger.info(f"Task {task_id} marked as finished")
                    return True
                else:
                    self._logger.warning(f"Attempted to finish non-existent task: {task_id}")
                    return False
                    
        except (ValueError, TypeError) as e:
            self._logger.error(f"Failed to finish task: {e}")
            raise
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the todo list.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, ordered by ID
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in sorted(self._tasks.values(), key=lambda t: t.id)]
        
        self._logger.info(f"Retrieved {len(all_tasks)} tasks")
        return all_tasks
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful clearing
        """
        with self._lock:
            task_count = len(self._tasks)
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
        
        self._logger.info(f"Cleared {task_count} tasks from todo list")
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks in the todo list
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_task_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


class TodoListApp:
    """
    Console-based Todo List Application.
    
    Provides a command-line interface for interacting with the TaskManager.
    """
    
    def __init__(self):
        """Initialize the Todo List Application."""
        self.task_manager = TaskManager()
        self._logger = logging.getLogger(__name__)
    
    def display_menu(self) -> None:
        """Display the main menu options."""
        print("\n" + "="*50)
        print("           TODO LIST MANAGER")
        print("="*50)
        print("1. Add Task")
        print("2. Remove Task")
        print("3. Search Tasks")
        print("4. Mark Task as Finished")
        print("5. View All Tasks")
        print("6. Clear All Tasks")
        print("7. Show Statistics")
        print("0. Exit")
        print("="*50)
    
    def add_task_interactive(self) -> None:
        """Interactive method to add a new task."""
        try:
            print("\n--- Add New Task ---")
            task_name = input("Enter task name: ").strip()
            task_description = input("Enter task description: ").strip()
            
            task_id = self.task_manager.add(task_name, task_description)
            print(f"✓ Task added successfully with ID: {task_id}")
            
        except (ValueError, TypeError) as e:
            print(f"✗ Error: {e}")
    
    def remove_task_interactive(self) -> None:
        """Interactive method to remove a task."""
        try:
            print("\n--- Remove Task ---")
            task_id = int(input("Enter task ID to remove: "))
            
            if self.task_manager.remove(task_id):
                print(f"✓ Task {task_id} removed successfully")
            else:
                print(f"✗ Task {task_id} not found")
                
        except ValueError:
            print("✗ Error: Please enter a valid task ID (number)")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def search_tasks_interactive(self) -> None:
        """Interactive method to search tasks."""
        try:
            print("\n--- Search Tasks ---")
            search_term = input("Enter search term: ").strip()
            
            results = self.task_manager.search(search_term)
            
            if results:
                print(f"\n✓ Found {len(results)} matching task(s):")
                self._display_tasks(results)
            else:
                print("✗ No tasks found matching your search term")
                
        except (ValueError, TypeError) as e:
            print(f"✗ Error: {e}")
    
    def finish_task_interactive(self) -> None:
        """Interactive method to mark a task as finished."""
        try:
            print("\n--- Mark Task as Finished ---")
            task_id = int(input("Enter task ID to mark as finished: "))
            
            if self.task_manager.finish(task_id):
                print(f"✓ Task {task_id} marked as finished")
            else:
                print(f"✗ Task {task_id} not found")
                
        except ValueError:
            print("✗ Error: Please enter a valid task ID (number)")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    def view_all_tasks(self) -> None:
        """Display all tasks."""
        print("\n--- All Tasks ---")
        tasks = self.task_manager.get_all()
        
        if tasks:
            self._display_tasks(tasks)
        else:
            print("No tasks found. Your todo list is empty!")
    
    def clear_all_tasks_interactive(self) -> None:
        """Interactive method to clear all tasks."""
        print("\n--- Clear All Tasks ---")
        confirm = input("Are you sure you want to delete ALL tasks? (yes/no): ").strip().lower()
        
        if confirm in ['yes', 'y']:
            self.task_manager.clear_all()
            print("✓ All tasks have been cleared")
        else:
            print("Operation cancelled")
    
    def show_statistics(self) -> None:
        """Display task statistics."""
        total_tasks = self.task_manager.get_task_count()
        completed_tasks = self.task_manager.get_completed_task_count()
        pending_tasks = total_tasks - completed_tasks
        
        print("\n--- Task Statistics ---")
        print(f"Total Tasks: {total_tasks}")
        print(f"Completed Tasks: {completed_tasks}")
        print(f"Pending Tasks: {pending_tasks}")
        
        if total_tasks > 0:
            completion_rate = (completed_tasks / total_tasks) * 100
            print(f"Completion Rate: {completion_rate:.1f}%")
    
    def _display_tasks(self, tasks: List[Dict]) -> None:
        """
        Display a list of tasks in a formatted manner.
        
        Args:
            tasks (List[Dict]): List of task dictionaries to display
        """
        print("\n" + "-"*80)
        print(f"{'ID':<4} {'Name':<25} {'Description':<35} {'Status':<10}")
        print("-"*80)
        
        for task in tasks:
            status = "✓ Done" if task['is_finished'] else "○ Pending"
            name = task['task_name'][:24] + "..." if len(task['task_name']) > 24 else task['task_name']
            desc = task['task_description'][:34] + "..." if len(task['task_description']) > 34 else task['task_description']
            
            print(f"{task['id']:<4} {name:<25} {desc:<35} {status:<10}")
        print("-"*80)
    
    def run(self) -> None:
        """Run the main application loop."""
        print("Welcome to Todo List Manager!")
        
        while True:
            try:
                self.display_menu()
                choice = input("\nEnter your choice (0-7): ").strip()
                
                if choice == '1':
                    self.add_task_interactive()
                elif choice == '2':
                    self.remove_task_interactive()
                elif choice == '3':
                    self.search_tasks_interactive()
                elif choice == '4':
                    self.finish_task_interactive()
                elif choice == '5':
                    self.view_all_tasks()
                elif choice == '6':
                    self.clear_all_tasks_interactive()
                elif choice == '7':
                    self.show_statistics()
                elif choice == '0':
                    print("\nThank you for using Todo List Manager! Goodbye!")
                    break
                else:
                    print("✗ Invalid choice. Please enter a number between 0-7.")
                    
            except KeyboardInterrupt:
                print("\n\nExiting Todo List Manager. Goodbye!")
                break
            except Exception as e:
                self._logger.error(f"Unexpected error in main loop: {e}")
                print(f"✗ An unexpected error occurred: {e}")


def main():
    """Main entry point of the application."""
    app = TodoListApp()
    app.run()


if __name__ == "__main__":
    main()
