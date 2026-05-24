from pyspark.sql import SparkSession

from src.domain.IExtract import IExtract
from src.domain.identificacao_pessoas import IdentificacaoPessoas


class ExtractIdentificacaoPessoasFake(IExtract[IdentificacaoPessoas]):
    def __init__(self, database_name: str, table_name: str):
        self.spark: SparkSession = (
            SparkSession.builder
            .appName("read-json-file-identificacao-pessoas")
            .master("local[*]")
            .getOrCreate()
        )
        self.database_name = database_name
        self.table_name = table_name


    def extract(self) -> IdentificacaoPessoas:
        arquivo_json = "app/src/indentificacao_pessoas.json"
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return IdentificacaoPessoas(df)
