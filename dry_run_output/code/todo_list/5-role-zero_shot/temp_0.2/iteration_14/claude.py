
"""
High-quality Todo List Application
Implements a console-based task management system following ISO/IEC 25010 standards.
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
        """Convert task to dictionary format for external consumption."""
        return {
            'id': self.id,
            'task_name': self.task_name,
            'task_description': self.task_description,
            'is_finished': self.is_finished
        }


class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception for when a task is not found."""
    pass


class TaskManager:
    """
    Thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, and updating tasks. All operations are
    thread-safe and include proper validation.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name: The name of the task
            task_description: The description of the task
            
        Raises:
            TaskValidationError: If inputs are invalid
        """
        if not isinstance(task_name, str) or not isinstance(task_description, str):
            raise TaskValidationError("Task name and description must be strings")
        
        if not task_name.strip():
            raise TaskValidationError("Task name cannot be empty or whitespace only")
        
        if not task_description.strip():
            raise TaskValidationError("Task description cannot be empty or whitespace only")
        
        if len(task_name.strip()) > 100:
            raise TaskValidationError("Task name cannot exceed 100 characters")
        
        if len(task_description.strip()) > 500:
            raise TaskValidationError("Task description cannot exceed 500 characters")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id: The ID to validate
            
        Raises:
            TaskValidationError: If ID is invalid
        """
        if not isinstance(task_id, int):
            raise TaskValidationError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
    
    def _get_next_id(self) -> int:
        """
        Generate the next unique task ID.
        
        Returns:
            The next available task ID
        """
        current_id = self._next_id
        self._next_id += 1
        return current_id
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name: Name/title of the task
            task_description: Detailed description of the task
            
        Returns:
            Unique ID of the created task
            
        Raises:
            TaskValidationError: If input validation fails
        """
        self._validate_task_input(task_name, task_description)
        
        with self._lock:
            task_id = self._get_next_id()
            task = Task(
                id=task_id,
                task_name=task_name.strip(),
                task_description=task_description.strip()
            )
            self._tasks[task_id] = task
            return task_id
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the todo list.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            True if task was successfully removed, False if task not found
            
        Raises:
            TaskValidationError: If task_id is invalid
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
            task_term: Search term to match against task name or description
            
        Returns:
            List of dictionaries containing matching task information
            
        Raises:
            TaskValidationError: If search term is invalid
        """
        if not isinstance(task_term, str):
            raise TaskValidationError("Search term must be a string")
        
        if not task_term.strip():
            raise TaskValidationError("Search term cannot be empty or whitespace only")
        
        search_term_lower = task_term.strip().lower()
        matching_tasks = []
        
        with self._lock:
            for task in self._tasks.values():
                if (search_term_lower in task.task_name.lower() or 
                    search_term_lower in task.task_description.lower()):
                    matching_tasks.append(task.to_dict())
        
        # Sort by task ID for consistent ordering
        return sorted(matching_tasks, key=lambda x: x['id'])
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to mark as finished
            
        Returns:
            True if task was successfully marked as finished, False if task not found
            
        Raises:
            TaskValidationError: If task_id is invalid
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
            List of dictionaries containing all task information,
            sorted by task ID
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            True indicating successful clearing of all tasks
        """
        with self._lock:
            self._tasks.clear()
            self._next_id = 1  # Reset ID counter
            return True
    
    def get_task_count(self) -> int:
        """
        Get the total number of tasks.
        
        Returns:
            Total number of tasks in the system
        """
        with self._lock:
            return len(self._tasks)
    
    def get_completed_count(self) -> int:
        """
        Get the number of completed tasks.
        
        Returns:
            Number of tasks marked as finished
        """
        with self._lock:
            return sum(1 for task in self._tasks.values() if task.is_finished)


def main():
    """
    Console interface for the Todo List application.
    Demonstrates usage of the TaskManager class.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == "quit":
                print("Goodbye!")
                break
            
            elif command == "add":
                name = input("Task name: ")
                description = input("Task description: ")
                try:
                    task_id = task_manager.add(name, description)
                    print(f"Task added successfully with ID: {task_id}")
                except TaskValidationError as e:
                    print(f"Error: {e}")
            
            elif command == "remove":
                try:
                    task_id = int(input("Task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("Task removed successfully")
                    else:
                        print("Task not found")
                except (ValueError, TaskValidationError) as e:
                    print(f"Error: {e}")
            
            elif command == "search":
                term = input("Search term: ")
                try:
                    results = task_manager.search(term)
                    if results:
                        print(f"\nFound {len(results)} matching task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No matching tasks found")
                except TaskValidationError as e:
                    print(f"Error: {e}")
            
            elif command == "finish":
                try:
                    task_id = int(input("Task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("Task marked as finished")
                    else:
                        print("Task not found")
                except (ValueError, TaskValidationError) as e:
                    print(f"Error: {e}")
            
            elif command == "list":
                tasks = task_manager.get_all()
                if tasks:
                    print(f"\nAll tasks ({len(tasks)} total):")
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
            
            else:
                print("Unknown command. Available commands: add, remove, search, finish, list, clear, quit")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
