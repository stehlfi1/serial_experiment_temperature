import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

load_dotenv()


class Llm:
    def __init__(self, model: str, name: str, temperature: float = 0.7, 
                 top_p: Optional[float] = None, top_k: Optional[int] = None):
        self.model = model
        self.name = name
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.client = OpenAI(
            base_url=os.getenv("OPENROUTER_API_URL"),
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    def query(self, question: str, system_prompt: str = "You are an AI assistant.") -> ChatCompletion:
        params = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question},
            ],
            "temperature": self.temperature,
        }
        
        if self.top_p is not None:
            params["top_p"] = self.top_p
            
        if self.top_k is not None:
            params["extra_body"] = {"top_k": self.top_k}
        
        return self.client.chat.completions.create(**params)
