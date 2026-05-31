from pyspark.sql import SparkSession

from src.domain.dados_cadastrais import DadosCadastrais
from src.extract import IExtract


class DadosCadastraisFakeExtract(IExtract[DadosCadastrais]):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file-dados-cadastrais")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name: str = database_name
        self.table_name: str = table_name


    def extract(self) -> DadosCadastrais:
        arquivo_json = "app/src/dados_cadastrais.json"
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return DadosCadastrais(df)
