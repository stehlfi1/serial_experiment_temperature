"""
This module contains the Challenge class, which is used to represent a challenge/task.
"""

from typing import List
from .prompt import Prompt


class Challenge:
    """
    This class represents a challenge/task.
    """

    def __init__(self, name: str, prompts: List[Prompt]):
        """
        Initializes a new instance of the challenge.

        Args:
            name (str): The name associated with the instance.
            prompts (List[Prompt]): A list of Prompt objects associated with the instance.
        """
        self.name = name
        self.prompts = prompts
