import sys
import logging
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark import SparkContext

from src.service.glue_configuration import GlueConfiguration
from src.etl.extract_builder import ExtractBuilderFactory
from src.etl.transformer import Transformer
from src.etl.formatter_registro1 import FormatterRegistro1
from src.etl.loader import Loader
from src.service.executor import Executor

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(message)s',
)
logger = logging.getLogger(__name__)


def run_pipeline(glue_config: GlueConfiguration) -> None:
    logger.info("Executando no ambiente: %s", glue_config.environment)

    builder = ExtractBuilderFactory.create(glue_config)
    transformer = Transformer(builder)
    formatter = FormatterRegistro1()
    loader = Loader()
    executor = Executor(transformer, formatter, loader)
    executor.run()


def run_job() -> None:
    args_list = ['JOB_NAME', 'DATABASE_NAME', 'TABLE_NAME']
    args = getResolvedOptions(sys.argv, args_list)

    database_name = args.get('DATABASE_NAME')
    table_name = args.get('TABLE_NAME')

    logger.info("Iniciando a execução do Job: %s", args.get('JOB_NAME'))
    logger.info("Iniciando leitura da tabela catalogada: %s.%s", database_name, table_name)

    sc = SparkContext.getOrCreate()
    glue_context = GlueContext(sc)

    dynamic_frame = glue_context.create_dynamic_frame.from_catalog(
        database=database_name,
        table_name=table_name
    )

    logger.info("Total de registros lidos: %s", dynamic_frame.count())
    dynamic_frame.printSchema()


if __name__ == '__main__':
    args_list = ['JOB_NAME', 'DATABASE_NAME', 'TABLE_NAME', 'ENVIRONMENT',
                 'ANOMESDIA', 'SETORES_EMPRESAS_PUBLICAS_CUSTOMIZADO']
    args = getResolvedOptions(sys.argv, args_list)

    sc = SparkContext.getOrCreate()
    sc.setLogLevel("WARN")
    glue_context = GlueContext(sc)

    glue_config = GlueConfiguration(args, glue_context)
    run_pipeline(glue_config)
