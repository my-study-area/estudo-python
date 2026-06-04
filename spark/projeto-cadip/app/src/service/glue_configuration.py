from typing import Dict, Any
from awsglue.context import GlueContext


class GlueConfiguration:
    """
    Classe responsável por expor as configurações e contexto do AWS Glue resolvidos.
    Atua como um container de configuração limpo e desacoplado de infraestrutura.
    """
    def __init__(self, args: Dict[str, Any], glue_context: GlueContext) -> None:
        # Resolve as propriedades a partir do dicionário de argumentos fornecido
        self._database_name: str = args.get('DATABASE_NAME', 'db_custodia')
        self._table_name: str = args.get('TABLE_NAME', '')
        # A chave de ambiente é 'ENVIRONMENT'
        self._environment: str = args.get('ENVIRONMENT', 'PROD').upper()
        self._glue_context: GlueContext = glue_context

    @property
    def database_name(self) -> str:
        """Retorna o nome do banco de dados configurado no Glue Data Catalog."""
        return self._database_name

    @property
    def table_name(self) -> str:
        """Retorna o nome da tabela no Glue Data Catalog."""
        return self._table_name

    @property
    def environment(self) -> str:
        """Retorna o ambiente de execução resolvido (LOCAL, DEV, HOM, PROD).
           Caso o valor não seja um valor válido, define como padrão o valor 'PROD'
        """
        return self._environment

    @property
    def glue_context(self) -> GlueContext:
        """Retorna o objeto GlueContext ativo."""
        return self._glue_context
