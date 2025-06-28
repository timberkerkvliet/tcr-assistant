from abc import ABC, abstractmethod

from xp_assistant.llm_conversation import LLMConversation


class LLMClient(ABC):
    @abstractmethod
    def new_conversation(self) -> LLMConversation:
        """Interface for talking to a LLM"""
