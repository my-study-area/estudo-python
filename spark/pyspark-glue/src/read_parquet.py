import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions


def print_line(message):
    print("=====================================================================================")
    print(message)
    print("=====================================================================================")
    print()


# --- Configuração para LocalStack (IMPORTANTE!) ---
# Define o endpoint do S3 para apontar para o LocalStack.
# Ajuste conforme seu ambiente Docker.
s3_endpoint = "http://localstack:4566"

# Inicializa o SparkContext e GlueContext
sc = SparkContext.getOrCreate()
# Configurações do Hadoop para o S3a para garantir conexão com LocalStack
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", s3_endpoint)
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true")
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
sc._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider")

glueContext = GlueContext(sc)
spark = glueContext.spark_session

# --- Caminho S3 do Arquivo Parquet ---
# Este é o mesmo caminho de saída que você usou no script anterior.
parquet_filtered_s3_path = "s3a://meu-bucket-dados-localstack/output/filtered_data/"

# Altere no read_parquet.py:
parquet_dynamic_frame_s3_path = "s3a://meu-bucket-dados-localstack/output/dynamicframe_filtered_data/"

def read_parquet(s3_path):
    """
    Função para ler um arquivo Parquet do S3 usando PySpark.
    """
    print_line(f"Lendo dados do arquivo Parquet em: {s3_path}")

    # --- Leitura do Parquet ---
    try:
        # Lendo o diretório Parquet (o Spark automaticamente encontra as partes)
        df_parquet = spark.read.parquet(s3_path)

        print_line("Schema do DataFrame lido do Parquet:")
        df_parquet.printSchema()

        print_line("Dados lidos do Parquet:")
        df_parquet.show()

    except Exception as e:
        print_line(f"Erro ao ler o arquivo Parquet: {e}")

    # O Glue SparkContext geralmente se encerra automaticamente,
    # então não precisamos chamar glueContext.stop() ou sc.stop() aqui.

if __name__ == "__main__":
    read_parquet(parquet_filtered_s3_path)
    read_parquet(parquet_dynamic_frame_s3_path)
