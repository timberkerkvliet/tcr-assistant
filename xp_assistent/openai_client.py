import time

import openai
from openai import OpenAIError

from xp_assistent.llm_conversation import LLMConversation


class OpenAIConversation(LLMConversation):
    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        temperature: float = 0.7,
        max_tokens: int = 1024
    ):
        openai.api_key = api_key
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
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=self.messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens
                )
                response_message = response.choices[0].message["content"]
                self.messages.append(response_message)
                return response_message
            except OpenAIError as e:
                print(f"OpenAI API error: {e}")
                time.sleep(2 ** attempt)
        raise RuntimeError("Failed to get response from OpenAI API after 3 attempts.")
