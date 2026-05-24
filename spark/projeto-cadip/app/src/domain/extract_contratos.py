from src.domain.IExtract import IExtract
from pyspark.sql import DataFrame
from awsglue.context import GlueContext

from src.domain.contratos import Contratos


class ExtractContratos(IExtract[Contratos]):
    def __init__(self, glue_context: GlueContext, database_name: str, table_name: str):
        self.glue_context = glue_context
        self.database_name = database_name
        self.table_name = table_name


    def extract(self) -> Contratos:
        raise Exception('Metodo nao implementado!')
