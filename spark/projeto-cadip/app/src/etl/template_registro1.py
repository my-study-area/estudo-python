from __future__ import annotations
from pyspark.sql import DataFrame


class TemplateRegistro1:
    def __init__(self, data_frame: DataFrame) -> None:
        self.__data_frame = data_frame

    def to_df(self) -> DataFrame:
        return self.__data_frame
