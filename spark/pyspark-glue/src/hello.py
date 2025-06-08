import sys
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.utils import getResolvedOptions

# Inicializa o SparkContext e GlueContext
sc = SparkContext.getOrCreate()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Nosso "Hello World"
print("Hello World do AWS Glue com PySpark!")

# Para um script Glue que processa dados, você normalmente adicionaria
# lógica de ETL (Extração, Transformação, Carga) aqui.
# Por enquanto, apenas a impressão é suficiente.

# Para garantir que o Job finalize corretamente (opcional, mas boa prática)
# O Glue geralmente lida com isso, mas para scripts mais complexos é útil
# glueContext.stop() # Descomente se tiver problemas de encerramento em scripts mais complexos
