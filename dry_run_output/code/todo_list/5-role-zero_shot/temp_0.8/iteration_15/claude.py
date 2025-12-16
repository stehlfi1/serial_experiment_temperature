
"""
High-quality Todo List Application
A console-based task management system following ISO/IEC 25010 standards.
"""

from typing import List, Dict, Optional
import logging
from datetime import datetime


class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception for when a task is not found."""
    pass


class Task:
    """
    Represents a single task with all its properties.
    
    This class encapsulates task data and provides a clean interface
    for task operations while maintaining data integrity.
    """
    
    def __init__(self, task_id: int, name: str, description: str):
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            name: Task name (cannot be empty)
            description: Task description (cannot be empty)
            
        Raises:
            TaskValidationError: If name or description is empty
        """
        if not name or not name.strip():
            raise TaskValidationError("Task name cannot be empty")
        if not description or not description.strip():
            raise TaskValidationError("Task description cannot be empty")
        
        self._id = task_id
        self._name = name.strip()
        self._description = description.strip()
        self._is_finished = False
        self._created_at = datetime.now()
        self._finished_at: Optional[datetime] = None
    
    @property
    def id(self) -> int:
        """Get task ID."""
        return self._id
    
    @property
    def name(self) -> str:
        """Get task name."""
        return self._name
    
    @property
    def description(self) -> str:
        """Get task description."""
        return self._description
    
    @property
    def is_finished(self) -> bool:
        """Get task completion status."""
        return self._is_finished
    
    def mark_finished(self) -> None:
        """Mark the task as completed."""
        if not self._is_finished:
            self._is_finished = True
            self._finished_at = datetime.now()
    
    def matches_search_term(self, search_term: str) -> bool:
        """
        Check if task matches the given search term.
        
        Args:
            search_term: Term to search for in name and description
            
        Returns:
            True if the search term is found in name or description
        """
        if not search_term or not search_term.strip():
            return False
        
        term_lower = search_term.strip().lower()
        return (term_lower in self._name.lower() or 
                term_lower in self._description.lower())
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary representation.
        
        Returns:
            Dictionary containing all task information
        """
        return {
            'id': self._id,
            'task_name': self._name,
            'task_description': self._description,
            'is_finished': self._is_finished
        }


class TaskManager:
    """
    High-performance task management system.
    
    This class provides efficient task operations with O(1) lookups,
    comprehensive error handling, and robust validation following
    ISO/IEC 25010 standards.
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}  # O(1) lookup by ID
        self._next_id = 1
        self._logger = self._setup_logger()
        
        # Performance optimization: maintain separate indexes
        self._name_index: Dict[str, List[int]] = {}  # For faster name-based searches
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the TaskManager."""
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID.
        
        Args:
            task_id: ID to validate
            
        Raises:
            TaskValidationError: If task_id is not a positive integer
            TaskNotFoundError: If task doesn't exist
        """
        if not isinstance(task_id, int) or task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def _update_name_index(self, task: Task) -> None:
        """Update the name index for faster searches."""
        name_key = task.name.lower()
        if name_key not in self._name_index:
            self._name_index[name_key] = []
        self._name_index[name_key].append(task.id)
    
    def _remove_from_name_index(self, task: Task) -> None:
        """Remove task from name index."""
        name_key = task.name.lower()
        if name_key in self._name_index:
            try:
                self._name_index[name_key].remove(task.id)
                if not self._name_index[name_key]:
                    del self._name_index[name_key]
            except ValueError:
                # Task ID not in index, log but don't fail
                self._logger.warning(f"Task ID {task.id} not found in name index")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the system.
        
        Args:
            task_name: Name of the task (cannot be empty)
            task_description: Description of the task (cannot be empty)
            
        Returns:
            Unique ID assigned to the new task
            
        Raises:
            TaskValidationError: If task_name or task_description is invalid
            TypeError: If arguments are not strings
        """
        # Type validation
        if not isinstance(task_name, str):
            raise TypeError("Task name must be a string")
        if not isinstance(task_description, str):
            raise TypeError("Task description must be a string")
        
        try:
            # Create new task (validation happens in Task constructor)
            task = Task(self._next_id, task_name, task_description)
            
            # Store task with O(1) insertion
            self._tasks[self._next_id] = task
            
            # Update search index
            self._update_name_index(task)
            
            # Increment ID counter
            current_id = self._next_id
            self._next_id += 1
            
            self._logger.info(f"Task added successfully with ID: {current_id}")
            return current_id
            
        except TaskValidationError as e:
            self._logger.error(f"Failed to add task: {e}")
            raise
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the system.
        
        Args:
            task_id: ID of the task to remove
            
        Returns:
            True if task was successfully removed, False otherwise
            
        Raises:
            TaskValidationError: If task_id is invalid
            TypeError: If task_id is not an integer
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        try:
            self._validate_task_id(task_id)
            
            # Get task for index cleanup
            task = self._tasks[task_id]
            
            # Remove from indexes
            self._remove_from_name_index(task)
            
            # Remove from main storage - O(1) deletion
            del self._tasks[task_id]
            
            self._logger.info(f"Task {task_id} removed successfully")
            return True
            
        except (TaskValidationError, TaskNotFoundError) as e:
            self._logger.error(f"Failed to remove task {task_id}: {e}")
            raise
    
    def search(self, search_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            search_term: Term to search for (case-insensitive)
            
        Returns:
            List of dictionaries containing matching task information
            
        Raises:
            TypeError: If search_term is not a string
            TaskValidationError: If search_term is empty
        """
        if not isinstance(search_term, str):
            raise TypeError("Search term must be a string")
        
        if not search_term or not search_term.strip():
            raise TaskValidationError("Search term cannot be empty")
        
        try:
            matching_tasks = []
            
            # Efficient search through all tasks
            for task in self._tasks.values():
                if task.matches_search_term(search_term):
                    matching_tasks.append(task.to_dict())
            
            # Sort by ID for consistent results
            matching_tasks.sort(key=lambda x: x['id'])
            
            self._logger.info(
                f"Search for '{search_term}' returned {len(matching_tasks)} results"
            )
            return matching_tasks
            
        except Exception as e:
            self._logger.error(f"Search failed: {e}")
            raise
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: ID of the task to mark as finished
            
        Returns:
            True if task was successfully marked as finished
            
        Raises:
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
            TypeError: If task_id is not an integer
        """
        if not isinstance(task_id, int):
            raise TypeError("Task ID must be an integer")
        
        try:
            self._validate_task_id(task_id)
            
            # Get task and mark as finished - O(1) operation
            task = self._tasks[task_id]
            was_finished = task.is_finished
            task.mark_finished()
            
            if not was_finished:
                self._logger.info(f"Task {task_id} marked as finished")
            else:
                self._logger.info(f"Task {task_id} was already finished")
            
            return True
            
        except (TaskValidationError, TaskNotFoundError) as e:
            self._logger.error(f"Failed to finish task {task_id}: {e}")
            raise
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks in the system.
        
        Returns:
            List of dictionaries containing all task information,
            sorted by task ID for consistent ordering
        """
        try:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
            
            # Sort by ID for consistent results
            all_tasks.sort(key=lambda x: x['id'])
            
            self._logger.info(f"Retrieved {len(all_tasks)} tasks")
            return all_tasks
            
        except Exception as e:
            self._logger.error(f"Failed to retrieve all tasks: {e}")
            raise
    
    def clear_all(self) -> bool:
        """
        Remove all tasks from the system.
        
        Returns:
            True if all tasks were successfully cleared
        """
        try:
            task_count = len(self._tasks)
            
            # Clear all data structures
            self._tasks.clear()
            self._name_index.clear()
            self._next_id = 1  # Reset ID counter
            
            self._logger.info(f"Cleared {task_count} tasks from the system")
            return True
            
        except Exception as e:
            self._logger.error(f"Failed to clear all tasks: {e}")
            raise
    
    def get_statistics(self) -> Dict:
        """
        Get system statistics for monitoring and debugging.
        
        Returns:
            Dictionary containing system statistics
        """
        total_tasks = len(self._tasks)
        finished_tasks = sum(1 for task in self._tasks.values() if task.is_finished)
        pending_tasks = total_tasks - finished_tasks
        
        return {
            'total_tasks': total_tasks,
            'finished_tasks': finished_tasks,
            'pending_tasks': pending_tasks,
            'next_id': self._next_id
        }


