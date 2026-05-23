from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

class Participantes:
    def __init__(self, data_frame: DataFrame):
        self.__data_frame = data_frame

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("identificador_pessoa").cast("string").alias("id_pessoa"),
            col("tipo_participante").cast("integer").alias("tipo"),
            col("numero_contrato_servico").cast("string").alias("numero_contrato")
        )
