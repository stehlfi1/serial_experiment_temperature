
"""
Todo List Application

A console-based todo list application implementing a TaskManager class
that provides comprehensive task management functionality with robust
error handling and validation.

This module adheres to ISO/IEC 25010 quality standards focusing on
functionality, reliability, usability, efficiency, and maintainability.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import threading
from datetime import datetime


@dataclass
class Task:
    """
    Represents a task in the todo list.
    
    Attributes:
        id (int): Unique identifier for the task
        name (str): Name/title of the task
        description (str): Detailed description of the task
        is_finished (bool): Completion status of the task
        created_at (datetime): Timestamp when task was created
    """
    id: int
    name: str
    description: str
    is_finished: bool = False
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary format for API responses."""
        return {
            'id': self.id,
            'task_name': self.name,
            'task_description': self.description,
            'is_finished': self.is_finished,
            'created_at': self.created_at.isoformat()
        }


class TaskManagerError(Exception):
    """Base exception class for TaskManager operations."""
    pass


class InvalidInputError(TaskManagerError):
    """Raised when invalid input is provided."""
    pass


class TaskNotFoundError(TaskManagerError):
    """Raised when a task with specified ID is not found."""
    pass


class TaskManager:
    """
    A thread-safe task management system for todo list operations.
    
    This class provides comprehensive task management functionality including
    adding, removing, searching, finishing, and retrieving tasks. It ensures
    data integrity through input validation and thread safety through locking.
    
    Attributes:
        _tasks (Dict[int, Task]): Internal storage for tasks indexed by ID
        _next_id (int): Counter for generating unique task IDs
        _lock (threading.RLock): Thread safety lock for concurrent operations
    """
    
    def __init__(self):
        """Initialize the TaskManager with empty task storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1
        self._lock = threading.RLock()
    
    def _validate_task_input(self, task_name: str, task_description: str) -> None:
        """
        Validate task input parameters.
        
        Args:
            task_name (str): Name of the task to validate
            task_description (str): Description of the task to validate
            
        Raises:
            InvalidInputError: If inputs are invalid (empty strings, wrong types)
        """
        if not isinstance(task_name, str):
            raise InvalidInputError("Task name must be a string")
        if not isinstance(task_description, str):
            raise InvalidInputError("Task description must be a string")
        if not task_name.strip():
            raise InvalidInputError("Task name cannot be empty or whitespace only")
        if not task_description.strip():
            raise InvalidInputError("Task description cannot be empty or whitespace only")
    
    def _validate_task_id(self, task_id: int) -> None:
        """
        Validate task ID parameter.
        
        Args:
            task_id (int): Task ID to validate
            
        Raises:
            InvalidInputError: If task_id is invalid (negative, non-integer)
            TaskNotFoundError: If task with given ID doesn't exist
        """
        if not isinstance(task_id, int):
            raise InvalidInputError("Task ID must be an integer")
        if task_id < 1:
            raise InvalidInputError("Task ID must be positive")
        if task_id not in self._tasks:
            raise TaskNotFoundError(f"Task with ID {task_id} not found")
    
    def add(self, task_name: str, task_description: str) -> int:
        """
        Add a new task to the todo list.
        
        Args:
            task_name (str): Name/title of the task (non-empty)
            task_description (str): Detailed description of the task (non-empty)
            
        Returns:
            int: Unique ID of the newly created task
            
        Raises:
            InvalidInputError: If task_name or task_description are invalid
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Buy groceries", "Buy milk, bread, and eggs")
            >>> task_id
            1
        """
        self._validate_task_input(task_name, task_description)
        
        with self._lock:
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
        Remove a task from the todo list.
        
        Args:
            task_id (int): Unique identifier of the task to remove
            
        Returns:
            bool: True if task was successfully removed, False otherwise
            
        Raises:
            InvalidInputError: If task_id is invalid
            TaskNotFoundError: If task with given ID doesn't exist
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Test task", "Test description")
            >>> tm.remove(task_id)
            True
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            del self._tasks[task_id]
            return True
    
    def search(self, task_term: str) -> List[Dict]:
        """
        Search tasks by name or description.
        
        Performs case-insensitive partial matching on both task name and description.
        
        Args:
            task_term (str): Search term to match against task names and descriptions
            
        Returns:
            List[Dict]: List of matching tasks in dictionary format
            
        Raises:
            InvalidInputError: If search term is invalid (empty or non-string)
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Buy groceries", "Buy milk and bread")
            >>> tm.search("milk")
            [{'id': 1, 'task_name': 'Buy groceries', 'task_description': 'Buy milk and bread', 'is_finished': False, 'created_at': '...'}]
        """
        if not isinstance(task_term, str):
            raise InvalidInputError("Search term must be a string")
        if not task_term.strip():
            raise InvalidInputError("Search term cannot be empty or whitespace only")
        
        search_term_lower = task_term.strip().lower()
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
            task_id (int): Unique identifier of the task to mark as finished
            
        Returns:
            bool: True if task was successfully marked as finished
            
        Raises:
            InvalidInputError: If task_id is invalid
            TaskNotFoundError: If task with given ID doesn't exist
            
        Example:
            >>> tm = TaskManager()
            >>> task_id = tm.add("Complete project", "Finish the final report")
            >>> tm.finish(task_id)
            True
        """
        self._validate_task_id(task_id)
        
        with self._lock:
            self._tasks[task_id].is_finished = True
            return True
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all tasks with their details.
        
        Returns:
            List[Dict]: List of all tasks in dictionary format, sorted by ID
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.add("Task 2", "Description 2")
            >>> tasks = tm.get_all()
            >>> len(tasks)
            2
        """
        with self._lock:
            all_tasks = [task.to_dict() for task in self._tasks.values()]
        
        # Sort by ID for consistent ordering
        return sorted(all_tasks, key=lambda x: x['id'])
    
    def clear_all(self) -> bool:
        """
        Delete all tasks from the todo list.
        
        Returns:
            bool: True if all tasks were successfully cleared
            
        Example:
            >>> tm = TaskManager()
            >>> tm.add("Task 1", "Description 1")
            >>> tm.clear_all()
            True
            >>> tm.get_all()
            []
        """
        with self._lock:
            self._tasks.clear()
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
    Console interface for the Todo List Application.
    
    Provides a simple command-line interface for interacting with the TaskManager.
    Demonstrates usage of all TaskManager methods with proper error handling.
    """
    task_manager = TaskManager()
    
    print("=== Todo List Application ===")
    print("Available commands:")
    print("1. add - Add a new task")
    print("2. remove - Remove a task by ID")
    print("3. search - Search tasks by term")
    print("4. finish - Mark a task as completed")
    print("5. list - Show all tasks")
    print("6. clear - Remove all tasks")
    print("7. stats - Show task statistics")
    print("8. exit - Exit the application")
    print()
    
    while True:
        try:
            command = input("Enter command: ").strip().lower()
            
            if command == "add":
                name = input("Enter task name: ").strip()
                description = input("Enter task description: ").strip()
                try:
                    task_id = task_manager.add(name, description)
                    print(f"✓ Task added with ID: {task_id}")
                except InvalidInputError as e:
                    print(f"✗ Error: {e}")
            
            elif command == "remove":
                try:
                    task_id = int(input("Enter task ID to remove: "))
                    if task_manager.remove(task_id):
                        print("✓ Task removed successfully")
                except (ValueError, InvalidInputError, TaskNotFoundError) as e:
                    print(f"✗ Error: {e}")
            
            elif command == "search":
                term = input("Enter search term: ").strip()
                try:
                    results = task_manager.search(term)
                    if results:
                        print(f"\n Found {len(results)} matching task(s):")
                        for task in results:
                            status = "✓" if task['is_finished'] else "○"
                            print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                    else:
                        print("No matching tasks found")
                except InvalidInputError as e:
                    print(f"✗ Error: {e}")
            
            elif command == "finish":
                try:
                    task_id = int(input("Enter task ID to finish: "))
                    if task_manager.finish(task_id):
                        print("✓ Task marked as completed")
                except (ValueError, InvalidInputError, TaskNotFoundError) as e:
                    print(f"✗ Error: {e}")
            
            elif command == "list":
                tasks = task_manager.get_all()
                if tasks:
                    print(f"\n All tasks ({len(tasks)}):")
                    for task in tasks:
                        status = "✓" if task['is_finished'] else "○"
                        print(f"  {status} [{task['id']}] {task['task_name']}: {task['task_description']}")
                else:
                    print("No tasks found")
            
            elif command == "clear":
                confirm = input("Are you sure you want to delete all tasks? (y/N): ").strip().lower()
                if confirm == 'y':
                    if task_manager.clear_all():
                        print("✓ All tasks cleared")
                else:
                    print("Operation cancelled")
            
            elif command == "stats":
                total = task_manager.get_task_count()
                completed = task_manager.get_completed_count()
                pending = total - completed
                print(f"\n📊 Task Statistics:")
                print(f"  Total tasks: {total}")
                print(f"  Completed: {completed}")
                print(f"  Pending: {pending}")
                if total > 0:
                    completion_rate = (completed / total) * 100
                    print(f"  Completion rate: {completion_rate:.1f}%")
            
            elif command == "exit":
                print("Goodbye!")
                break
            
            else:
                print("✗ Unknown command. Please try again.")
            
            print()  # Add spacing between commands
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"✗ Unexpected error: {e}")


if __name__ == "__main__":
    main()
