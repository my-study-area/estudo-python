from __future__ import annotations
import logging
from pyspark.sql import DataFrame

from src.domain.dados_cadip import DadosCadip
from src.etl.template_registro1 import TemplateRegistro1

logger = logging.getLogger(__name__)


class FormatterRegistro1:
    def format(self, dados_cadip: DadosCadip) -> TemplateRegistro1:
        logger.info('formating ...')
        df = dados_cadip.to_df()
        df.printSchema()
        df.show(truncate=False)
        logger.info('Total de registros: %s', df.count())
        return TemplateRegistro1(df)
