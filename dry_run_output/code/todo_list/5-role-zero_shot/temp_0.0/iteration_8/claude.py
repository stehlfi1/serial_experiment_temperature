
"""
High-quality console-based todo list application following ISO/IEC 25010 standards.

This module provides a TaskManager class for managing todo tasks with full CRUD operations,
validation, and error handling.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Data class representing a todo task.
    
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


class TaskManager:
    """
    Thread-safe task manager for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks with proper
    validation and error handling.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_name(self, task_name: str) -> None:
        """
        Validate task name input.
        
        Args:
            task_name (str): The task name to validate
            
        Raises:
            TypeError: If task_name is not a string
            ValueError: If task_name is empty or only whitespace
        """
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or only whitespace")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): The task description to validate
            
        Raises:
            TypeError: If task_description is not a string
            ValueError: If task_description is empty or only whitespace
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise ValueError("Task description cannot be empty or only whitespace")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _validate_search_term(self, task_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            task_term (str): The search term to validate
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or only whitespace
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty or only whitespace")
    
    def _task_exists(self, task_id: int) -> bool:
        """
        Check if a task exists by ID.
        
        Args:
            task_id (int): The task ID to check
            
        Returns:
            bool: True if task exists, False otherwise
        """
        return task_id in self._tasks
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name/title of the task
            task_description (str): Detailed description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TypeError: If inputs are not strings
            ValueError: If inputs are empty or only whitespace
        """
        # Validate inputs
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        with self._lock:
            # Create new task with unique ID
            task_id = self._next_id
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            
            # Store task and increment ID counter
            self._tasks[task_id] = task
            self._next_id += 1
            
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by ID.
        
        Args:
            task_id (int): Unique ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        # Validate input
        self._validate_task_id(task_id)
        
        with self._lock:
            if self._task_exists(task_id):
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term (str): Search term to match against task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or only whitespace
        """
        # Validate input
        self._validate_search_term(task_term)
        
        search_term_lower = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                # Case-insensitive search in both name and description
                if (search_term_lower in task.task_name.lower() or 
                    search_term_lower in task.task_description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): Unique ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
        """
        # Validate input
        self._validate_task_id(task_id)
        
        with self._lock:
            if self._task_exists(task_id):
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
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
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
    
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
    
    def get_pending_count(self) -> int:
        """
        Get the number of pending (incomplete) tasks.
        
        Returns:
            int: Number of pending tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if not task.is_finished)


def main():
    """
    Console interface for the todo list application.
    
    Provides a simple command-line interface for interacting with the TaskManager.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, stats, quit")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().lower()
            
            if command == "quit" or command == "exit":
                print("Goodbye!")
                break
            
            elif command == "add":
                name = input("Task name: ").strip()
                description = input("Task description: ").strip()
                try:
                    task_id = task_manager.add(name, description)
                    print(f"✓ Task added with ID: {task_id}")
                except (TypeError, ValueError) as e:
                    print(f"✗ Error: {e}")
            
            elif command == "remove":
                try:
                    task_id = int(input("Task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("✓ Task removed successfully")
                    else:
                        print("✗ Task not found")
                except ValueError:
                    print("✗ Please enter a valid task ID")
                except (TypeError, ValueError) as e:
                    print(f"✗ Error: {e}")
            
            elif command == "search":
                term = input("Search term: ").strip()
                try:
                    results = task_manager.search(term)
                    if results:
                        print(f"\nFound {len(results)} matching task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No matching tasks found")
                except (TypeError, ValueError) as e:
                    print(f"✗ Error: {e}")
            
            elif command == "finish":
                try:
                    task_id = int(input("Task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("✓ Task marked as finished")
                    else:
                        print("✗ Task not found")
                except ValueError:
                    print("✗ Please enter a valid task ID")
                except (TypeError, ValueError) as e:
                    print(f"✗ Error: {e}")
            
            elif command == "list":
                tasks = task_manager.get_all()
                if tasks:
                    print(f"\nAll tasks ({len(tasks)}):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ").strip().lower()
                if confirm in ['yes', 'y']:
                    task_manager.clear_all()
                    print("✓ All tasks cleared")
                else:
                    print("Operation cancelled")
            
            elif command == "stats":
                total = task_manager.get_task_count()
                completed = task_manager.get_completed_count()
                pending = task_manager.get_pending_count()
                print(f"\nTask Statistics:")
                print(f"  Total tasks: {total}")
                print(f"  Completed: {completed}")
                print(f"  Pending: {pending}")
            
            else:
                print("Unknown command. Available commands: add, remove, search, finish, list, clear, stats, quit")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
        
        print()  # Add spacing between commands


if __name__ == "__main__":
    main()
