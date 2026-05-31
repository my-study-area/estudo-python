from pyspark.sql import SparkSession

from src.domain.contratos import Contratos
from src.extract import IExtract


class ContratosFakeExtract(IExtract[Contratos]):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name: str = database_name
        self.table_name: str = table_name


    def extract(self) -> Contratos:
        arquivo_json = "app/src/dados_contratos.json"
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return Contratos(df)
