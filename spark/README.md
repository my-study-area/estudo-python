# Spark

```bash
source ../venv/bin/activate.fish

which python

pip install --upgrade pip

pip install -r requirements.txt

spark-submit meu_primeiro_app.py
```

## Pyspark
Execução dos testes com Pyspark:
```
# dentro de ./spark/testing_pyspark
pytest --cov ./ --cov-branch --cov-report term-missing
```

## Pyspark/Glue com docker
```bash
# dentro de spark/pyspark-glue

# inicia containers
docker compose up -d

# acessa o bash do glue
docker compose exec glue bash

# cria o bucket
aws s3 mb s3://meu-bucket-dados-localstack

# lista os buckets
aws s3 ls

# executa o script hello
spark-submit workspace/src/hello.py

# copia arquivo csv para bucket
aws s3 cp workspace/src/data.csv s3://meu-bucket-dados-localstack/data/data.csv

# lista arquivo csv
aws s3 ls s3://meu-bucket-dados-localstack/data/

# lê arquivo csv do bucket
spark-submit workspace/src/read_s3_data.py 

# transforma e carrega arquivo no bucket s3 como parquet
spark-submit workspace/src/transform_and_load.py 

# Verifica se o arquivo parquet criado no localstack
aws s3 ls s3://meu-bucket-dados-localstack/output/filtered_data/

# lê arquivo parquet gerado anteriormente no s3
spark-submit workspace/src/read_parquet.py 

# copia do arquivo parquet do s3 para o diretório local
aws s3 cp s3://meu-bucket-dados-localstack/output/filtered_data/part-00000-7d936b73-fd30-4e2d-888e-f9d2b1e8adc2-c000.snappy.parquet ./my_filtered_data.parquet

# lê e escreve arquivo com dynamicframe no S3 
spark-submit workspace/src/etl_with_dynamicframe.py

# lê arquivos parquet gerado anteriormente no s3
spark-submit workspace/src/read_parquet.py 
```

> [!CAUTION]
> Os arquivos sample e test-sample, precisam de uma conta válida na aws.

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

Opção 1:

Vá em `Run > Edit configurations ... ` e cole em **Enviroment variables**:
```commandline
JAVA_HOME=/home/adriano/.asdf/installs/java/openjdk-17.0.2
```

Opção 2:

Inicie o pycharm do seu terminal que já possui a variável de ambiente configurada



### Passo para resolver os problemas enfrentados ao configurar o docker com Glue/Pyspark e Localstack
```bash
docker run -it --rm -v /home/adriano/Downloads/testes/python/glue:/home/hadoop/workspace -v public.ecr.aws/glue/aws-glue-libs:5 -c bash
docker run -it --rm -v $PWD:/home/hadoop/workspace -v $HOME:/home/hadoop/.aws -e AWS_PROFILE=localstack public.ecr.aws/glue/aws-glue-libs:5 -c bash

spark-submit workspace/src/sample.py

docker run -it --rm -v $PWD:/home/hadoop/workspace -v $HOME/.aws:/home/hadoop/.aws -e AWS_PROFILE=localstack --network=pyspark-glue_default public.ecr.aws/glue/aws-glue-libs:5 -c bash
aws s3 ls --endpoint-url=http:localstack:4566



aws configure --profile pyspark
docker run -it --rm -v $PWD:/home/hadoop/workspace -v $HOME/.aws:/home/hadoop/.aws -e AWS_PROFILE=pyspark --network=pyspark-glue_default public.ecr.aws/glue/aws-glue-libs:5 -c bash
aws s3 ls --endpoint-url=http://localstack:4566


docker compose exec glue bash
```

```yml
services:
  glue:
    image: public.ecr.aws/glue/aws-glue-libs:5
    volumes:
      - /home/adriano/Downloads/testes/python/glue:/home/hadoop/workspace
    command: 
      - -c 
      - tail -f /dev/null

```

```
# assisti um vídeo de configuração do pychram com o interpretador python apontando para o docker. O arquivo utilizado foi o exemplo abaixo:
https://github.com/AdrianoNicolucci/dataenguncomplicated/blob/main/aws_glue/firstGlueScript.py

# Url para acessar o LocalStack executado com docker. Obs: é necessário criar uma conta gratuita para acessar o painel web.
https://app.localstack.cloud/


aws s3api create-bucket --bucket teste

# acessar como root no container
docker exec -it -u root 49669e16189d bash

# verica a comunicação com o localstack
nc -vz localstack 4566
```

Backup da V1 do docker-compose.yml:
```yml
services:
  localstack:
    container_name: localstack
    image: localstack/localstack
    ports:
      - "127.0.0.1:4566:4566"            # LocalStack Gateway
      - "127.0.0.1:4510-4559:4510-4559"  # external services port range
    environment:
      - DEBUG=${DEBUG:-0}
    volumes:
      - "${LOCALSTACK_VOLUME_DIR:-./volume}:/var/lib/localstack"
      - "/var/run/docker.sock:/var/run/docker.sock"

  glue-job-runner:
    container_name: glue-job-runner
    image: public.ecr.aws/glue/aws-glue-libs:5 # Sua imagem Glue
    # Certifique-se de que este contêiner possa se comunicar com o LocalStack
    environment:
      - AWS_ACCESS_KEY_ID=test
      - AWS_SECRET_ACCESS_KEY=test
      - AWS_DEFAULT_REGION=us-east-1
      # Aponta o Spark para o endpoint do LocalStack para Glue e S3
      - SPARK_CONF_spark.hadoop.fs.s3a.endpoint=http://localstack:4566
      - SPARK_CONF_spark.hadoop.fs.s3a.path.style.access=true
      - SPARK_CONF_spark.hadoop.fs.s3a.impl=org.apache.hadoop.fs.s3a.S3AFileSystem
      - SPARK_CONF_spark.hadoop.fs.s3a.aws.credentials.provider=org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider
      - AWS_ENDPOINT_URL=http://localstack:4566 # Para boto3 ou outras ferramentas AWS
      # Isso é crítico para GlueContext e outras APIs AWS usarem LocalStack
      - AWS_GLUE_ENDPOINT=http://localstack:4566
    volumes:
      - ./jobs:/home/glue_user/workspace # Mapeia seu diretório de jobs
#      - ~/.aws:/home/glue_user/.aws:ro # Opcional: para usar perfis AWS locais
    depends_on:
      - localstack
    command: ["tail", "-f", "/dev/null"] # Mantém o contêiner rodando para comandos manuais

volumes:
  localstack_data:
```
