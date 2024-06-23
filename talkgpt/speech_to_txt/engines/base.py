from abc import ABC, abstractmethod


class BaseSTT(ABC):
    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...
