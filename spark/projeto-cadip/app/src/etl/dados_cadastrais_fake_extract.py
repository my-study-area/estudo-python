from pathlib import Path
from typing import Optional
from awsglue.context import GlueContext
from pyspark.sql import SparkSession

from src.domain.dados_cadastrais import DadosCadastrais
from src.extract import IExtract


class DadosCadastraisFakeExtract(IExtract[DadosCadastrais]):
    def __init__(self, glue_context: GlueContext, setores_empresas_publicas_customizado: Optional[str]) -> None:
        self.__setores_empresas_publicas_customizado: Optional[str] = setores_empresas_publicas_customizado
        self.spark: SparkSession = glue_context.spark_session

    def extract(self) -> DadosCadastrais:
        caminho_base = Path(__file__).parent.parent
        arquivo_json = str(caminho_base / "dados_cadastrais.json")
        df = (
            self.spark.read
            .option("multiline", "true")
            .json(arquivo_json)
        )
        return DadosCadastrais(df, self.__setores_empresas_publicas_customizado)
