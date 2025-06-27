import time

import openai
from openai import OpenAIError, Client

from xp_assistent.llm_conversation import LLMConversation


class OpenAIConversation(LLMConversation):
    def __init__(
        self,
        client: Client,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        self._client = client
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.messages = []

    def chat(
        self,
        message: str
    ) -> str:
        self.messages.append({"role": "user", "content": message})
        for attempt in range(3):
            try:
                response = self._client.responses.create(
                    model=self.model,
                    instructions="You are a coding assistant that talks like a pirate.",
                    input=message,
                )
                response_message = response.output_text
                self.messages.append(response_message)
                return response_message
            except OpenAIError as e:
                print(f"OpenAI API error: {e}")
                time.sleep(2 ** attempt)
        raise RuntimeError("Failed to get response from OpenAI API after 3 attempts.")
