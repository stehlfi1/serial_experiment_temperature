
"""
High-quality Todo List Application
A console-based task management system implementing ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import threading
from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Name/title of the task
        description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
    """
    id: int
    name: str
    description: str
    is_finished: bool = False
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary format for external use."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished
        }


class TaskManagerError(Exception):
    """Base exception class for TaskManager related errors."""
    pass


class InvalidTaskDataError(TaskManagerError):
    """Raised when invalid task data is provided."""
    pass


class TaskNotFoundError(TaskManagerError):
    """Raised when a task with specified ID is not found."""
    pass


class TaskManager:
    """
    A thread-safe task management system for handling todo list operations.
    
    This class provides CRUD operations for tasks with efficient lookups,
    validation, and error handling following ISO/IEC 25010 standards.
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
            InvalidTaskDataError: If task name is invalid
        """
        if not isinstance(task_name, str):
            raise InvalidTaskDataError("Task name must be a string")
        if not task_name.strip():
            raise InvalidTaskDataError("Task name cannot be empty or whitespace only")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): The task description to validate
            
        Raises:
            InvalidTaskDataError: If task description is invalid
        """
        if not isinstance(task_description, str):
            raise InvalidTaskDataError("Task description must be a string")
        if not task_description.strip():
            raise InvalidTaskDataError("Task description cannot be empty or whitespace only")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            InvalidTaskDataError: If task ID is invalid
        """
        if not isinstance(task_id, int):
            raise InvalidTaskDataError("Task ID must be an integer")
        if task_id <= 0:
            raise InvalidTaskDataError("Task ID must be a positive integer")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term (str): The search term to validate
            
        Raises:
            InvalidTaskDataError: If search term is invalid
        """
        if not isinstance(search_term, str):
            raise InvalidTaskDataError("Search term must be a string")
        if not search_term.strip():
            raise InvalidTaskDataError("Search term cannot be empty or whitespace only")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task
            task_description (str): Description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            InvalidTaskDataError: If task name or description is invalid
        """
        # Validate inputs
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        with self._lock:
            # Create new task with unique ID
            task_id = self._next_id
            self._next_id += 1
            
            task = Task(
                id=task_id,
                name=task_name.strip(),
                description=task_description.strip()
            )
            
            self._tasks[task_id] = task
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): ID of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            InvalidTaskDataError: If task ID is invalid
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
            InvalidTaskDataError: If search term is invalid
        """
        self._validate_search_term(search_term)
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.name.lower() or 
                    search_term_lower in task.description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if not found
            
        Raises:
            InvalidTaskDataError: If task ID is invalid
        """
        self._validate_task_id(task_id)
        
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
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
        Returns:
            bool: Always True, indicating successful operation
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1
            return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks in the todo list
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
    Main function demonstrating the TaskManager usage.
    This serves as an example of how to use the TaskManager class.
    """
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding tasks...")
        task1_id = task_manager.add("Buy groceries", "Need to buy milk, bread, and eggs")
        task2_id = task_manager.add("Write report", "Complete the quarterly sales report")
        task3_id = task_manager.add("Call dentist", "Schedule annual checkup appointment")
        
        print(f"Added task with ID: {task1_id}")
        print(f"Added task with ID: {task2_id}")
        print(f"Added task with ID: {task3_id}")
        
        # Display all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Finish a task
        print(f"\nMarking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("\nSearching for 'report':")
        search_results = task_manager.search("report")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Display statistics
        print(f"\nTotal tasks: {task_manager.get_task_count()}")
        print(f"Completed tasks: {task_manager.get_completed_count()}")
        
    except (InvalidTaskDataError, TaskNotFoundError) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
