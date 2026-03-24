from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# 1. Crie a SparkSession
spark = SparkSession.builder.appName("InnerJoinComIgualdade").getOrCreate()

# --- Criação dos DataFrames ---
dados_ratings = [
    {"cpfcnpj": "111.222.333-44", "segmento": "Tecnologia", "classificacao": "A"},
    {"cpfcnpj": "00.000.000/0001-00", "segmento": "Saúde", "classificacao": "B"},
    {"cpfcnpj": "999.888.777-66", "segmento": "Varejo", "classificacao": "A"},
]
df_ratings = spark.createDataFrame(dados_ratings)

dados_clientes = [
    {"num_doc": "111.222.333-44", "tipo_pessoa": "f", "nome": "Maria Silva"},
    {"num_doc": "11.000.000/0001-00", "tipo_pessoa": "j", "nome": "ABC Comércio Ltda"},
    {"num_doc": "555.666", "tipo_pessoa": "e", "nome": "John Doe Corp"},
]
df_clientes = spark.createDataFrame(dados_clientes)

# 2. Realize o INNER JOIN (Junção Interna) usando a condição de igualdade
# on=df_ratings["cpfcnpj"] == df_clientes["num_doc"]
df_join = df_ratings.join(
    other=df_clientes,
    on=df_ratings["cpfcnpj"] == df_clientes["num_doc"], # <--- A sintaxe da igualdade
    how="inner"
)

# 3. Selecione e organize as colunas
df_final = df_join.select(
    col("cpfcnpj").alias("documento"),
    col("nome"),
    col("tipo_pessoa"),
    col("segmento"),
    col("classificacao")
).orderBy("documento")

print("\n--- Resultado do INNER JOIN ---")
df_final.show()

# 4. Finaliza a SparkSession
spark.stop()
