from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class IExtract(ABC, Generic[T]):
    @abstractmethod
    def extract(self) -> T:
        pass