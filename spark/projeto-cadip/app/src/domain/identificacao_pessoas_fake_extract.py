from pyspark.sql import SparkSession

from src.domain.identificacao_pessoas import IdentificacaoPessoas
from src.extract import IExtract


class IdentificacaoPessoasFakeExtract(IExtract[IdentificacaoPessoas]):
    def __init__(self, database_name: str, table_name: str) -> None:
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file-identificacao-pessoas")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name: str = database_name
        self.table_name: str = table_name


    def extract(self) -> IdentificacaoPessoas:
        arquivo_json = "app/src/indentificacao_pessoas.json"
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return IdentificacaoPessoas(df)
