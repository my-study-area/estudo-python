# meu_primeiro_app.py
from typing import Tuple

import pyspark.sql
from pyspark.sql import SparkSession, DataFrame

def print_local(mensagem :str) -> None:
    print("=============================================\n")
    print(f"\n {mensagem} \n")
    print("=============================================\n")

if __name__ == "__main__":
    # Inicializa a SparkSession.
    # .appName define o nome do seu aplicativo no Spark UI.
    # .master("local[*]") diz ao Spark para rodar localmente, usando todos os núcleos disponíveis.
    spark: SparkSession = SparkSession.builder \
        .appName("MeuPrimeiroAppLocal") \
        .master("local[*]") \
        .getOrCreate()

    print_local("SparkSession criada com sucesso!")

    # 1. Crie um DataFrame simples
    dados: list[Tuple[str, int, str]] = [("João", 25, "Engenheiro"),
             ("Maria", 30, "Médica"),
             ("Pedro", 22, "Estudante"),
             ("Ana", 35, "Professora")]

    colunas: list[str] = ["Nome", "Idade", "Profissao"]

    df: DataFrame = spark.createDataFrame(dados, colunas)

    print_local("DataFrame Original:")
    df.show()

    # 2. Faça uma operação Spark: Filtrar por idade
    df_filtrado: DataFrame = df.filter(df.Idade > 28)

    print_local("DataFrame Filtrado (Idade > 28):")
    df_filtrado.show()

    # 3. Faça outra operação Spark: Contar registros
    total_registros: int = df.count()
    print_local(f"Total de registros no DataFrame original: {total_registros}")

    # 4. Parar a SparkSession. Isso é importante para liberar recursos.
    spark.stop()
    print_local("SparkSession encerrada. Fim do aplicativo.")