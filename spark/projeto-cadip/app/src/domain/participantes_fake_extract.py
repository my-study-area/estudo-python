from pyspark.sql import SparkSession

from src.domain.participantes import Participantes
from src.extract import IExtract


class ParticipantesFakeExtract(IExtract[Participantes]):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file-participantes")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name: str = database_name
        self.table_name: str = table_name


    def extract(self) -> Participantes:
        arquivo_json = "app/src/dados_participantes.json"
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        df.printSchema()
        df.show()
        return Participantes(df)
