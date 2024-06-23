from abc import ABC, abstractmethod


class BaseTTS(ABC):
    @abstractmethod
    def process_prompt(self, prompt): ...
