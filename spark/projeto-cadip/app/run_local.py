from unittest.mock import MagicMock

from awsglue.context import GlueContext
from pyspark.sql import SparkSession

from src.domain.contratos_fake_extract import ContratosFakeExtract


def get_local_spark():
    return SparkSession.builder \
        .master("local[*]") \
        .appName("LOCAL") \
        .getOrCreate()


def mock_glue_session(func):
    """
    Decorator que substitui a spark_session do GlueContext
    por uma sessão Spark local.
    """

    def wrapper(*args, **kwargs):
        # Cria o mock do GlueContext
        mock_glue_context = MagicMock(spec=GlueContext)

        # Cria a sessão Spark local e atribui ao mock
        local_spark = get_local_spark()
        mock_glue_context.spark_session = local_spark

        # Passa o contexto mockado para a função
        return func(mock_glue_context, *args, **kwargs)

    return wrapper

@mock_glue_session
def run(glue_context):
    print("Executando em ambiente local com Spark Session mockada...")
    ContratosFakeExtract(glue_context).extract().to_df().show()

    return None

if __name__ == '__main__':
    run()
