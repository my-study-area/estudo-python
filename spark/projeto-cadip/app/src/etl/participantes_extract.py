from awsglue.context import GlueContext

from src.domain.participantes import Participantes
from src.extract import IExtract


class ParticipantesExtract(IExtract[Participantes]):
    def __init__(self, glue_context: GlueContext, database_name: str, table_name: str) -> None:
        self.glue_context: GlueContext = glue_context
        self.database_name: str = database_name
        self.table_name: str = table_name


    def extract(self) -> Participantes:
        raise Exception('Metodo nao implementado!')
