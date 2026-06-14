from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import col


class Ipocs:
    def __init__(self, data_frame: DataFrame) -> None:
        self.__data_frame = data_frame

    def is_empty(self) -> bool:
        return len(self.__data_frame.take(1)) == 0

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("numero_contrato_servico").cast("string").alias("numero_contrato"),
            col("codigo_ipoc").cast("string").alias("codigo_ipoc")
        )
