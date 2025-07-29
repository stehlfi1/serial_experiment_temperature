
"""
High-quality Todo List Application
Implements a console-based task management system following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Data class representing a single task.
    
    Attributes:
        id (int): Unique identifier for the task
        task_name (str): Name/title of the task
        task_description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
        created_at (datetime): Timestamp when task was created
    """
    id: int
    task_name: str
    task_description: str
    is_finished: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        """Set creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary format for external use."""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }


class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception for when a task is not found."""
    pass


class TaskManager:
    """
    Thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and managing task completion status.
    All operations are thread-safe and include comprehensive validation.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses a dictionary for O(1) lookups and a threading lock for
        thread safety in concurrent environments.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name (str): The name of the task
            task_description (str): The description of the task
            
        Raises:
            TaskValidationError: If inputs are invalid
            TypeError: If inputs are not strings
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or whitespace only")
        
        if not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or whitespace only")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id (int): The ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (cannot be empty)
            task_description (str): Description of the task (cannot be empty)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If task inputs are invalid
            TypeError: If inputs are not strings
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Buy milk, bread, and eggs")
            >>> print(task_id)
            1
        """
        self._validate_task_input(task_name, task_description)
        
        with self._lock:
            task_id = self._next_id
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            self._tasks[task_id] = task
            self._next_id += 1
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id (int): ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Test description")
            >>> success = tm.remove(task_id)
            >>> print(success)
            True
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Performs case-insensitive substring search across task names and descriptions.
        
        Args:
            search_term (str): Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If search_term is not a string
            TaskValidationError: If search_term is empty
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Buy milk and bread")
            >>> results = tm.search("buy")
            >>> len(results)
            1
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        search_term = search_term.strip()
        if not search_term:
            raise TaskValidationError("Search term cannot be empty or whitespace only")
        
        search_lower = search_term.lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_lower in task.task_name.lower() or 
                    search_lower in task.task_description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if already finished
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> success = tm.finish(task_id)
            >>> print(success)
            True
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            task = self._tasks[task_id]
            if not task.is_finished:
                task.is_finished = True
                return True
            return False  # Task was already finished
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> all_tasks = tm.get_all()
            >>> len(all_tasks)
            2
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: True if tasks were cleared successfully, False if no tasks existed
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> success = tm.clear_all()
            >>> print(success)
            True
            >>> len(tm.get_all())
            0
        """
        with self._lock:
            if self._tasks:
                self._tasks.clear()
                return True
            return False  # No tasks to clear
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Total number of tasks in the system
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function provides a simple console interface to interact with
    the TaskManager and demonstrates all available operations.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Available commands: add, remove, search, finish, list, clear, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "quit":
                print("Goodbye!")
                break
            
            elif command == "add":
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                try:
                    task_id = task_manager.add(name, description)
                    print(f"Task added successfully with ID: {task_id}")
                except (TaskValidationError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "remove":
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except (ValueError, TypeError, TaskValidationError) as e:
                    print(f"Error: {e}")
            
            elif command == "search":
                search_term = input("Enter search term: ").strip()
                try:
                    results = task_manager.search(search_term)
                    if results:
                        print(f"Found {len(results)} matching task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No matching tasks found")
                except (TaskValidationError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "finish":
                try:
                    task_id = int(input("Enter task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as completed")
                    else:
                        print("Task was already completed")
                except (ValueError, TypeError, TaskValidationError, TaskNotFoundError) as e:
                    print(f"Error: {e}")
            
            elif command == "list":
                tasks = task_manager.get_all()
                if tasks:
                    print(f"All tasks ({len(tasks)} total):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == "clear":
                if task_manager.clear_all():
                    print("All tasks cleared successfully")
                else:
                    print("No tasks to clear")
            
            else:
                print("Unknown command. Available: add, remove, search, finish, list, clear, quit")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
