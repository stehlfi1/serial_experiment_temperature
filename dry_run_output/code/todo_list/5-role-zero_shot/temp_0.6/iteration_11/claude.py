
"""
High-quality Todo List Application
A console-based task management system following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Data class representing a task with all its attributes.
    
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
        """Convert task to dictionary format for external consumption."""
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
    A thread-safe task management system for handling todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and updating tasks with proper validation
    and error handling.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses a dictionary for O(1) lookups and a lock for thread safety.
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
        """
        if not isinstance(task_name, str) or not task_name.strip():
            raise TaskValidationError("Task name must be a non-empty string")
        
        if not isinstance(task_description, str) or not task_description.strip():
            raise TaskValidationError("Task description must be a non-empty string")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id (int): The ID to validate
            
        Raises:
            TaskValidationError: If ID is invalid
            TaskNotFoundError: If task with ID doesn't exist
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (must be non-empty)
            task_description (str): Description of the task (must be non-empty)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If input parameters are invalid
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Get milk, bread, and eggs")
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
            task_id (int): ID of the task to remove (must be positive)
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TaskValidationError: If task_id is invalid
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Test description")
            >>> success = tm.remove(task_id)
            >>> print(success)
            True
        """
        try:
            self._validate_task_id(task_id)
            
            with self._lock:
                del self._tasks[task_id]
                return True
                
        except TaskNotFoundError:
            return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            search_term (str): Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TaskValidationError: If search_term is invalid
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Get milk and bread")
            >>> results = tm.search("milk")
            >>> print(len(results))
            1
        """
        if not isinstance(search_term, str) or not search_term.strip():
            raise TaskValidationError("Search term must be a non-empty string")
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.task_name.lower() or 
                    search_term_lower in task.task_description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False otherwise
            
        Raises:
            TaskValidationError: If task_id is invalid
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> success = tm.finish(task_id)
            >>> print(success)
            True
        """
        try:
            self._validate_task_id(task_id)
            
            with self._lock:
                self._tasks[task_id].is_finished = True
                return True
                
        except TaskNotFoundError:
            return False
    
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
            >>> print(len(all_tasks))
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
            bool: Always returns True indicating successful operation
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> success = tm.clear_all()
            >>> print(success)
            True
            >>> print(len(tm.get_all()))
            0
        """
        with self._lock:
            self._tasks.clear()
            # Reset ID counter for clean slate
            self._next_id = 1
        
        return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks currently stored
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
    Demonstrates the TaskManager functionality with a simple CLI.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "quit":
                print("Goodbye!")
                break
                
            elif command == "add":
                name = input("Task name: ").strip()
                description = input("Task description: ").strip()
                try:
                    task_id = task_manager.add(name, description)
                    print(f"Task added with ID: {task_id}")
                except TaskValidationError as e:
                    print(f"Error: {e}")
                    
            elif command == "remove":
                try:
                    task_id = int(input("Task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except (ValueError, TaskValidationError) as e:
                    print(f"Error: {e}")
                    
            elif command == "search":
                search_term = input("Search term: ").strip()
                try:
                    results = task_manager.search(search_term)
                    if results:
                        print(f"Found {len(results)} matching task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No matching tasks found")
                except TaskValidationError as e:
                    print(f"Error: {e}")
                    
            elif command == "finish":
                try:
                    task_id = int(input("Task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as finished")
                    else:
                        print("Task not found")
                except (ValueError, TaskValidationError) as e:
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
                confirm = input("Are you sure you want to clear all tasks? (y/N): ")
                if confirm.lower() == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared")
                else:
                    print("Operation cancelled")
                    
            else:
                print("Unknown command. Available: add, remove, search, finish, list, clear, quit")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
