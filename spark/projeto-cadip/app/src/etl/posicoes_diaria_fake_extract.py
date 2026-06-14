from pathlib import Path
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from src.domain.posicoes_diaria import PosicoesDiaria
from src.extract import IExtract

class PosicoesDiariaFakeExtract(IExtract[PosicoesDiaria]):
    def __init__(self, glue_context: GlueContext, anomesdia: str) -> None:
        self.__anomesdia: str = anomesdia
        self.spark_session: SparkSession = glue_context.spark_session

    def extract(self) -> PosicoesDiaria:
        caminho_base = Path(__file__).parent.parent
        arquivo_json = str(caminho_base / "dados_posicoes_diaria.json")
        df = (
            self.spark_session.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return PosicoesDiaria(df)
