from __future__ import annotations
import logging

from src.etl.transformer import Transformer
from src.etl.formatter_registro1 import FormatterRegistro1
from src.etl.loader import Loader
from src.etl.template_registro1 import TemplateRegistro1
from src.service.business_exception import BusinessException

logger = logging.getLogger(__name__)


class Executor:
    def __init__(self, transformer: Transformer, formatter: FormatterRegistro1, loader: Loader) -> None:
        self.__transformer = transformer
        self.__formatter = formatter
        self.__loader = loader

    def run(self) -> None:
        try:
            dados_cadip = self.__transformer.transform()
            template = self.__formatter.format(dados_cadip)
            self.__loader.load(template)
            logger.info('Processamento realizado com sucesso.')
        except BusinessException as ex:
            logger.info('Processamento finalizado. Motivo: %s', ex)
        except Exception:
            logger.exception('Erro ao realizar processamento')
            raise
