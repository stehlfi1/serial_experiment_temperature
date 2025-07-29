
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
    is_finished: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        """Set creation timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format for API responses.
        
        Returns:
            Dict: Task data in dictionary format
        """
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }


class TaskManager:
    """
    Thread-safe task management system for todo list operations.
    
    Provides CRUD operations for tasks with efficient data structures
    and comprehensive error handling.
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
            task_name (str): Task name to validate
            
        Raises:
            ValueError: If task name is invalid
        """
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace only")
        if len(task_name.strip()) > 100:
            raise ValueError("Task name cannot exceed 100 characters")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): Task description to validate
            
        Raises:
            ValueError: If task description is invalid
        """
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        if len(task_description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            ValueError: If task ID is invalid
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _validate_search_term(self, task_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            task_term (str): Search term to validate
            
        Raises:
            ValueError: If search term is invalid
        """
        if not isinstance(task_term, str):
            raise TypeError("Search term must be a string")
        if not task_term or not task_term.strip():
            raise ValueError("Search term cannot be empty or whitespace only")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task
            task_description (str): Description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If inputs are invalid
            TypeError: If inputs are not strings
        """
        # Input validation
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
        Remove a task from the todo list.
        
        Args:
            task_id (int): ID of the task to remove
            
        Returns:
            bool: True if task was removed, False if task not found
            
        Raises:
            ValueError: If task ID is invalid
            TypeError: If task ID is not an integer
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
        
        Args:
            task_term (str): Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            ValueError: If search term is invalid
            TypeError: If search term is not a string
        """
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
            task_id (int): ID of the task to mark as finished
            
        Returns:
            bool: True if task was marked as finished, False if task not found
            
        Raises:
            ValueError: If task ID is invalid
            TypeError: If task ID is not an integer
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks from the todo list.
        
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
            bool: Always returns True indicating successful clearing
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
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
    Demonstration of the TaskManager functionality.
    """
    # Create task manager instance
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {task1_id}, {task2_id}, {task3_id}")
        
        # Display all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        print(f"\nMarking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("\nSearching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print(f"\nStatistics:")
        print(f"  Total tasks: {task_manager.get_task_count()}")
        print(f"  Completed tasks: {task_manager.get_completed_count()}")
        
        # Remove a task
        print(f"\nRemoving task {task2_id}...")
        removed = task_manager.remove(task2_id)
        print(f"Task removed: {removed}")
        
        # Display final state
        print("\nFinal task list:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
            
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
