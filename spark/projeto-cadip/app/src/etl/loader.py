from __future__ import annotations
import logging
from src.etl.template_registro1 import TemplateRegistro1

logger = logging.getLogger(__name__)


class Loader:
    def load(self, template: TemplateRegistro1) -> None:
        logger.info('loading ...')
