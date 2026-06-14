from __future__ import annotations
import logging
from pyspark.sql import DataFrame

from src.domain.dados_cadip import DadosCadip

logger = logging.getLogger(__name__)


class FormatterRegistro1:
    def format(self, dados_cadip: DadosCadip) -> DataFrame:
        logger.info('formating ...')
        return dados_cadip.to_df()
