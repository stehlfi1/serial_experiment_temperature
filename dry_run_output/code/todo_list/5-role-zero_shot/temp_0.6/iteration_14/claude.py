
"""
High-Quality Todo List Application

This module implements a console-based todo list application following ISO/IEC 25010 
quality standards with emphasis on functionality, reliability, usability, efficiency,
maintainability, and portability.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single task with all its properties.
    
    Attributes:
        id: Unique identifier for the task
        task_name: Name/title of the task
        task_description: Detailed description of the task
        is_finished: Completion status of the task
        created_at: Timestamp when task was created
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
        """Convert task to dictionary format for API responses."""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }


class TaskValidationError(ValueError):
    """Raised when task validation fails."""
    pass


class TaskNotFoundError(KeyError):
    """Raised when a task with given ID is not found."""
    pass


class TaskManager:
    """
    A thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks. All operations
    are thread-safe and include proper validation.
    
    Attributes:
        _tasks: Dictionary storing tasks with ID as key
        _next_id: Counter for generating unique task IDs
        _lock: Thread lock for ensuring thread safety
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for nested operations
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name: The name of the task
            task_description: The description of the task
            
        Raises:
            TaskValidationError: If validation fails
            TypeError: If inputs are not strings
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or whitespace only")
        
        if not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or whitespace only")
        
        if len(task_name.strip()) > 100:
            raise TaskValidationError("Task name cannot exceed 100 characters")
        
        if len(task_description.strip()) > 500:
            raise TaskValidationError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id: The ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: Name of the task (1-100 characters, non-empty)
            task_description: Description of the task (1-500 characters, non-empty)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If input validation fails
            TypeError: If inputs are not strings
            
        Example:
            >>> manager = TaskManager()
            >>> task_id = manager.add("Buy groceries", "Buy milk, bread, and eggs")
            >>> print(task_id)
            1
        """
        self._validate_task_input(task_name, task_description)
        
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            
            self._tasks[task_id] = task
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Example:
            >>> manager = TaskManager()
            >>> task_id = manager.add("Test task", "Test description")
            >>> success = manager.remove(task_id)
            >>> print(success)
            True
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Performs case-insensitive substring search in both task name and description.
        
        Args:
            task_term: Search term to look for
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or whitespace only
            
        Example:
            >>> manager = TaskManager()
            >>> manager.add("Buy groceries", "Buy milk and bread")
            >>> results = manager.search("milk")
            >>> print(len(results))
            1
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        
        search_term = task_term.strip().lower()
        if not search_term:
            raise ValueError("Search term cannot be empty or whitespace only")
        
        with self._lock:
            matching_tasks = []
            for task in self._tasks.values():
                if (search_term in task.task_name.lower() or 
                    search_term in task.task_description.lower()):
                    matching_tasks.append(task.to_dict())
            
            # Sort by task ID for consistent ordering
            matching_tasks.sort(key=lambda x: x['id'])
            return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Example:
            >>> manager = TaskManager()
            >>> task_id = manager.add("Complete project", "Finish the todo app")
            >>> success = manager.finish(task_id)
            >>> print(success)
            True
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
            
        Example:
            >>> manager = TaskManager()
            >>> manager.add("Task 1", "Description 1")
            >>> manager.add("Task 2", "Description 2")
            >>> all_tasks = manager.get_all()
            >>> print(len(all_tasks))
            2
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            # Sort by task ID for consistent ordering
            all_tasks.sort(key=lambda x: x['id'])
            return all_tasks
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True to indicate successful clearing
            
        Example:
            >>> manager = TaskManager()
            >>> manager.add("Task 1", "Description 1")
            >>> success = manager.clear_all()
            >>> print(success)
            True
            >>> print(len(manager.get_all()))
            0
        """
        with self._lock:
            self._tasks.clear()
            return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks in the system
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
    Console interface for the Todo List application.
    
    Provides a simple command-line interface for interacting with the TaskManager.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, quit")
    print("Type 'help' for detailed command information")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                print("Goodbye!")
                break
            
            elif command == 'help':
                print("\nAvailable commands:")
                print("  add - Add a new task")
                print("  remove - Remove a task by ID")
                print("  search - Search tasks by keyword")
                print("  finish - Mark a task as completed")
                print("  list - Show all tasks")
                print("  clear - Remove all tasks")
                print("  quit - Exit the application")
            
            elif command == 'add':
                name = input("Task name: ").strip()
                description = input("Task description: ").strip()
                try:
                    task_id = task_manager.add(name, description)
                    print(f"Task added successfully with ID: {task_id}")
                except (TaskValidationError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'remove':
                try:
                    task_id = int(input("Task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'search':
                try:
                    term = input("Search term: ")
                    results = task_manager.search(term)
                    if results:
                        print(f"\nFound {len(results)} matching task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  [{task['id']}] {status} {task['task_name']}: {task['task_description']}")
                    else:
                        print("No matching tasks found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'finish':
                try:
                    task_id = int(input("Task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as completed")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'list':
                tasks = task_manager.get_all()
                if tasks:
                    print(f"\nAll tasks ({len(tasks)} total):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  [{task['id']}] {status} {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == 'clear':
                confirm = input("Are you sure you want to delete all tasks? (y/N): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared")
                else:
                    print("Operation cancelled")
            
            else:
                print("Unknown command. Type 'help' for available commands.")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
