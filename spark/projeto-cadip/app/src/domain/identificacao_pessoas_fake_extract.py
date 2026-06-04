from pathlib import Path
from awsglue.context import GlueContext
from pyspark.sql import SparkSession

from src.domain.identificacao_pessoas import IdentificacaoPessoas
from src.extract import IExtract


class IdentificacaoPessoasFakeExtract(IExtract[IdentificacaoPessoas]):
    def __init__(self, glue_context: GlueContext) -> None:
        self.spark: SparkSession = glue_context.spark_session

    def extract(self) -> IdentificacaoPessoas:
        caminho_base = Path(__file__).parent.parent
        arquivo_json = str(caminho_base / "indentificacao_pessoas.json")
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return IdentificacaoPessoas(df)

