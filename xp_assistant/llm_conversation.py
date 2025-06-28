from abc import ABC, abstractmethod
from typing import List, Dict

class LLMConversation(ABC):
    @abstractmethod
    def chat(self, message: str) -> str:
        """Send a new message"""
