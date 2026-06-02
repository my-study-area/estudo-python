from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame

from src.domain.contratos import Contratos
from src.extract import IExtract

DATABASE_NAME = "your_database"
TABLE_NAME = "your_table"


class ContratosExtract(IExtract[Contratos]):
    def __init__(self, glue_context: GlueContext) -> None:
        self.__glue_context: GlueContext = glue_context
        self.__database_name: str = DATABASE_NAME
        self.__table_name: str = TABLE_NAME

    def extract(self) -> Contratos:
        dynamic_frame: DynamicFrame = self.__glue_context.create_dynamic_frame.from_catalog(
            database=self.__database_name, table_name=self.__table_name)
        data_frame = dynamic_frame.toDF()
        return Contratos(data_frame)
