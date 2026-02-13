import os
from openai import OpenAI
from .base import LLMAdapter

class GrokAdapter(LLMAdapter):

    def __init__(self):
        api_key = os.getenv("LLM_API_KEY")
        if not api_key:
            raise RuntimeError("LLM_API_KEY not set")

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )

    def chat(self, prompt: str) -> dict:
        response = self.client.chat.completions.create(
            model="grok-4-0709",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "metadata": {
                "usage": getattr(response, "usage", None)
            }
        }