def main():
    """
    Console interface for the Todo List application.
    Demonstrates usage of the TaskManager class.
    """
    task_manager = TaskManager()
    
    print("Welcome to the Todo List Application!")
    print("Available commands: add, remove, search, finish, list, clear, stats, quit")
    
    while True:
        try:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                print("Goodbye!")
                break
                
            elif command == 'add':
                name = input("Enter task name: ")
                description = input("Enter task description: ")
                task_id = task_manager.add(name, description)
                print(f"Task added with ID: {task_id}")
                
            elif command == 'remove':
                task_id = int(input("Enter task ID to remove: "))
                if task_manager.remove(task_id):
                    print("Task removed successfully")
                    
            elif command == 'search':
                term = input("Enter search term: ")
                results = task_manager.search(term)
                if results:
                    print(f"\nFound {len(results)} matching tasks:")
                    for task in results:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                else:
                    print("No matching tasks found")
                    
            elif command == 'finish':
                task_id = int(input("Enter task ID to finish: "))
                if task_manager.finish(task_id):
                    print("Task marked as finished")
                    
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
                confirm = input("Are you sure you want to clear all tasks? (yes/no): ")
                if confirm.lower() == 'yes':
                    if task_manager.clear_all():
                        print("All tasks cleared")
                else:
                    print("Operation cancelled")
                    
            elif command == 'stats':
                stats = task_manager.get_statistics()
                print(f"\nSystem Statistics:")
                print(f"  Total tasks: {stats['total_tasks']}")
                print(f"  Finished tasks: {stats['finished_tasks']}")
                print(f"  Pending tasks: {stats['pending_tasks']}")
                
            else:
                print("Unknown command. Available: add, remove, search, finish, list, clear, stats, quit")
                
        except (TaskValidationError, TaskNotFoundError, TypeError) as e:
            print(f"Error: {e}")
        except ValueError:
            print("Error: Please enter a valid number for task ID")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
