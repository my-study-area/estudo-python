from pathlib import Path

from awsglue.context import GlueContext
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import date_sub, current_date, col

from src.domain.contratos import Contratos
from src.extract import IExtract


class ContratosFakeExtract(IExtract[Contratos]):
    def __init__(self, glue_context: GlueContext, anomesdia: str) -> None:
        self.__glue_context: GlueContext = glue_context
        self.__anomesdia: str = anomesdia
        self.spark_session: SparkSession = self.__glue_context.spark_session

    def extract(self) -> Contratos:
        caminho_base = Path(__file__).parent.parent
        arquivo_json = str(caminho_base / "dados_contratos.json")
        df = (
            self.spark_session.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        df = df.filter(col("anomesdia") == self.__anomesdia)
        df = df.withColumn("data_contratacao", date_sub(current_date(), 1))
        return Contratos(df)
