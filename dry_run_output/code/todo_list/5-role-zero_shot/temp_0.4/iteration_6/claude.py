
"""
High-quality console-based todo list application implementing ISO/IEC 25010 standards.

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
    is_finished: bool
    created_at: datetime


class TaskManager:
    """
    Thread-safe task manager for todo list operations.
    
    Provides comprehensive task management functionality including adding, removing,
    searching, completing, and retrieving tasks with proper validation and error handling.
    """
    
    def __init__(self) -> None:
        """Initialize TaskManager with empty task storage and thread safety."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (cannot be empty or whitespace only)
            task_description (str): Description of the task (cannot be empty or whitespace only)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If task_name or task_description is empty or contains only whitespace
            TypeError: If task_name or task_description is not a string
        """
        # Input validation
        if not isinstance(task_name, str):
            raise TypeError("task_name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("task_description must be a string")
        
        if not task_name or not task_name.strip():
            raise ValueError("task_name cannot be empty or contain only whitespace")
        if not task_description or not task_description.strip():
            raise ValueError("task_description cannot be empty or contain only whitespace")
        
        with self._lock:
            task_id = self._next_id
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
            )
            self._tasks[task_id] = task
            self._next_id += 1
            
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): ID of the task to remove (must be positive)
            
        Returns:
            bool: True if task was successfully removed, False if task doesn't exist
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer")
        if task_id <= 0:
            raise ValueError("task_id must be a positive integer")
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description using case-insensitive matching.
        
        Args:
            task_term (str): Search term to match against task name or description
            
        Returns:
            List[Dict]: List of matching tasks as dictionaries with keys:
                       (id, task_name, task_description, is_finished)
                       
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or contains only whitespace
        """
        # Input validation
        if not isinstance(task_term, str):
            raise TypeError("task_term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("task_term cannot be empty or contain only whitespace")
        
        search_term = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term in task.task_name.lower() or 
                    search_term in task.task_description.lower()):
                    matching_tasks.append(self._task_to_dict(task))
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished (must be positive)
            
        Returns:
            bool: True if task was successfully marked as finished, False if task doesn't exist
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("task_id must be an integer")
        if task_id <= 0:
            raise ValueError("task_id must be a positive integer")
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the todo list.
        
        Returns:
            List[Dict]: List of all tasks as dictionaries with keys:
                       (id, task_name, task_description, is_finished)
                       Sorted by task ID for consistent ordering
        """
        with self._lock:
            all_tasks = [self._task_to_dict(task) for task in self._tasks.values()]
        
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
    
    def _task_to_dict(self, task: Task) -> Dict:
        """
        Convert a Task object to dictionary format for external interface.
        
        Args:
            task (Task): Task object to convert
            
        Returns:
            Dict: Task data with keys (id, task_name, task_description, is_finished)
        """
        return {
            'id': task.id,
            'task_name': task.task_name,
            'task_description': task.task_description,
            'is_finished': task.is_finished
        }
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Total number of tasks in the manager
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
    Console application demonstrating TaskManager functionality.
    
    Provides an interactive command-line interface for managing todo tasks.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Manager ===")
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
                    print(f"Task added successfully with ID: {task_id}")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "remove":
                try:
                    task_id = int(input("Task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "search":
                try:
                    term = input("Search term: ").strip()
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
            
            elif command == "finish":
                try:
                    task_id = int(input("Task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as finished")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "list":
                tasks = task_manager.get_all()
                if tasks:
                    print(f"\nAll tasks ({len(tasks)} total):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  [{task['id']}] {status} {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == "clear":
                confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
                if confirm == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared")
                else:
                    print("Operation cancelled")
            
            else:
                print("Unknown command. Available commands: add, remove, search, finish, list, clear, quit")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
