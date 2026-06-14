from typing import Optional
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

from src.domain.dados_cadastrais import DadosCadastrais
from src.extract import IExtract

class DadosCadastraisExtract(IExtract[DadosCadastrais]):
    __DATABASE_NAME = "db_custodia"
    __TABLE_NAME = "tb_dados_cadastrais"

    def __init__(self, glue_context: GlueContext, setores_empresas_publicas_customizado: Optional[str]) -> None:
        self.__glue_context: GlueContext = glue_context
        self.__setores_empresas_publicas_customizado: Optional[str] = setores_empresas_publicas_customizado

    def extract(self) -> DadosCadastrais:
        dynamic_frame: DynamicFrame = self.__glue_context.create_dynamic_frame.from_catalog(
            database=self.__class__.__DATABASE_NAME, table_name=self.__class__.__TABLE_NAME)
        data_frame = dynamic_frame.toDF()
        return DadosCadastrais(data_frame, self.__setores_empresas_publicas_customizado)
