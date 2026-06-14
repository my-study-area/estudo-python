from __future__ import annotations
from pyspark.sql import DataFrame
from pyspark.sql.functions import col

from src.domain.contratos import Contratos
from src.domain.dados_cadip import DadosCadip
from src.domain.dados_cadastrais import DadosCadastrais
from src.domain.identificacao_pessoas import IdentificacaoPessoas
from src.domain.participantes import Participantes
from src.domain.posicoes_diaria import PosicoesDiaria
from src.domain.ipocs import Ipocs
from src.etl.extract_builder import ExtractBuilder
from src.service.business_exception import BusinessException


class Transformer:
    def __init__(self, builder: ExtractBuilder) -> None:
        self.__builder = builder
        self.__data_frame: DataFrame | None = None

    def transform(self) -> DadosCadip:
        contratos: Contratos = self.__builder.build_extract_contrato().extract()
        if contratos.is_empty():
            raise BusinessException("Não existem contratos para realizar o processamento")

        participantes: Participantes = self.__builder.build_extract_participantes().extract()
        if participantes.is_empty():
            raise BusinessException("Não existem participantes para realizar o processamento")

        identificao_pessoas: IdentificacaoPessoas = self.__builder.build_extract_identificao_pessoas().extract()
        if identificao_pessoas.is_empty():
            raise BusinessException("Não existem identificacao_pessoas para realizar o processamento")

        dados_cadastrais: DadosCadastrais = self.__builder.build_extract_dados_cadastrais().extract()
        if dados_cadastrais.is_empty():
            raise BusinessException("Não existem dados_cadastrais para realizar o processamento")

        contratos_filtrados = contratos.filter_by_entes_publicos(
            participantes, identificao_pessoas, dados_cadastrais
        )
        if contratos_filtrados.is_empty():
            raise BusinessException("Não existem contratos de entes públicos")

        posicoes_diaria: PosicoesDiaria = self.__builder.build_extract_posicoes_diarias().extract()
        ipocs: Ipocs = self.__builder.build_extract_ipocs().extract()
        tomadores = dados_cadastrais.get_tomadores(participantes, identificao_pessoas)
        garantidores = dados_cadastrais.get_garantidores(participantes, identificao_pessoas)

        df_contratos = contratos_filtrados.to_df()
        df_posicoes_diaria = posicoes_diaria.to_df()
        df_tomadores = tomadores.to_df()
        df_garantidores = garantidores.to_df()
        df_ipocs = ipocs.to_df()

        self.__data_frame = (
            df_contratos.alias("contratos")
            .join(df_posicoes_diaria.alias("posicoes"), col("posicoes.numero_contrato") == col("contratos.numero_contrato"), "left")
            .join(df_tomadores.alias("tomadores"), col("tomadores.numero_contrato") == col("contratos.numero_contrato"), "left")
            .join(df_garantidores.alias("garantidores"), col("garantidores.numero_contrato") == col("contratos.numero_contrato"), "left")
            .join(df_ipocs.alias("ipocs"), col("ipocs.numero_contrato") == col("contratos.numero_contrato"), "left")
            .select("contratos.*")
        )

        return DadosCadip(self.__data_frame)
