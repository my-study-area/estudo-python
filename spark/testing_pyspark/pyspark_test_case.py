import unittest
from pyspark.sql import SparkSession


class PySparkTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.spark: SparkSession = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.spark.stop()