
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
    Represents a single task with all its properties.
    
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
    adding, removing, searching, and managing task completion status.
    All operations are thread-safe and include proper validation.
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
            TaskValidationError: If task name is invalid
        """
        if not isinstance(task_name, str):
            raise TaskValidationError("Task name must be a string")
        if not task_name or not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or whitespace only")
        if len(task_name.strip()) > 100:
            raise TaskValidationError("Task name cannot exceed 100 characters")
    
    def _validate_task_description(self, task_description: str) -> None:
        """
        Validate task description input.
        
        Args:
            task_description (str): The task description to validate
            
        Raises:
            TaskValidationError: If task description is invalid
        """
        if not isinstance(task_description, str):
            raise TaskValidationError("Task description must be a string")
        if not task_description or not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or whitespace only")
        if len(task_description.strip()) > 500:
            raise TaskValidationError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID input.
        
        Args:
            task_id (int): The task ID to validate
            
        Raises:
            TaskValidationError: If task ID is invalid
            TaskNotFoundError: If task ID doesn't exist
        """
        if not isinstance(task_id, int):
            raise TaskValidationError("Task ID must be an integer")
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term input.
        
        Args:
            search_term (str): The search term to validate
            
        Raises:
            TaskValidationError: If search term is invalid
        """
        if not isinstance(search_term, str):
            raise TaskValidationError("Search term must be a string")
        if not search_term or not search_term.strip():
            raise TaskValidationError("Search term cannot be empty or whitespace only")
    
    def _task_to_dict(self, task: Task) -> Dict:
        """
        Convert a Task object to dictionary format.
        
        Args:
            task (Task): The task to convert
            
        Returns:
            Dict: Task data in dictionary format
        """
        return {
            'id': task.id,
            'task_name': task.task_name,
            'task_description': task.task_description,
            'is_finished': task.is_finished
        }
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (1-100 characters)
            task_description (str): Description of the task (1-500 characters)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If input validation fails
        """
        # Validate inputs
        self._validate_task_name(task_name)
        self._validate_task_description(task_description)
        
        with self._lock:
            # Create new task with auto-generated ID
            task_id = self._next_id
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip(),
                is_finished=False,
                created_at=datetime.now()
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
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            TaskValidationError: If task ID is invalid
        """
        try:
            self._validate_task_id(task_id)
            
            with self._lock:
                # Double-check existence after acquiring lock
                if task_id in self._tasks:
                    del self._tasks[task_id]
                    return True
                return False
                
        except (TaskValidationError, TaskNotFoundError):
            return False
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            search_term (str): Term to search for (case-insensitive)
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TaskValidationError: If search term is invalid
        """
        self._validate_search_term(search_term)
        
        search_term_lower = search_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                # Case-insensitive search in both name and description
                if (search_term_lower in task.task_name.lower() or 
                    search_term_lower in task.task_description.lower()):
                    matching_tasks.append(self._task_to_dict(task))
        
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
            TaskValidationError: If task ID is invalid
        """
        try:
            self._validate_task_id(task_id)
            
            with self._lock:
                # Double-check existence after acquiring lock
                if task_id in self._tasks:
                    self._tasks[task_id].is_finished = True
                    return True
                return False
                
        except (TaskValidationError, TaskNotFoundError):
            return False
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
        """
        with self._lock:
            all_tasks = [self._task_to_dict(task) for task in self._tasks.values()]
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: True if all tasks were successfully cleared
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
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


def main():
    """
    Demonstration of the TaskManager functionality.
    """
    print("=== Todo List Application Demo ===\n")
    
    # Initialize task manager
    task_manager = TaskManager()
    
    try:
        # Add some sample tasks
        print("Adding sample tasks...")
        task1_id = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        task2_id = task_manager.add("Complete project", "Finish the Python todo list application")
        task3_id = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added tasks with IDs: {task1_id}, {task2_id}, {task3_id}\n")
        
        # Display all tasks
        print("All tasks:")
        all_tasks = task_manager.get_all()
        for task in all_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Mark a task as finished
        print(f"Marking task {task1_id} as finished...")
        task_manager.finish(task1_id)
        
        # Search for tasks
        print("Searching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        print()
        
        # Display statistics
        total_tasks = task_manager.get_task_count()
        completed_tasks = task_manager.get_completed_count()
        print(f"Statistics: {completed_tasks}/{total_tasks} tasks completed\n")
        
        # Remove a task
        print(f"Removing task {task2_id}...")
        removed = task_manager.remove(task2_id)
        print(f"Task removal {'successful' if removed else 'failed'}\n")
        
        # Display final state
        print("Final task list:")
        final_tasks = task_manager.get_all()
        for task in final_tasks:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
    except (TaskValidationError, TaskNotFoundError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
