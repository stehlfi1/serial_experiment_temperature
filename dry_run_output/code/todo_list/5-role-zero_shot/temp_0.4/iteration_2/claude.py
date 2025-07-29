
"""
Todo List Application

A console-based todo list application implementing the TaskManager class
with full CRUD operations and search functionality.

This module adheres to ISO/IEC 25010 quality standards for software systems.
"""

from typing import Dict, List, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Represents a single task in the todo list.
    
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
    Manages todo list operations with thread-safe implementations.
    
    This class provides a complete interface for managing tasks including
    adding, removing, searching, completing, and retrieving tasks.
    All operations are optimized for performance and thread safety.
    """
    
    def __init__(self) -> None:
        """
        Initialize the TaskManager with empty task storage.
        
        Uses a dictionary for O(1) lookups and a thread lock for safety.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): The name/title of the task
            task_description (str): Detailed description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If task_name or task_description is empty or contains only whitespace
            TypeError: If arguments are not strings
            
        Time Complexity: O(1)
        """
        # Input validation
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        if not task_name.strip():
            raise ValueError("Task name cannot be empty or contain only whitespace")
        
        if not task_description.strip():
            raise ValueError("Task description cannot be empty or contain only whitespace")
        
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            
            new_task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
            )
            
            self._tasks[task_id] = new_task
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Time Complexity: O(1)
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Performs case-insensitive substring matching on both task name and description.
        
        Args:
            search_term (str): The term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If search_term is not a string
            ValueError: If search_term is empty or contains only whitespace
            
        Time Complexity: O(n) where n is the number of tasks
        """
        # Input validation
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        if not search_term.strip():
            raise ValueError("Search term cannot be empty or contain only whitespace")
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.task_name.lower() or 
                    search_term_lower in task.task_description.lower()):
                    matching_tasks.append(self._task_to_dict(task))
        
        # Sort by creation time for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique identifier of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Time Complexity: O(1)
        """
        # Input validation
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the todo list.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
            
        Time Complexity: O(n log n) where n is the number of tasks (due to sorting)
        """
        with self._lock:
            all_tasks = [self._task_to_dict(task) for task in self._tasks.values()]
        
        # Sort by ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True to indicate successful operation
            
        Time Complexity: O(1)
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
    
    def _task_to_dict(self, task: Task) -> Dict:
        """
        Convert a Task object to dictionary format for external consumption.
        
        Args:
            task (Task): The task object to convert
            
        Returns:
            Dict: Dictionary containing task information in the required format
            
        Private method for internal use only.
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
            int: Total number of tasks in the system
            
        Time Complexity: O(1)
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
            
        Time Complexity: O(n) where n is the number of tasks
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main() -> None:
    """
    Main function demonstrating the TaskManager functionality.
    
    This function provides a simple console interface for testing
    the TaskManager class operations.
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
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "remove":
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
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
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "finish":
                try:
                    task_id = int(input("Enter task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as finished")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
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
                confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
                if confirm == 'y':
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
