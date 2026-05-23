from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

class IdentificacaoPessoas:
    def __init__(self, data_frame: DataFrame):
        self.__data_frame = data_frame

    def to_df(self) -> DataFrame:
        return self.__data_frame.select(
            col("cod_ident_pess").cast("string").alias("id_pessoa"),
            col("num_doc").cast("string").alias("cnpj")
        )
