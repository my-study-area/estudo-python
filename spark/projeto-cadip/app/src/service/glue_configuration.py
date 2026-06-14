import logging
from typing import Dict, Any, Optional
from awsglue.context import GlueContext

logger = logging.getLogger(__name__)


class GlueConfiguration:
    """
    Classe responsável por expor as configurações e contexto do AWS Glue resolvidos.
    Atua como um container de configuração limpo e desacoplado de infraestrutura.
    """
    def __init__(self, args: Dict[str, Any], glue_context: GlueContext) -> None:
        self._database_name: str = args.get('DATABASE_NAME', 'db_custodia')
        logger.info("DATABASE_NAME: %s", self._database_name)
        self._table_name: str = args.get('TABLE_NAME', '')
        logger.info("TABLE_NAME: %s", self._table_name)
        self._environment: str = args.get('ENVIRONMENT', 'PROD').upper()
        logger.info("ENVIRONMENT: %s", self._environment)
        self._anomesdia: str = args.get('ANOMESDIA', '')
        logger.info("ANOMESDIA: %s", self._anomesdia)
        self._setores_empresas_publicas_customizado: Optional[str] = args.get('SETORES_EMPRESAS_PUBLICAS_CUSTOMIZADO', None)
        logger.info("SETORES_EMPRESAS_PUBLICAS_CUSTOMIZADO: %s", self._setores_empresas_publicas_customizado)
        self._glue_context: GlueContext = glue_context

    @property
    def database_name(self) -> str:
        return self._database_name

    @property
    def table_name(self) -> str:
        return self._table_name

    @property
    def environment(self) -> str:
        return self._environment

    @property
    def anomesdia(self) -> str:
        return self._anomesdia

    @property
    def setores_empresas_publicas_customizado(self) -> Optional[str]:
        return self._setores_empresas_publicas_customizado

    @property
    def glue_context(self) -> GlueContext:
        return self._glue_context
