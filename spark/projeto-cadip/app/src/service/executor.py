from src.service.extract_builder import ExtractBuilder
from src.service.glue_configuration import GlueConfiguration


class Executor:
    def __init__(self, glue_configuration: GlueConfiguration, builder: ExtractBuilder) -> None:
        self.__builder = builder
        self.__context: GlueConfiguration = glue_configuration

    def run(self) -> None:
        print('running executor ...')
        extract_contrato = self.__builder.build_extract_contrato()
        extract_contrato.extract().to_df().show()

        extract_posicoes_diarias = self.__builder.build_extract_posicoes_diarias()
        extract_posicoes_diarias.extract().to_df().show()

