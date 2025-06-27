import os

from xp_assistent.openai_client import OpenAIClient

client = OpenAIClient(os.getenv("OPENAI_SECRET"), model='gpt-4o-mini')

conversation = client.new_conversation()

print(conversation.chat("Hallo, hoe kan je me helpen?"))
