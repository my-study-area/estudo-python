from abc import ABC, abstractmethod
from typing import Type, Dict

from awsglue.context import GlueContext
from src.extract import IExtract
from src.service.glue_configuration import GlueConfiguration

# Importações de domínio
from src.domain.contratos import Contratos
from src.domain.posicoes_diaria import PosicoesDiaria
from src.domain.dados_cadastrais import DadosCadastrais
from src.domain.identificacao_pessoas import IdentificacaoPessoas
from src.domain.participantes import Participantes
from src.domain.ipocs import Ipocs

# Importações dos Extratores Reais
from src.etl.contratos_extract import ContratosExtract
from src.etl.posicoes_diaria_extract import PosicoesDiariaExtract
from src.etl.dados_cadastrais_extract import DadosCadastraisExtract
from src.etl.identificacao_pessoas_extract import IdentificacaoPessoasExtract
from src.etl.participantes_extract import ParticipantesExtract
from src.etl.ipocs_extract import IpocsExtract

# Importações dos Extratores Fakes
from src.etl.contratos_fake_extract import ContratosFakeExtract
from src.etl.posicoes_diaria_fake_extract import PosicoesDiariaFakeExtract
from src.etl.dados_cadastrais_fake_extract import DadosCadastraisFakeExtract
from src.etl.identificacao_pessoas_fake_extract import IdentificacaoPessoasFakeExtract
from src.etl.participantes_fake_extract import ParticipantesFakeExtract
from src.etl.ipocs_fake_extract import IpocsFakeExtract


class ExtractBuilder(ABC):
    def __init__(self, glue_config: GlueConfiguration) -> None:
        self._glue_config = glue_config
        self._glue_context: GlueContext = glue_config.glue_context

    @abstractmethod
    def build_extract_contrato(self) -> IExtract[Contratos]:
        pass

    @abstractmethod
    def build_extract_posicoes_diarias(self) -> IExtract[PosicoesDiaria]:
        pass

    @abstractmethod
    def build_extract_dados_cadastrais(self) -> IExtract[DadosCadastrais]:
        pass

    @abstractmethod
    def build_extract_identificao_pessoas(self) -> IExtract[IdentificacaoPessoas]:
        pass

    @abstractmethod
    def build_extract_participantes(self) -> IExtract[Participantes]:
        pass

    @abstractmethod
    def build_extract_ipocs(self) -> IExtract[Ipocs]:
        pass


class RealExtractBuilder(ExtractBuilder):
    def build_extract_contrato(self) -> IExtract[Contratos]:
        return ContratosExtract(self._glue_context, self._glue_config.anomesdia)

    def build_extract_posicoes_diarias(self) -> IExtract[PosicoesDiaria]:
        return PosicoesDiariaExtract(self._glue_context, self._glue_config.anomesdia)

    def build_extract_dados_cadastrais(self) -> IExtract[DadosCadastrais]:
        return DadosCadastraisExtract(self._glue_context, self._glue_config.setores_empresas_publicas_customizado)

    def build_extract_identificao_pessoas(self) -> IExtract[IdentificacaoPessoas]:
        return IdentificacaoPessoasExtract(self._glue_context)

    def build_extract_participantes(self) -> IExtract[Participantes]:
        return ParticipantesExtract(self._glue_context, self._glue_config.anomesdia)

    def build_extract_ipocs(self) -> IExtract[Ipocs]:
        return IpocsExtract(self._glue_context, self._glue_config.anomesdia)


class FakeExtractBuilder(ExtractBuilder):
    def build_extract_contrato(self) -> IExtract[Contratos]:
        return ContratosFakeExtract(self._glue_context, self._glue_config.anomesdia)

    def build_extract_posicoes_diarias(self) -> IExtract[PosicoesDiaria]:
        return PosicoesDiariaFakeExtract(self._glue_context, self._glue_config.anomesdia)

    def build_extract_dados_cadastrais(self) -> IExtract[DadosCadastrais]:
        return DadosCadastraisFakeExtract(self._glue_context, self._glue_config.setores_empresas_publicas_customizado)

    def build_extract_identificao_pessoas(self) -> IExtract[IdentificacaoPessoas]:
        return IdentificacaoPessoasFakeExtract(self._glue_context)

    def build_extract_participantes(self) -> IExtract[Participantes]:
        return ParticipantesFakeExtract(self._glue_context, self._glue_config.anomesdia)

    def build_extract_ipocs(self) -> IExtract[Ipocs]:
        return IpocsFakeExtract(self._glue_context, self._glue_config.anomesdia)


class ExtractBuilderFactory:
    @staticmethod
    def create(glue_config: GlueConfiguration) -> ExtractBuilder:
        builder_mapping: Dict[str, Type[ExtractBuilder]] = {
            'LOCAL': FakeExtractBuilder,
            'DEV': RealExtractBuilder,
            'HOM': RealExtractBuilder,
            'PROD': RealExtractBuilder
        }
        environment = glue_config.environment.upper()
        extract_builder = builder_mapping.get(environment, RealExtractBuilder)

        return extract_builder(glue_config)
