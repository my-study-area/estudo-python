from awsglue.context import GlueContext
from src.domain.posicoes_diaria import PosicoesDiaria
from src.extract import IExtract

class PosicoesDiariaExtract(IExtract[PosicoesDiaria]):
    def __init__(self, glue_context: GlueContext, database_name: str, table_name: str) -> None:
        self.glue_context = glue_context
        self.database_name = database_name
        self.table_name = table_name

    def extract(self) -> PosicoesDiaria:
        dynamic_frame = self.glue_context.create_dynamic_frame.from_catalog(
            database=self.database_name, table_name=self.table_name
        )
        return PosicoesDiaria(dynamic_frame.toDF())
