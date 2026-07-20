


from abc import ABC, abstractmethod


class DarijaCallable(ABC):
    
    @abstractmethod
    def arity(self) -> int:
        pass

    @abstractmethod
    def call(self, interpreter, arguments):
        pass

    
    