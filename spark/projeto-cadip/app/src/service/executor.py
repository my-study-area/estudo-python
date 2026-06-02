from awsglue.context import GlueContext


class Executor:
    def __init__(self, glue_context: GlueContext) -> None:
        self.__context: GlueContext = glue_context

    def run(self) -> None:
        self.__context.create_dynamic_frame.from_catalog(database="your_database", table_name="your_table")
        print('run')