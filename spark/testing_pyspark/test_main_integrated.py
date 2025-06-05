from spark.testing_pyspark.main import transform_data, sample_data
from pyspark.sql import SparkSession
from pyspark.testing.utils import assertDataFrameEqual
import os

# descomente a linha abaixo para configurar o JAVA_HOME para o spark no pycharm
# os.environ['JAVA_HOME']='/home/adriano/.asdf/installs/java/openjdk-17.0.2'
# Obs: também pode configurar o valor em "Run > Edit configurations ...", em "Enviroment variables"

def test_main():
    spark = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()
    expected_data = [{"name": "John D.", "age": 30},
                     {"name": "Alice G.", "age": 25},
                     {"name": "Bob T.", "age": 35},
                     {"name": "Eve A.", "age": 28}]
    expected_df = spark.createDataFrame(expected_data)
    df = spark.createDataFrame(sample_data)

    transformed_df = transform_data(df, "name")

    assertDataFrameEqual(transformed_df, expected_df)
