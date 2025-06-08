import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

# --- Configuração para LocalStack (IMPORTANTE!) ---
# Define o endpoint do S3 para apontar para o LocalStack
# Isso garante que o PySpark dentro do container se conecte ao S3 local.
# O IP pode variar dependendo de como seu Docker está configurado.
# Geralmente, 'host.docker.internal' ou o IP do seu host LocalStack.
# Se estiver executando no mesmo container, 'localhost' pode funcionar.
# Para LocalStack rodando no host e o container Glue rodando, 'host.docker.internal'
# é a maneira mais comum e robusta de se referir ao host do Docker.
s3_endpoint = "http://localstack:4566" # Ou 'http://localhost:4566' se o LocalStack estiver no mesmo container ou for acessível via localhost do container

# Inicializa o SparkContext e GlueContext
# Configura o endpoint do S3 para o SparkContext
sc = SparkContext.getOrCreate()
sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", s3_endpoint)
sc._jsc.hadoopConfiguration().set("fs.s3a.path.style.access", "true") # Necessário para alguns sistemas de armazenamento compatíveis com S3 como o LocalStack
sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
# Se estiver usando credenciais dummy para LocalStack (muito comum):
sc._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.AnonymousAWSCredentialsProvider")
# Ou se precisar de credenciais (ex: testando com credenciais reais que apontam para LocalStack)
# sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "test")
# sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "test")


glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Caminho para o nosso arquivo CSV no S3 do LocalStack
s3_path = "s3a://meu-bucket-dados-localstack/data/data.csv" # Use s3a:// para o Spark com S3


def print_line(message):
    print("=====================================================================================")
    print(message)
    print("=====================================================================================")
    print()


# Lê o arquivo CSV do S3
print_line(f"Lendo dados do S3 em: {s3_path}")

try:
    df = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(s3_path)

    # Mostra o schema e os dados lidos
    print_line("Schema do DataFrame:")
    df.printSchema()

    print_line("Dados lidos do S3:")
    df.show()

except Exception as e:
    print_line(f"Erro ao ler do S3: {e}")

# Para garantir que o Job finalize corretamente
# glueContext.stop() # Descomente se tiver problemas de encerramento em scripts mais complexos
