# Spark

```bash
source ../venv/bin/activate.fish

which python

pip install --upgrade pip

pip install -r requirements.txt

spark-submit meu_primeiro_app.py
```

## Passo gerado pelo Gemini

### Passo 3: Testar o PySpark Shell Interativo

Agora que tudo está configurado, vamos ver se o PySpark funciona.

1.  **Abra o terminal ou prompt de comando.**
2.  **Digite `pyspark`:**

    ```bash
    pyspark
    ```

    Se tudo estiver correto, você verá muitas mensagens de log (normal!) e, em seguida, um prompt Python, indicando que o **SparkSession** e o **SparkContext** foram iniciados. Você verá algo como:

    ```
    Python 3.x.x (default, ...)
    [GCC ...] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    Welcome to
          ____              __
         / __/__  ___ _____/ /__
        _\ \/ _ \/ _ `/ __/  '_/
       /__ / .__/\_,_/_/ /_/\_\   version 3.x.x
         /_/

    Using Python version 3.x.x with Spark version 3.x.x
    SparkSession available as 'spark'.
    SparkContext available as 'sc'.
    >>>
    ```

3.  **Execute um código simples:** No prompt `>>>`, digite:

    ```python
    data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
    df = spark.createDataFrame(data, ["Name", "ID"])
    df.show()
    ```

    Você deverá ver a seguinte saída:

    ```
    +-------+---+
    |   Name| ID|
    +-------+---+
    |  Alice|  1|
    |    Bob|  2|
    |Charlie|  3|
    +-------+---+
    ```

    Isso significa que o PySpark está funcionando e você conseguiu criar seu primeiro DataFrame!
4.  **Para sair do shell PySpark:** Digite `exit()` e pressione Enter.

---

### Passo 4: Executar um Script PySpark do Zero

Agora, vamos criar um arquivo Python e executá-lo como um trabalho Spark.

1.  **Crie um arquivo Python:**
    * Abra um editor de texto (VS Code, Sublime Text, Bloco de Notas, etc.).
    * Cole o seguinte código e salve o arquivo como `meu_primeiro_app.py` em algum lugar fácil de acessar (ex: sua área de trabalho).

    ```python
    # meu_primeiro_app.py
    from pyspark.sql import SparkSession

    if __name__ == "__main__":
        # Inicializa a SparkSession.
        # .appName define o nome do seu aplicativo no Spark UI.
        # .master("local[*]") diz ao Spark para rodar localmente, usando todos os núcleos disponíveis.
        spark = SparkSession.builder \
            .appName("MeuPrimeiroAppLocal") \
            .master("local[*]") \
            .getOrCreate()

        print("SparkSession criada com sucesso!")

        # 1. Crie um DataFrame simples
        dados = [("João", 25, "Engenheiro"),
                 ("Maria", 30, "Médica"),
                 ("Pedro", 22, "Estudante"),
                 ("Ana", 35, "Professora")]

        colunas = ["Nome", "Idade", "Profissao"]

        df = spark.createDataFrame(dados, colunas)

        print("\nDataFrame Original:")
        df.show()

        # 2. Faça uma operação Spark: Filtrar por idade
        df_filtrado = df.filter(df.Idade > 28)

        print("\nDataFrame Filtrado (Idade > 28):")
        df_filtrado.show()

        # 3. Faça outra operação Spark: Contar registros
        total_registros = df.count()
        print(f"\nTotal de registros no DataFrame original: {total_registros}")

        # 4. Parar a SparkSession. Isso é importante para liberar recursos.
        spark.stop()
        print("\nSparkSession encerrada. Fim do aplicativo.")
    ```

2.  **Execute o script usando `spark-submit`:**
    * Abra seu terminal ou prompt de comando.
    * Navegue até o diretório onde você salvou `meu_primeiro_app.py`.
    * Execute o comando:

        ```bash
        spark-submit meu_primeiro_app.py
        ```

    Você verá muitos logs do Spark (o que é normal), seguidos pelas saídas dos seus `print()` e `df.show()`:

    ```
    SparkSession criada com sucesso!

    DataFrame Original:
    +-----+-----+----------+
    | Nome|Idade|  Profissao|
    +-----+-----+----------+
    | João|   25|Engenheiro|
    |Maria|   30|    Médica|
    |Pedro|   22| Estudante|
    |  Ana|   35| Professora|
    +-----+-----+----------+

    DataFrame Filtrado (Idade > 28):
    +-----+-----+----------+
    | Nome|Idade|  Profissao|
    +-----+-----+----------+
    |Maria|   30|    Médica|
    |  Ana|   35| Professora|
    +-----+-----+----------+

    Total de registros no DataFrame original: 4

    SparkSession encerrada. Fim do aplicativo.
    ```

---

### Próximos Passos e Dicas para Iniciantes:

* **Entenda `SparkSession`:** É o ponto de entrada principal para programar Spark com a API DataFrame e SQL. `master("local[*]")` é crucial para rodar localmente.
* **DataFrames:** Pense neles como tabelas em um banco de dados relacional, mas distribuídas. São a estrutura de dados central no PySpark para trabalhar com dados estruturados.
* **Operações Lazies:** Muitas operações Spark (como `filter`, `select`) são "lazies". Elas não são executadas imediatamente, mas sim quando uma "ação" (como `show()`, `count()`, `write()`) é chamada.
* **Documentação Oficial:** O site do Apache Spark tem uma excelente documentação para PySpark.
* **Cursos Online:** Existem muitos cursos gratuitos e pagos que podem aprofundar seu conhecimento em PySpark.

Parabéns! Você acabou de configurar seu ambiente Spark local e executou seus primeiros códigos PySpark. Este é o ponto de partida para explorar o poder do processamento de dados distribuídos.

### FAQ de Erros
```commandline
/home/adriano/github-workspace/estudo-python/venv/bin/python /home/adriano/github-workspace/estudo-python/spark/meu_primeiro_app.py 
JAVA_HOME is not set
Traceback (most recent call last):
  File "/home/adriano/github-workspace/estudo-python/spark/meu_primeiro_app.py", line 16, in <module>
    .getOrCreate()
     ^^^^^^^^^^^^^
  File "/home/adriano/github-workspace/estudo-python/venv/lib/python3.12/site-packages/pyspark/sql/session.py", line 556, in getOrCreate
    sc = SparkContext.getOrCreate(sparkConf)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/adriano/github-workspace/estudo-python/venv/lib/python3.12/site-packages/pyspark/core/context.py", line 523, in getOrCreate
    SparkContext(conf=conf or SparkConf())
  File "/home/adriano/github-workspace/estudo-python/venv/lib/python3.12/site-packages/pyspark/core/context.py", line 205, in __init__
    SparkContext._ensure_initialized(self, gateway=gateway, conf=conf)
  File "/home/adriano/github-workspace/estudo-python/venv/lib/python3.12/site-packages/pyspark/core/context.py", line 444, in _ensure_initialized
    SparkContext._gateway = gateway or launch_gateway(conf)
                                       ^^^^^^^^^^^^^^^^^^^^
  File "/home/adriano/github-workspace/estudo-python/venv/lib/python3.12/site-packages/pyspark/java_gateway.py", line 111, in launch_gateway
    raise PySparkRuntimeError(
pyspark.errors.exceptions.base.PySparkRuntimeError: [JAVA_GATEWAY_EXITED] Java gateway process exited before sending its port number.

Process finished with exit code 1
```
Para corrigir basta configurar o `JAVA_HOME` nas configurações de execução no pycharm.

Vá em `Run > Edit configurations ... ` e cole em **Enviroment variables**:
```commandline
JAVA_HOME=/home/adriano/.asdf/installs/java/openjdk-17.0.2
```