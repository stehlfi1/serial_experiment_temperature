
"""
Todo List Application - A console-based task management system.

This module implements a TaskManager class that provides comprehensive
task management functionality including adding, removing, searching,
and completing tasks while adhering to ISO/IEC 25010 quality standards.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """
    Represents a task with its properties.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Task name
        description (str): Task description
        is_finished (bool): Completion status
        created_at (datetime): Task creation timestamp
    """
    id: int
    name: str
    description: str
    is_finished: bool
    created_at: datetime

    def to_dict(self) -> Dict:
        """Convert task to dictionary format for external consumption."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished,
            'created_at': self.created_at.isoformat()
        }


class TaskManager:
    """
    A thread-safe task management system for handling todo list operations.
    
    This class provides comprehensive task management functionality including
    creation, deletion, searching, and completion tracking. It uses efficient
    data structures for optimal performance and includes comprehensive error
    handling and validation.
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

    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term (str): The search term to validate
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is empty or only whitespace
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        if not search_term or not search_term.strip():
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
            task_name (str): The name of the task (non-empty)
            task_description (str): The description of the task (non-empty)
            
        Returns:
            int: The unique ID assigned to the new task
            
        Raises:
            TypeError: If inputs are not strings
            ValueError: If inputs are empty or only whitespace
            
        Example:
            >>> manager = TaskManager()
            >>> task_id = manager.add("Buy groceries", "Get milk and bread")
            >>> print(task_id)
            1
        """
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)

        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            
            task = Task(
                id=task_id,
                name=task_name.strip(),
                description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
            )
            
            self._tasks[task_id] = task
            return task_id

    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The ID of the task to remove (positive integer)
            
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
            if self._task_exists(task_id):
                del self._tasks[task_id]
                return True
            return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description using case-insensitive matching.
        
        Args:
            task_term (str): The search term to look for (non-empty)
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or only whitespace
            
        Example:
            >>> manager = TaskManager()
            >>> manager.add("Buy groceries", "Get milk and bread")
            >>> results = manager.search("buy")
            >>> print(len(results))
            1
        """
        self._validate_search_term(task_term)

        search_term_lower = task_term.strip().lower()
        matching_tasks = []

        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.name.lower() or 
                    search_term_lower in task.description.lower()):
                    matching_tasks.append(task.to_dict())

        # Sort by creation time for consistent ordering
        matching_tasks.sort(key=lambda x: x['created_at'])
        return matching_tasks

    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed by its ID.
        
        Args:
            task_id (int): The ID of the task to mark as finished (positive integer)
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Example:
            >>> manager = TaskManager()
            >>> task_id = manager.add("Test task", "Test description")
            >>> success = manager.finish(task_id)
            >>> print(success)
            True
        """
        self._validate_task_id(task_id)

        with self._lock:
            if self._task_exists(task_id):
                self._tasks[task_id].is_finished = True
                return True
            return False

    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their complete information.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by creation time
            
        Example:
            >>> manager = TaskManager()
            >>> manager.add("Task 1", "Description 1")
            1
            >>> manager.add("Task 2", "Description 2")
            2
            >>> all_tasks = manager.get_all()
            >>> print(len(all_tasks))
            2
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
        
        # Sort by creation time for consistent ordering
        all_tasks.sort(key=lambda x: x['created_at'])
        return all_tasks

    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful clearing
            
        Example:
            >>> manager = TaskManager()
            >>> manager.add("Task 1", "Description 1")
            1
            >>> success = manager.clear_all()
            >>> print(success)
            True
            >>> print(len(manager.get_all()))
            0
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True

    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: The number of tasks currently stored
        """
        with self._lock:
            return len(self._tasks)

    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: The number of completed tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)

    def get_pending_count(self) -> int:
        """
        Get the number of pending (incomplete) tasks.
        
        Returns:
            int: The number of pending tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if not task.is_finished)


def main():
    """
    Console application entry point demonstrating TaskManager usage.
    
    This function provides a simple command-line interface for interacting
    with the TaskManager, showcasing all available operations.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, stats, quit")
    
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
                except (TypeError, ValueError) as e:
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
                term = input("Search term: ").strip()
                try:
                    results = task_manager.search(term)
                    if results:
                        print(f"\nFound {len(results)} task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No tasks found")
                except (TypeError, ValueError) as e:
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
                    print(f"\nAll tasks ({len(tasks)}):")
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
                    
            elif command == "stats":
                total = task_manager.get_task_count()
                completed = task_manager.get_completed_count()
                pending = task_manager.get_pending_count()
                print(f"\nTask Statistics:")
                print(f"  Total tasks: {total}")
                print(f"  Completed: {completed}")
                print(f"  Pending: {pending}")
                
            else:
                print("Unknown command. Available: add, remove, search, finish, list, clear, stats, quit")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
