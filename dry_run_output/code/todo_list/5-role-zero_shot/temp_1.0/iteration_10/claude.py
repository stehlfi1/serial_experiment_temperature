
"""
High-Quality Todo List Application

A console-based todo list application implementing the TaskManager class
with comprehensive task management functionality following ISO/IEC 25010 standards.
"""

from typing import Dict, List, Optional
import re
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Task:
    """
    Data class representing a single task.
    
    Attributes:
        id: Unique identifier for the task
        task_name: Name/title of the task
        task_description: Detailed description of the task
        is_finished: Completion status of the task
        created_at: Timestamp when the task was created
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
        Convert task to dictionary format for API consistency.
        
        Returns:
            Dict containing task information in required format
        """
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }


class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(ValueError):
    """Custom exception for task not found errors."""
    pass


class TaskManager:
    """
    A high-performance task management system with comprehensive CRUD operations.
    
    This class provides efficient task management functionality including adding,
    removing, searching, and updating tasks. It uses optimized data structures
    for O(1) lookups and maintains data integrity through comprehensive validation.
    """
    
    def __init__(self):
        """
        Initialize the TaskManager with empty task storage.
        
        Uses dictionary for O(1) task lookups by ID and maintains
        a counter for unique ID generation.
        """
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._id_lock = object()  # Simple synchronization for ID generation
    
    def _generate_unique_id(self) -> int:
        """
        Generate a unique ID for a new task.
        
        Returns:
            int: A unique task identifier
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name: Name of the task to validate
            task_description: Description of the task to validate
            
        Raises:
            TaskValidationError: If validation fails
            TypeError: If inputs are not strings
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TypeError("Task name and description must be strings")
        
        # Strip whitespace and check for empty strings
        if not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or only whitespace")
        
        if not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or only whitespace")
        
        # Additional validation for reasonable length limits
        if len(task_name.strip()) > 200:
            raise TaskValidationError("Task name cannot exceed 200 characters")
        
        if len(task_description.strip()) > 1000:
            raise TaskValidationError("Task description cannot exceed 1000 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id: Task ID to validate
            
        Raises:
            TypeError: If task_id is not an integer
            TaskValidationError: If task_id is invalid
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
    
    def _validate_search_term(self, search_term: str) -> None:
        """
        Validate search term parameter.
        
        Args:
            search_term: Search term to validate
            
        Raises:
            TypeError: If search_term is not a string
            TaskValidationError: If search_term is invalid
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        if not search_term.strip():
            raise TaskValidationError("Search term cannot be empty or only whitespace")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: Name/title of the task
            task_description: Detailed description of the task
            
        Returns:
            int: Unique ID of the created task
            
        Raises:
            TaskValidationError: If input validation fails
            TypeError: If inputs are not of correct type
        """
        try:
            # Validate inputs
            self._validate_task_input(task_name, task_description)
            
            # Generate unique ID and create task
            task_id = self._generate_unique_id()
            new_task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            
            # Store task with O(1) insertion
            self._tasks[task_id] = new_task
            
            return task_id
            
        except (TaskValidationError, TypeError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Unexpected error while adding task: {str(e)}")
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task by its unique ID.
        
        Args:
            task_id: Unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False if task not found
            
        Raises:
            TaskValidationError: If task_id validation fails
            TypeError: If task_id is not an integer
        """
        try:
            # Validate task ID
            self._validate_task_id(task_id)
            
            # Check if task exists and remove with O(1) operation
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            else:
                return False
                
        except (TaskValidationError, TypeError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Unexpected error while removing task: {str(e)}")
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description using case-insensitive matching.
        
        Args:
            search_term: Term to search for in task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            TaskValidationError: If search_term validation fails
            TypeError: If search_term is not a string
        """
        try:
            # Validate search term
            self._validate_search_term(search_term)
            
            search_term_lower = search_term.strip().lower()
            matching_tasks = []
            
            # Search through all tasks with O(n) complexity
            for task in self._tasks.values():
                task_name_lower = task.task_name.lower()
                task_desc_lower = task.task_description.lower()
                
                # Check if search term is contained in name or description
                if (search_term_lower in task_name_lower or 
                    search_term_lower in task_desc_lower):
                    matching_tasks.append(task.to_dict())
            
            # Sort results by task ID for consistent ordering
            matching_tasks.sort(key=lambda x: x['id'])
            
            return matching_tasks
            
        except (TaskValidationError, TypeError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Unexpected error while searching tasks: {str(e)}")
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: Unique identifier of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished, False if task not found
            
        Raises:
            TaskValidationError: If task_id validation fails
            TypeError: If task_id is not an integer
        """
        try:
            # Validate task ID
            self._validate_task_id(task_id)
            
            # Check if task exists and update with O(1) operation
            if task_id in self._tasks:
                self._tasks[task_id].is_finished = True
                return True
            else:
                return False
                
        except (TaskValidationError, TypeError) as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Unexpected error while finishing task: {str(e)}")
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their complete information.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
        """
        try:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            # Sort by ID to maintain consistent ordering
            all_tasks.sort(key=lambda x: x['id'])
            return all_tasks
            
        except Exception as e:
            raise RuntimeError(f"Unexpected error while retrieving all tasks: {str(e)}")
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.
        
        Returns:
            bool: Always returns True indicating successful operation
        """
        try:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
            
        except Exception as e:
            raise RuntimeError(f"Unexpected error while clearing all tasks: {str(e)}")
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            int: Number of tasks currently stored
        """
        return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            int: Number of completed tasks
        """
        return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Demonstration of the TaskManager functionality.
    
    This function provides a simple interactive console interface
    to demonstrate the capabilities of the TaskManager class.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application Demo ===")
    print("Available commands: add, remove, search, finish, list, clear, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                break
            elif command == 'add':
                name = input("Task name: ")
                description = input("Task description: ")
                task_id = task_manager.add(name, description)
                print(f"Task added with ID: {task_id}")
                
            elif command == 'remove':
                task_id = int(input("Task ID to remove: "))
                success = task_manager.remove(task_id)
                print(f"Task removal: {'Success' if success else 'Failed - Task not found'}")
                
            elif command == 'search':
                search_term = input("Search term: ")
                results = task_manager.search(search_term)
                print(f"Found {len(results)} matching tasks:")
                for task in results:
                    status = "✓" if task['is_finished'] else "○"
                    print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    
            elif command == 'finish':
                task_id = int(input("Task ID to finish: "))
                success = task_manager.finish(task_id)
                print(f"Task completion: {'Success' if success else 'Failed - Task not found'}")
                
            elif command == 'list':
                tasks = task_manager.get_all()
                print(f"All tasks ({len(tasks)} total):")
                for task in tasks:
                    status = "✓" if task['is_finished'] else "○"
                    print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    
            elif command == 'clear':
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ")
                if confirm.lower() == 'yes':
                    task_manager.clear_all()
                    print("All tasks cleared successfully")
                    
            else:
                print("Unknown command. Available: add, remove, search, finish, list, clear, quit")
                
        except (TaskValidationError, TaskNotFoundError) as e:
            print(f"Validation Error: {e}")
        except ValueError as e:
            print(f"Input Error: {e}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
