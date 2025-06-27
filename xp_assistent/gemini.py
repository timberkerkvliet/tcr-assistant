import google.generativeai as genai
import os

from xp_assistent.llm_client import LLMClient
from xp_assistent.llm_conversation import LLMConversation


class GeminiConversation(LLMConversation):
    def __init__(self, model):
        self.model = model
        self.chat_session = model.start_chat(history=[])

    def chat(self, message: str) -> str:
        """Send a new message to the Gemini model and return the response."""
        response = self.chat_session.send_message(message)
        return response.text


class GeminiClient(LLMClient):
    def __init__(self, api_key: str = None, model_name: str = 'gemini-2.5-flash'):
        if api_key:
            genai.configure(api_key=api_key)
        else:
            # Try to get API key from environment variable
            api_key_from_env = os.getenv("GEMINI_API_KEY")
            if api_key_from_env:
                genai.configure(api_key=api_key_from_env)
            else:
                raise ValueError(
                    "Google Gemini API key not provided. "
                    "Please pass it to the constructor or set the GEMINI_API_KEY environment variable."
                )
        self.model = genai.GenerativeModel(model_name)

    def new_conversation(self) -> GeminiConversation:
        """Create and return a new GeminiConversation instance."""
        return GeminiConversation(self.model)
