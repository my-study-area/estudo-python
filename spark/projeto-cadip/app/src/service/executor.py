from src.etl.extract_builder import ExtractBuilder
from src.service.glue_configuration import GlueConfiguration


class Executor:
    def __init__(self, glue_configuration: GlueConfiguration, builder: ExtractBuilder) -> None:
        self.__builder = builder
        self.__context: GlueConfiguration = glue_configuration

    def run(self) -> None:
        print('running executor ...')
        self.__show_all_data_frames()

    def __show_all_data_frames(self):
        extract_contrato = self.__builder.build_extract_contrato()
        extract_contrato.extract().to_df().show()

        extract_posicoes_diarias = self.__builder.build_extract_posicoes_diarias()
        extract_posicoes_diarias.extract().to_df().show()

        extract_participantes = self.__builder.build_extract_participantes()
        extract_participantes.extract().to_df().show()

        extract_ipocs = self.__builder.build_extract_ipocs()
        extract_ipocs.extract().to_df().show()

        extract_identificacao_pessoas = self.__builder.build_extract_identificao_pessoas()
        extract_identificacao_pessoas.extract().to_df().show()

        extract_dados_cadastrais = self.__builder.build_extract_dados_cadastrais()
        extract_dados_cadastrais.extract().to_df().show()

