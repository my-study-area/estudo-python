from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

class Contratos:
    def __init__(self, data_frame: DataFrame):
        self.__data_frame = data_frame

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("numero_contrato_servico").cast("string").alias("numero_contrato"),
            col("valor_contratacao").cast("string").alias("valor"),
            col("data_contratacao").alias("data"),
        )