from abc import ABC, abstractmethod
from pyspark.sql import DataFrame

class IExtract(ABC):
    @abstractmethod
    def extract(self) -> DataFrame:
        pass