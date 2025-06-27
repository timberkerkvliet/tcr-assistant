import openai
from openai import Client

from xp_assistent.llm_client import LLMClient
from xp_assistent.llm_conversation import LLMConversation
from xp_assistent.openai_conversation import OpenAIConversation


class OpenAIClient(LLMClient):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        self._client = Client(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def new_conversation(self) -> LLMConversation:
        return OpenAIConversation(self._client, self.model, self.temperature, self.max_tokens)
