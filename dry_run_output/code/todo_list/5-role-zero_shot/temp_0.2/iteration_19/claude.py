
"""
High-quality console-based todo list application implementing ISO/IEC 25010 standards.

This module provides a TaskManager class for managing todo tasks with full CRUD operations,
input validation, and efficient data handling.
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
    A thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, completing, and retrieving tasks with
    proper validation and error handling.
    """

    def __init__(self):
        """Initialize the TaskManager with empty task storage and thread safety."""
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

    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name of the task (non-empty string)
            task_description (str): Description of the task (non-empty string)
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TypeError: If inputs are not strings
            ValueError: If inputs are empty or only whitespace
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
        Remove a task from the todo list by its ID.
        
        Args:
            task_id (int): ID of the task to remove (positive integer)
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        # Input validation
        self._validate_task_id(task_id)

        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description containing the search term.
        
        Args:
            task_term (str): Search term to look for (non-empty string)
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TypeError: If task_term is not a string
            ValueError: If task_term is empty or only whitespace
        """
        # Input validation
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
            task_id (int): ID of the task to mark as finished (positive integer)
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TypeError: If task_id is not an integer
            ValueError: If task_id is not positive
        """
        # Input validation
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
        
        # Sort by task ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])

    def clear_all(self) -> bool:
        """
        Remove all tasks from the todo list.
        
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
            int: Number of tasks currently in the system
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
    
    This function shows basic usage of all TaskManager methods with
    proper error handling and user feedback.
    """
    task_manager = TaskManager()
    
    try:
        # Demonstrate adding tasks
        print("=== Todo List Manager Demo ===\n")
        
        print("Adding tasks...")
        id1 = task_manager.add("Buy groceries", "Get milk, bread, and eggs from the store")
        id2 = task_manager.add("Complete project", "Finish the Python todo list application")
        id3 = task_manager.add("Exercise", "Go for a 30-minute run in the park")
        
        print(f"Added task with ID: {id1}")
        print(f"Added task with ID: {id2}")
        print(f"Added task with ID: {id3}")
        
        # Demonstrate getting all tasks
        print("\nAll tasks:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate finishing a task
        print(f"\nMarking task {id1} as finished...")
        task_manager.finish(id1)
        
        # Demonstrate searching
        print("\nSearching for 'project':")
        search_results = task_manager.search("project")
        for task in search_results:
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Show updated task list
        print("\nUpdated task list:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
        
        # Demonstrate task statistics
        print(f"\nTask Statistics:")
        print(f"Total tasks: {task_manager.get_task_count()}")
        print(f"Completed tasks: {task_manager.get_completed_count()}")
        
        # Demonstrate removing a task
        print(f"\nRemoving task {id2}...")
        removed = task_manager.remove(id2)
        print(f"Task removed: {removed}")
        
        # Final task list
        print("\nFinal task list:")
        for task in task_manager.get_all():
            status = "✓" if task['is_finished'] else "○"
            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
            
    except (TypeError, ValueError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
