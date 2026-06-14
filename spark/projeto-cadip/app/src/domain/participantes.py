from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import col


class Participantes:
    __CODIGO_TIPO_PARTICIPANTE_TOMADOR = 2

    def __init__(self, data_frame: DataFrame) -> None:
        self.__data_frame = data_frame

    @property
    def codigo_tipo_participante_tomador(self) -> int:
        return self.__CODIGO_TIPO_PARTICIPANTE_TOMADOR

    def is_empty(self) -> bool:
        return len(self.__data_frame.take(1)) == 0

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("identificador_pessoa").cast("string").alias("id_pessoa"),
            col("tipo_participante").cast("integer").alias("tipo"),
            col("numero_contrato_servico").cast("string").alias("numero_contrato")
        )
