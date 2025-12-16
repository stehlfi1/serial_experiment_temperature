
"""
Todo List Application - Console-based task management system
Implements ISO/IEC 25010 quality standards for software development
"""

from typing import List, Dict, Optional
import re
from datetime import datetime


class Task:
    """
    Represents a single task with all its properties.
    
    This class encapsulates task data and provides a clean interface
    for task manipulation while ensuring data integrity.
    """
    
    def __init__(self, task_id: int, name: str, description: str) -> None:
        """
        Initialize a new task.
        
        Args:
            task_id: Unique identifier for the task
            name: Task name/title
            description: Detailed task description
        """
        self.id = task_id
        self.name = name
        self.description = description
        self.is_finished = False
        self.created_at = datetime.now()
        self.finished_at: Optional[datetime] = None
    
    def mark_finished(self) -> None:
        """Mark the task as completed."""
        self.is_finished = True
        self.finished_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """
        Convert task to dictionary format for external consumption.
        
        Returns:
            Dictionary containing all task information
        """
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished,
            'created_at': self.created_at.isoformat(),
            'finished_at': self.finished_at.isoformat() if self.finished_at else None
        }


class TaskValidationError(ValueError):
    """Custom exception for task validation errors."""
    pass


class TaskNotFoundError(KeyError):
    """Custom exception for when a task is not found."""
    pass


class TaskManager:
    """
    High-performance task management system with comprehensive functionality.
    
    This class provides a complete interface for managing tasks with efficient
    data structures and robust error handling following ISO/IEC 25010 standards.
    """
    
    def __init__(self) -> None:
        """Initialize the task manager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id = 1
        self._name_index: Dict[str, set] = {}  # For efficient search by name
        self._description_index: Dict[str, set] = {}  # For efficient search by description
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name: The task name to validate
            task_description: The task description to validate
            
        Raises:
            TaskValidationError: If validation fails
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
            task_id: The task ID to validate
            
        Raises:
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
        """
        if not isinstance(task_id, int):
            raise TaskValidationError("Task ID must be an integer")
        
        if task_id <= 0:
            raise TaskValidationError("Task ID must be a positive integer")
        
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def _update_search_indices(self, task: Task) -> None:
        """
        Update search indices for efficient task lookup.
        
        Args:
            task: The task to index
        """
        # Index individual words for better search capability
        name_words = re.findall(r'\w+', task.name.lower())
        desc_words = re.findall(r'\w+', task.description.lower())
        
        for word in name_words:
            if word not in self._name_index:
                self._name_index[word] = set()
            self._name_index[word].add(task.id)
        
        for word in desc_words:
            if word not in self._description_index:
                self._description_index[word] = set()
            self._description_index[word].add(task.id)
    
    def _remove_from_search_indices(self, task: Task) -> None:
        """
        Remove task from search indices.
        
        Args:
            task: The task to remove from indices
        """
        name_words = re.findall(r'\w+', task.name.lower())
        desc_words = re.findall(r'\w+', task.description.lower())
        
        for word in name_words:
            if word in self._name_index:
                self._name_index[word].discard(task.id)
                if not self._name_index[word]:
                    del self._name_index[word]
        
        for word in desc_words:
            if word in self._description_index:
                self._description_index[word].discard(task.id)
                if not self._description_index[word]:
                    del self._description_index[word]
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the task manager.
        
        Args:
            task_name: The name/title of the task
            task_description: Detailed description of the task
            
        Returns:
            The unique ID assigned to the new task
            
        Raises:
            TaskValidationError: If input validation fails
        """
        try:
            # Validate inputs
            self._validate_task_input(task_name, task_description)
            
            # Create and store the task
            task_id = self._next_id
            task = Task(task_id, task_name.strip(), task_description.strip())
            
            self._tasks[task_id] = task
            self._update_search_indices(task)
            self._next_id += 1
            
            return task_id
            
        except Exception as e:
            # Re-raise known exceptions, wrap unknown ones
            if isinstance(e, (TaskValidationError, TaskNotFoundError)):
                raise
            raise TaskValidationError(f"Failed to add task: {str(e)}")
    
    def remove(self, task_id: int) -> bool:
        """
        Remove a task from the task manager.
        
        Args:
            task_id: The unique ID of the task to remove
            
        Returns:
            True if the task was successfully removed
            
        Raises:
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
        """
        try:
            # Validate task ID and existence
            self._validate_task_id(task_id)
            
            # Remove from indices and storage
            task = self._tasks[task_id]
            self._remove_from_search_indices(task)
            del self._tasks[task_id]
            
            return True
            
        except Exception as e:
            # Re-raise known exceptions, wrap unknown ones
            if isinstance(e, (TaskValidationError, TaskNotFoundError)):
                raise
            raise TaskValidationError(f"Failed to remove task: {str(e)}")
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search for tasks by name or description.
        
        Args:
            task_term: Search term to look for in task names and descriptions
            
        Returns:
            List of dictionaries containing matching task information
            
        Raises:
            TaskValidationError: If search term is invalid
        """
        try:
            if not isinstance(task_term, str):
                raise TaskValidationError("Search term must be a string")
            
            if not task_term.strip():
                raise TaskValidationError("Search term cannot be empty or whitespace only")
            
            search_term = task_term.strip().lower()
            matching_ids = set()
            
            # Search using indices for better performance
            search_words = re.findall(r'\w+', search_term)
            
            for word in search_words:
                # Find in name index
                if word in self._name_index:
                    matching_ids.update(self._name_index[word])
                
                # Find in description index
                if word in self._description_index:
                    matching_ids.update(self._description_index[word])
            
            # Also perform substring search for partial matches
            for task_id, task in self._tasks.items():
                if (search_term in task.name.lower() or 
                    search_term in task.description.lower()):
                    matching_ids.add(task_id)
            
            # Return sorted results for consistent output
            results = []
            for task_id in sorted(matching_ids):
                if task_id in self._tasks:  # Safety check
                    results.append(self._tasks[task_id].to_dict())
            
            return results
            
        except Exception as e:
            # Re-raise known exceptions, wrap unknown ones
            if isinstance(e, (TaskValidationError, TaskNotFoundError)):
                raise
            raise TaskValidationError(f"Failed to search tasks: {str(e)}")
    
    def finish(self, task_id: int) -> bool:
        """
        Mark a task as completed.
        
        Args:
            task_id: The unique ID of the task to mark as finished
            
        Returns:
            True if the task was successfully marked as finished
            
        Raises:
            TaskValidationError: If task_id is invalid
            TaskNotFoundError: If task doesn't exist
        """
        try:
            # Validate task ID and existence
            self._validate_task_id(task_id)
            
            # Mark task as finished
            self._tasks[task_id].mark_finished()
            return True
            
        except Exception as e:
            # Re-raise known exceptions, wrap unknown ones
            if isinstance(e, (TaskValidationError, TaskNotFoundError)):
                raise
            raise TaskValidationError(f"Failed to finish task: {str(e)}")
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List of dictionaries containing all task information,
            sorted by task ID for consistent output
        """
        try:
            results = []
            for task_id in sorted(self._tasks.keys()):
                results.append(self._tasks[task_id].to_dict())
            return results
            
        except Exception as e:
            raise TaskValidationError(f"Failed to retrieve tasks: {str(e)}")
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the task manager.
        
        Returns:
            True if all tasks were successfully cleared
        """
        try:
            self._tasks.clear()
            self._name_index.clear()
            self._description_index.clear()
            self._next_id = 1
            return True
            
        except Exception as e:
            raise TaskValidationError(f"Failed to clear all tasks: {str(e)}")
    
    def get_stats(self) -> Dict:
        """
        Get statistics about the current tasks.
        
        Returns:
            Dictionary containing task statistics
        """
        total_tasks = len(self._tasks)
        finished_tasks = sum(1 for task in self._tasks.values() if task.is_finished)
        pending_tasks = total_tasks - finished_tasks
        
        return {
            'total_tasks': total_tasks,
            'finished_tasks': finished_tasks,
            'pending_tasks': pending_tasks,
            'completion_rate': finished_tasks / total_tasks if total_tasks > 0 else 0
        }


