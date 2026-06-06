from awsglue.context import GlueContext

from src.domain.identificacao_pessoas import IdentificacaoPessoas
from src.extract import IExtract


class IdentificacaoPessoasExtract(IExtract[IdentificacaoPessoas]):
    def __init__(self, glue_context: GlueContext, database_name: str, table_name: str) -> None:
        self.glue_context: GlueContext = glue_context
        self.database_name: str = database_name
        self.table_name: str = table_name


    def extract(self) -> IdentificacaoPessoas:
        raise Exception('Metodo nao implementado!')
