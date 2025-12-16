
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
    A thread-safe task manager for handling todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and updating tasks. All operations are
    thread-safe and include proper validation and error handling.
    
    Attributes:
        _tasks (Dict[int, Task]): Internal storage for tasks indexed by ID
        _next_id (int): Counter for generating unique task IDs
        _lock (threading.RLock): Thread synchronization lock
    """
    
    def __init__(self) -> None:
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): The name/title of the task
            task_description (str): Detailed description of the task
            
        Returns:
            int: The unique ID assigned to the new task
            
        Raises:
            ValueError: If task_name or task_description is empty or contains only whitespace
            TypeError: If task_name or task_description is not a string
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Get milk, bread, and eggs")
            >>> print(task_id)
            1
        """
        # Input validation
        if not isinstance(task_name, str):
            raise TypeError("task_name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("task_description must be a string")
        
        # Check for empty or whitespace-only strings
        if not task_name.strip():
            raise ValueError("task_name cannot be empty or contain only whitespace")
        if not task_description.strip():
            raise ValueError("task_description cannot be empty or contain only whitespace")
        
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
            task_id (int): The unique ID of the task to remove
            
        Returns:
            bool: True if the task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Test description")
            >>> success = tm.remove(task_id)
            >>> print(success)
            True
        """
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
        Search for tasks by name or description containing the given term.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions
            
        Returns:
            List[Dict]: List of dictionaries containing task information that match the search term
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or contains only whitespace
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Get milk and bread")
            >>> results = tm.search("milk")
            >>> print(len(results))
            1
        """
        if not isinstance(task_term, str):
            raise TypeError("task_term must be a string")
        if not task_term.strip():
            raise ValueError("task_term cannot be empty or contain only whitespace")
        
        search_term = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term in task.task_name.lower() or 
                    search_term in task.task_description.lower()):
                    matching_tasks.append(self._task_to_dict(task))
        
        return matching_tasks
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished
            
        Returns:
            bool: True if the task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> success = tm.finish(task_id)
            >>> print(success)
            True
        """
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
            List[Dict]: List of dictionaries containing all task information,
                       sorted by creation time (oldest first)
                       
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> all_tasks = tm.get_all()
            >>> print(len(all_tasks))
            2
        """
        with self._lock:
            # Sort tasks by creation time for consistent ordering
            sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.created_at)
            return [self._task_to_dict(task) for task in sorted_tasks]
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True to indicate successful clearing
            
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
            return True
    
    def _task_to_dict(self, task: Task) -> Dict:
        """
        Convert a Task object to a dictionary format for external consumption.
        
        Args:
            task (Task): The task object to convert
            
        Returns:
            Dict: Dictionary containing task information in the required format
        """
        return {
            'id': task.id,
            'task_name': task.task_name,
            'task_description': task.task_description,
            'is_finished': task.is_finished
        }
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks in the todo list.
        
        Returns:
            int: The number of tasks currently stored
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> print(tm.get_task_count())
            1
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: The number of tasks marked as finished
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Task 1", "Description 1")
            >>> tm.finish(task_id)
            >>> print(tm.get_completed_count())
            1
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Console interface for the todo list application.
    
    Provides a simple command-line interface for interacting with the TaskManager.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, stats, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                print("Goodbye!")
                break
            elif command == 'add':
                name = input("Task name: ").strip()
                description = input("Task description: ").strip()
                try:
                    task_id = task_manager.add(name, description)
                    print(f"Task added successfully with ID: {task_id}")
                except (ValueError, TypeError) as e:
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
                    term = input("Search term: ").strip()
                    results = task_manager.search(term)
                    if results:
                        print(f"\nFound {len(results)} matching task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No matching tasks found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'finish':
                try:
                    task_id = int(input("Task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as finished")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == 'list':
                tasks = task_manager.get_all()
                if tasks:
                    print(f"\nAll tasks ({len(tasks)}):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == 'clear':
                confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
                if confirm == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared")
                else:
                    print("Operation cancelled")
            
            elif command == 'stats':
                total = task_manager.get_task_count()
                completed = task_manager.get_completed_count()
                pending = total - completed
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
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
