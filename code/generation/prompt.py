"""
This module contains the Prompt class.
"""


class Prompt:
    """
    A class representing a prompt which is send to AI.
    """

    def __init__(self, name: str, prompt: str):
        """
        Initializes a new instance of the class.

        Args:
            name (str): The name associated with the instance.
            prompt (str): The prompt or message associated with the instance.
        """
        self.name = name
        self.prompt = prompt
