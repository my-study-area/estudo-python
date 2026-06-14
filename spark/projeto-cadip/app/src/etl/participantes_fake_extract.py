from pathlib import Path
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

from src.domain.participantes import Participantes
from src.extract import IExtract


class ParticipantesFakeExtract(IExtract[Participantes]):
    def __init__(self, glue_context: GlueContext, anomesdia: str) -> None:
        self.__anomesdia: str = anomesdia
        self.spark: SparkSession = glue_context.spark_session

    def extract(self) -> Participantes:
        caminho_base = Path(__file__).parent.parent
        arquivo_json = str(caminho_base / "dados_participantes.json")
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        df = df.filter(col("anomesdia") == self.__anomesdia)
        return Participantes(df)
