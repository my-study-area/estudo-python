# meu_primeiro_app.py
from pyspark.sql import SparkSession

def print_local(mensagem :str) -> None:
    print("=============================================\n")
    print(f"\n {mensagem} \n")
    print("=============================================\n")

if __name__ == "__main__":
    # Inicializa a SparkSession.
    # .appName define o nome do seu aplicativo no Spark UI.
    # .master("local[*]") diz ao Spark para rodar localmente, usando todos os núcleos disponíveis.
    spark = SparkSession.builder \
        .appName("MeuPrimeiroAppLocal") \
        .master("local[*]") \
        .getOrCreate()

    print_local("SparkSession criada com sucesso!")

    # 1. Crie um DataFrame simples
    dados = [("João", 25, "Engenheiro"),
             ("Maria", 30, "Médica"),
             ("Pedro", 22, "Estudante"),
             ("Ana", 35, "Professora")]

    colunas = ["Nome", "Idade", "Profissao"]

    df = spark.createDataFrame(dados, colunas)

    print_local("DataFrame Original:")
    df.show()

    # 2. Faça uma operação Spark: Filtrar por idade
    df_filtrado = df.filter(df.Idade > 28)

    print_local("DataFrame Filtrado (Idade > 28):")
    df_filtrado.show()

    # 3. Faça outra operação Spark: Contar registros
    total_registros = df.count()
    print_local(f"Total de registros no DataFrame original: {total_registros}")

    # 4. Parar a SparkSession. Isso é importante para liberar recursos.
    spark.stop()
    print_local("SparkSession encerrada. Fim do aplicativo.")