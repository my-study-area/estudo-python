from pyspark.sql import SparkSession

from src.domain.IExtract import IExtract
from src.domain.participantes import Participantes


class ExtractParticipantesFake(IExtract[Participantes]):
    def __init__(self, database_name: str, table_name: str):
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file-participantes")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name = database_name
        self.table_name = table_name


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
