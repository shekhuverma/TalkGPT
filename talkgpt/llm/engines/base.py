from abc import abstractmethod


class BaseLLM:
    @abstractmethod
    async def process_prompt(self, prompt: str):
        pass
