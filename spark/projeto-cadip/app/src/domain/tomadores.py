from __future__ import annotations
from pyspark.sql import DataFrame


class Tomadores:
    def __init__(self, data_frame: DataFrame) -> None:
        self.__data_frame = data_frame

    def to_df(self) -> DataFrame:
        return self.__data_frame

    def is_empty(self) -> bool:
        return len(self.__data_frame.take(1)) == 0
