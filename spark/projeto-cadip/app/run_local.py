import logging
from pyspark.sql import SparkSession
from unittest.mock import MagicMock

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


def run() -> None:
    logger.info("Executando em ambiente LOCAL com Spark Session simulada...")

    spark = SparkSession.builder.master("local[*]").appName("LOCAL_TEST").getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    mock_glue_context = MagicMock()
    mock_glue_context.spark_session = spark

    local_args = {
        "JOB_NAME": "local_job",
        "DATABASE_NAME": "db_custodia",
        "TABLE_NAME": "tb_contratos",
        "ENVIRONMENT": "LOCAL",
        "ANOMESDIA": "20260101",
        # "SETORES_EMPRESAS_PUBLICAS_CUSTOMIZADO": "1000,2000",
        "SETORES_EMPRESAS_PUBLICAS_CUSTOMIZADO": "2001",
    }

    glue_config = GlueConfiguration(local_args, mock_glue_context)
    builder = ExtractBuilderFactory.create(glue_config)
    transformer = Transformer(builder)
    formatter = FormatterRegistro1()
    loader = Loader()
    executor = Executor(transformer, formatter, loader)
    executor.run()


if __name__ == '__main__':
    run()
