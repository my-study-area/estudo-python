from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

from src.domain.participantes import Participantes
from src.extract import IExtract

class ParticipantesExtract(IExtract[Participantes]):
    __DATABASE_NAME = "db_custodia"
    __TABLE_NAME = "tb_participantes"

    def __init__(self, glue_context: GlueContext) -> None:
        self.__glue_context: GlueContext = glue_context

    def extract(self) -> Participantes:
        dynamic_frame: DynamicFrame = self.__glue_context.create_dynamic_frame.from_catalog(
            database=self.__class__.__DATABASE_NAME, table_name=self.__class__.__TABLE_NAME)
        data_frame = dynamic_frame.toDF()
        return Participantes(data_frame)
