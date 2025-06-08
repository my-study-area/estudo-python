import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

def print_line(message):
    print("=====================================================================================")
    print(message)
    print("=====================================================================================")
    print()



# --- Configuração para LocalStack (Revisão Importante!) ---
# Define o endpoint do S3 para apontar para o LocalStack.
# Se o LocalStack estiver rodando no seu host e o container Glue separado,
# 'host.docker.internal' é a opção mais comum e robusta.
# Se estiver executando no mesmo container, 'localhost' pode funcionar.
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

# --- Caminhos S3 ---
# Caminho para o arquivo CSV de entrada no S3 do LocalStack
input_s3_path = "s3a://meu-bucket-dados-localstack/data/data.csv"
# Caminho para onde o Parquet transformado será salvo
output_s3_path = "s3a://meu-bucket-dados-localstack/output/filtered_data/"

print_line(f"Iniciando processo de ETL. Lendo de: {input_s3_path}")

# --- Extração (Read) ---
try:
    df_raw = spark.read \
        .option("header", "true") \
        .option("inferSchema", "true") \
        .csv(input_s3_path)

    print_line("Schema do DataFrame de entrada:")
    df_raw.printSchema()
    print_line("Dados de entrada:")
    df_raw.show()

    # --- Transformação (Transform) ---
    # Filtrar pessoas com idade maior que 30
    print_line("Aplicando transformação: Filtrando idade > 30...")
    df_filtered = df_raw.filter(df_raw.idade > 30)

    print_line("Schema do DataFrame transformado:")
    df_filtered.printSchema() # O schema deve ser o mesmo
    print_line("Dados transformados (idade > 30):")
    df_filtered.show()

    # --- Carga (Write) ---
    # Escrever o DataFrame transformado em formato Parquet para o S3
    print_line(f"Escrevendo dados transformados em formato Parquet para: {output_s3_path}")
    # Usamos .mode("overwrite") para sobrescrever se o diretório já existir
    # Você pode usar .mode("append") para adicionar, ou .mode("ignore") para não fazer nada se existir
    df_filtered.write \
        .mode("overwrite") \
        .parquet(output_s3_path)

    print_line("Processo ETL concluído com sucesso!")

except Exception as e:
    print_line(f"Ocorreu um erro durante o processo ETL: {e}")
    # Você pode adicionar um tratamento de erro mais sofisticado aqui, se necessário

# Finaliza o GlueContext (boa prática)
# glueContext.stop()
