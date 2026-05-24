from pyspark.sql import SparkSession, DataFrame

from src.domain.IExtract import IExtract
from src.domain.contratos import Contratos


class ExtractContratosFake(IExtract[Contratos]):
    def __init__(self, database_name: str, table_name: str):
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name = database_name
        self.table_name = table_name


    def extract(self) -> Contratos:
        arquivo_json = "app/src/dados_contratos.json"
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return Contratos(df)
