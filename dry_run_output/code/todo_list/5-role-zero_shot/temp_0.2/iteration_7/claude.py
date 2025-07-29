
"""
High-Quality Todo List Application
A console-based task management system implementing ISO/IEC 25010 standards.
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
        """Initialize created_at timestamp if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format for external consumption.
        
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
    A thread-safe task management system for handling todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and updating tasks while ensuring data
    integrity and performance optimization.
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
            ValueError: If task name is invalid
        """
        if not isinstance(task_name, str):
            raise ValueError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise ValueError("Task name cannot be empty or whitespace only")
        if len(task_name.strip()) > 100:
            raise ValueError("Task name cannot exceed 100 characters")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): The task description to validate
            
        Raises:
            ValueError: If task description is invalid
        """
        if not isinstance(task_description, str):
            raise ValueError("Task description must be a string")
        if len(task_description) > 500:
            raise ValueError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            ValueError: If task ID is invalid
        """
        if not isinstance(task_id, int):
            raise ValueError("Task ID must be an integer")
        if task_id <= 0:
            raise ValueError("Task ID must be a positive integer")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term (str): The search term to validate
            
        Raises:
            ValueError: If search term is invalid
        """
        if not isinstance(search_term, str):
            raise ValueError("Search term must be a string")
        if not search_term or not search_term.strip():
            raise ValueError("Search term cannot be empty or whitespace only")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (1-100 characters)
            task_description (str): Description of the task (max 500 characters)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            ValueError: If input parameters are invalid
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
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            ValueError: If task_id is invalid
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            search_term (str): Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            ValueError: If search_term is invalid
        """
        self._validate_search_term(search_term)
        
        search_term_lower = search_term.strip().lower()
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
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            ValueError: If task_id is invalid
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


def main():
    """
    Demonstration of the TaskManager functionality.
    This function shows basic usage of all implemented methods.
    """
    print("=== Todo List Application Demo ===\n")
    
    # Initialize task manager
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added task {task1_id}: Buy groceries")
        print(f"Added task {task2_id}: Complete project")
        print(f"Added task {task3_id}: Exercise")
        
        # Display all tasks
        print("\n--- All Tasks ---")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Mark a task as finished
        print(f"\nMarking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("\nSearching for 'project'...")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"Found: {status} [{task['id']}] {task['task_name']}")
        
        # Display updated task list
        print("\n--- Updated Task List ---")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Show statistics
        print(f"\nTotal tasks: {task_manager.get_task_count()}")
        print(f"Completed tasks: {task_manager.get_completed_count()}")
        
        # Remove a task
        print(f"\nRemoving task {task2_id}...")
        removed = task_manager.remove(task2_id)
        print(f"Task removal {'successful' if removed else 'failed'}")
        
        # Final task list
        print("\n--- Final Task List ---")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"{status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
