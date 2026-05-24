from pyspark.sql import SparkSession

from src.domain.IExtract import IExtract
from src.domain.dados_cadastrais import DadosCadastrais


class ExtractDadosCadastraisFake(IExtract[DadosCadastrais]):
    def __init__(self, database_name: str, table_name: str):
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file-dados-cadastrais")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name = database_name
        self.table_name = table_name


    def extract(self) -> DadosCadastrais:
        arquivo_json = "app/src/dados_cadastrais.json"
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return DadosCadastrais(df)
