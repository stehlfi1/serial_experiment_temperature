
"""
High-Quality Todo List Application

A console-based todo list application implementing the TaskManager class
with comprehensive task management functionality following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Data class representing a task with all its properties.
    
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
    A thread-safe task management system for handling todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks. All operations
    are optimized for performance and include proper error handling.
    
    Attributes:
        _tasks (Dict[int, Task]): Internal storage for tasks indexed by ID
        _next_id (int): Counter for generating unique task IDs
        _lock (threading.RLock): Thread lock for ensuring thread safety
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
        
        # Check for empty or whitespace-only strings
        if not task_name.strip():
            raise ValueError("task_name cannot be empty or contain only whitespace")
        if not task_description.strip():
            raise ValueError("task_description cannot be empty or contain only whitespace")
        
        with self._lock:
            task_id = self._next_id
            self._next_id += 1
            
            # Create new task with current timestamp
            new_task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
            )
            
            # Store task in dictionary for O(1) access
            self._tasks[task_id] = new_task
            
        return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): The unique ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
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
        Search for tasks by name or description containing the search term.
        
        Args:
            task_term (str): The search term to look for in task names and descriptions
            
        Returns:
            List[Dict]: List of dictionaries containing matching task information
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or contains only whitespace
        """
        # Input validation
        if not isinstance(task_term, str):
            raise TypeError("task_term must be a string")
        if not task_term.strip():
            raise ValueError("task_term cannot be empty or contain only whitespace")
        
        search_term = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                # Case-insensitive search in both name and description
                if (search_term in task.task_name.lower() or 
                    search_term in task.task_description.lower()):
                    matching_tasks.append(self._task_to_dict(task))
        
        # Sort results by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): The unique ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is negative or zero
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
        Retrieve all tasks with their complete information.
        
        Returns:
            List[Dict]: List of dictionaries containing all task information,
                       sorted by task ID
        """
        with self._lock:
            all_tasks = [self._task_to_dict(task) for task in self._tasks.values()]
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: Always returns True indicating successful clearing
        """
        with self._lock:
            self._tasks.clear()
            # Reset ID counter for efficiency
            self._next_id = 1
        
        return True
    
    def _task_to_dict(self, task: Task) -> Dict:
        """
        Convert a Task object to a dictionary with the required format.
        
        Args:
            task (Task): The task object to convert
            
        Returns:
            Dict: Dictionary containing task information in the specified format
        """
        return {
            'id': task.id,
            'task_name': task.task_name,
            'task_description': task.task_description,
            'is_finished': task.is_finished
        }
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks in the system.
        
        Returns:
            int: Total number of tasks
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
    Demonstration of the TaskManager functionality.
    
    This function provides a simple console interface to interact with
    the TaskManager and demonstrates all available operations.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Available commands:")
    print("1. add - Add a new task")
    print("2. remove - Remove a task by ID")
    print("3. search - Search tasks")
    print("4. finish - Mark task as completed")
    print("5. list - Show all tasks")
    print("6. clear - Clear all tasks")
    print("7. stats - Show task statistics")
    print("8. quit - Exit application")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().lower()
            
            if command == "add":
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
                        print("Task marked as completed")
                    else:
                        print("Task not found")
                except (ValueError, TypeError) as e:
                    print(f"Error: {e}")
            
            elif command == "list":
                tasks = task_manager.get_all()
                if tasks:
                    print(f"All tasks ({len(tasks)}):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == "clear":
                confirm = input("Are you sure you want to clear all tasks? (y/N): ").strip().lower()
                if confirm == 'y':
                    task_manager.clear_all()
                    print("All tasks cleared successfully")
                else:
                    print("Operation cancelled")
            
            elif command == "stats":
                total = task_manager.get_task_count()
                completed = task_manager.get_completed_count()
                pending = task_manager.get_pending_count()
                print(f"Task Statistics:")
                print(f"  Total tasks: {total}")
                print(f"  Completed: {completed}")
                print(f"  Pending: {pending}")
            
            elif command == "quit":
                print("Goodbye!")
                break
            
            else:
                print("Invalid command. Please try again.")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        print()  # Add blank line for readability


if __name__ == "__main__":
    main()
