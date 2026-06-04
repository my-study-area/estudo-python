from pyspark.sql import SparkSession
from unittest.mock import MagicMock

from src.service import executor
from src.service.executor import Executor
from src.service.glue_configuration import GlueConfiguration
from src.service.extract_builder import ExtractBuilderFactory, ExtractBuilder


def run() -> None:
    print("Executando em ambiente LOCAL com Spark Session simulada...")
    
    # 1. Setup local mockado do Spark e Glue Context
    spark = SparkSession.builder.master("local[*]").appName("LOCAL_TEST").getOrCreate()
    mock_glue_context = MagicMock()
    mock_glue_context.spark_session = spark

    # 2. Criação do dicionário de args mockados
    local_args = {
        "JOB_NAME": "local_job",
        "DATABASE_NAME": "db_custodia",
        "TABLE_NAME": "tb_contratos",
        "ENVIRONMENT": "LOCAL"  # Força o Builder a resolver como FakeExtractBuilder
    }

    # 3. Instancia a configuração e executa
    glue_config: GlueConfiguration = GlueConfiguration(local_args, mock_glue_context)
    builder: ExtractBuilder = ExtractBuilderFactory.create(glue_config)
    executor: Executor = Executor(glue_config, builder)
    executor.run()



if __name__ == '__main__':
    run()