def main():
    """
    Console interface for the Todo List application.
    Provides an interactive command-line interface for task management.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Commands: add, remove, search, finish, list, clear, stats, help, quit")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().lower()
            
            if command == 'quit' or command == 'exit':
                print("Goodbye!")
                break
            
            elif command == 'help':
                print("\nAvailable commands:")
                print("  add - Add a new task")
                print("  remove - Remove a task by ID")
                print("  search - Search tasks by keyword")
                print("  finish - Mark a task as completed")
                print("  list - Show all tasks")
                print("  clear - Delete all tasks")
                print("  stats - Show task statistics")
                print("  help - Show this help message")
                print("  quit - Exit the application")
                print()
            
            elif command == 'add':
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                
                task_id = task_manager.add(name, description)
                print(f"✓ Task added successfully with ID: {task_id}")
            
            elif command == 'remove':
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    task_manager.remove(task_id)
                    print(f"✓ Task {task_id} removed successfully")
                except ValueError:
                    print("✗ Please enter a valid task ID (number)")
            
            elif command == 'search':
                term = input("Enter search term: ").strip()
                results = task_manager.search(term)
                
                if results:
                    print(f"\nFound {len(results)} matching task(s):")
                    for task in results:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}")
                        print(f"      {task['task_description']}")
                else:
                    print("No tasks found matching your search term")
            
            elif command == 'finish':
                try:
                    task_id = int(input("Enter task ID to finish: "))
                    task_manager.finish(task_id)
                    print(f"✓ Task {task_id} marked as completed")
                except ValueError:
                    print("✗ Please enter a valid task ID (number)")
            
            elif command == 'list':
                tasks = task_manager.get_all()
                
                if tasks:
                    print(f"\nAll tasks ({len(tasks)}):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}")
                        print(f"      {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == 'clear':
                confirm = input("Are you sure you want to delete all tasks? (yes/no): ")
                if confirm.lower() in ['yes', 'y']:
                    task_manager.clear_all()
                    print("✓ All tasks cleared successfully")
                else:
                    print("Operation cancelled")
            
            elif command == 'stats':
                stats = task_manager.get_stats()
                print(f"\nTask Statistics:")
                print(f"  Total tasks: {stats['total_tasks']}")
                print(f"  Completed: {stats['finished_tasks']}")
                print(f"  Pending: {stats['pending_tasks']}")
                print(f"  Completion rate: {stats['completion_rate']:.1%}")
            
            else:
                print("Unknown command. Type 'help' for available commands.")
            
            print()  # Add spacing between commands
            
        except (TaskValidationError, TaskNotFoundError) as e:
            print(f"✗ Error: {e}")
            print()
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        
        except Exception as e:
            print(f"✗ Unexpected error: {e}")
            print("Please try again or contact support if the problem persists.")
            print()


if __name__ == "__main__":
    main()
