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
    """
    Interface/Classe abstrata base para construção de extratores de dados.
    """
    def __init__(self, glue_context: GlueContext) -> None:
        self._glue_context = glue_context

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
    """
    Implementação concreta do builder que instancia extratores reais
    conectados ao catálogo de dados do AWS Glue.
    """
    def build_extract_contrato(self) -> IExtract[Contratos]:
        # ContratosExtract no momento recebe apenas glue_context e possui banco/tabela fixos internamente
        return ContratosExtract(self._glue_context)

    def build_extract_posicoes_diarias(self) -> IExtract[PosicoesDiaria]:
        return PosicoesDiariaExtract(self._glue_context, "db_custodia", "tb_posicoes_diaria")

    def build_extract_dados_cadastrais(self) -> IExtract[DadosCadastrais]:
        return DadosCadastraisExtract(self._glue_context, "db_custodia", "tb_dados_cadastrais")

    def build_extract_identificao_pessoas(self) -> IExtract[IdentificacaoPessoas]:
        return IdentificacaoPessoasExtract(self._glue_context, "db_custodia", "tb_identificacao_pessoas")

    def build_extract_participantes(self) -> IExtract[Participantes]:
        return ParticipantesExtract(self._glue_context, "db_custodia", "tb_participantes")

    def build_extract_ipocs(self) -> IExtract[Ipocs]:
        return IpocsExtract(self._glue_context, "db_custodia", "tb_ipocs")


class FakeExtractBuilder(ExtractBuilder):
    """
    Implementação concreta do builder que instancia extratores mockados (fakes)
    para desenvolvimento e validação em ambiente local.
    """
    def build_extract_contrato(self) -> IExtract[Contratos]:
        return ContratosFakeExtract(self._glue_context)

    def build_extract_posicoes_diarias(self) -> IExtract[PosicoesDiaria]:
        return PosicoesDiariaFakeExtract(self._glue_context)

    def build_extract_dados_cadastrais(self) -> IExtract[DadosCadastrais]:
        return DadosCadastraisFakeExtract(self._glue_context)

    def build_extract_identificao_pessoas(self) -> IExtract[IdentificacaoPessoas]:
        return IdentificacaoPessoasFakeExtract(self._glue_context)

    def build_extract_participantes(self) -> IExtract[Participantes]:
        return ParticipantesFakeExtract(self._glue_context)

    def build_extract_ipocs(self) -> IExtract[Ipocs]:
        return IpocsFakeExtract(self._glue_context)


class ExtractBuilderFactory:
    """
    Factory responsável por criar a instância correta de ExtractBuilder
    com base no ambiente resolvido por GlueConfiguration. Ex:
    Cria um FakeExtractBuilder para um ambiente LOCAL e um RealExtractBuilder
    para ambientes DEV, HOM ou PROD.
    """

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

        return extract_builder(glue_config.glue_context)


