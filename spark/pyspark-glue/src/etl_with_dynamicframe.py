import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions
from awsglue.dynamicframe import DynamicFrame # Importa DynamicFrame explicitamente


def print_line(message):
    print("=====================================================================================")
    print(message)
    print("=====================================================================================")
    print()


# --- Configuração para LocalStack (Revisão Importante!) ---
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

# --- Caminhos S3 ---
# Caminho para o arquivo CSV de entrada no S3 do LocalStack
input_s3_path = "s3a://meu-bucket-dados-localstack/data/" # Aponta para o diretório, o Glue encontra o CSV
# Caminho para onde o Parquet transformado será salvo
output_s3_path = "s3a://meu-bucket-dados-localstack/output/dynamicframe_filtered_data/"

print_line(f"Iniciando processo ETL com DynamicFrame. Lendo de: {input_s3_path}")

# --- Extração (Read) usando DynamicFrame ---
try:
    # Cria um DynamicFrame a partir do CSV no S3
    # Note que passamos o diretório 'data/' e o Glue infere o CSV dentro
    dynamic_frame_raw = glueContext.create_dynamic_frame.from_options(
        connection_type="s3",
        connection_options={"paths": [input_s3_path], "recurse": True},
        format="csv",
        format_options={"withHeader": True, "inferSchema": True},
        transformation_ctx="dynamic_frame_raw"
    )

    print_line("Schema do DynamicFrame de entrada:")
    dynamic_frame_raw.printSchema()
    print_line("Dados do DynamicFrame de entrada (primeiras linhas):")
    # Para visualizar os dados, convertemos para Spark DataFrame para usar .show()
    dynamic_frame_raw.toDF().show()

    # --- Transformação (Transform) ---
    # Para operações complexas, é comum converter DynamicFrame para Spark DataFrame
    # aplicar as transformações e depois converter de volta.
    print_line("Convertendo DynamicFrame para Spark DataFrame para aplicar transformação...")
    df_raw = dynamic_frame_raw.toDF()

    print_line("Aplicando transformação: Filtrando idade > 30...")
    df_filtered = df_raw.filter(df_raw.idade > 30)

    print_line("Schema do DataFrame transformado:")
    df_filtered.printSchema()
    print_line("Dados transformados (idade > 30):")
    df_filtered.show()

    # --- Carga (Write) usando DynamicFrame ---
    # Converte o Spark DataFrame filtrado de volta para DynamicFrame para a escrita
    print_line("Convertendo Spark DataFrame filtrado de volta para DynamicFrame para escrita...")
    dynamic_frame_filtered = DynamicFrame.fromDF(df_filtered, glueContext, "dynamic_frame_filtered")

    print_line(f"Escrevendo DynamicFrame transformado em formato Parquet para: {output_s3_path}")
    glueContext.write_dynamic_frame.from_options(
        frame=dynamic_frame_filtered,
        connection_type="s3",
        connection_options={"path": output_s3_path},
        format="parquet",
        format_options={}, # Nenhuma opção específica para parquet neste caso
        transformation_ctx="write_dynamic_frame_filtered",
        # Adiciona a opção "overwrite" diretamente na conexão para o modo de escrita
        # Isso substitui o modo do DataFrame.write
        # Note: No Glue, o overwrite é geralmente controlado pelo Data Catalog ou pela partição
        # Para S3, um caminho simples sem partição, ele geralmente sobrescreve o conteúdo do diretório.
        # No LocalStack, o comportamento é similar ao Spark DataFrame .mode("overwrite").
    )

    print_line("Processo ETL com DynamicFrame concluído com sucesso!")

except Exception as e:
    print_line(f"Ocorreu um erro durante o processo ETL com DynamicFrame: {e}")

# Não precisamos chamar glueContext.stop() ou sc.stop() aqui.
