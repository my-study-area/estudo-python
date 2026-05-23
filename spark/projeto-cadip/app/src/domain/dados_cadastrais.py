from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

class DadosCadastrais:
    def __init__(self, data_frame: DataFrame):
        self.__data_frame = data_frame

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("identificacao_pessoa").cast("string").alias("id_pessoa"),
            col("setor_empresa").cast("string"),
            col("enderecos").alias("enderecos")
        )
