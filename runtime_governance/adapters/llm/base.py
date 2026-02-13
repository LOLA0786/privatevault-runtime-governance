from abc import ABC, abstractmethod

class LLMAdapter(ABC):

    @abstractmethod
    def chat(self, prompt: str) -> dict:
        """
        Returns:
        {
            "content": str,
            "model": str,
            "metadata": dict
        }
        """
        pass
