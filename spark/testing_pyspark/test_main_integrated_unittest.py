from pyspark.testing.utils import assertDataFrameEqual

from spark.testing_pyspark.main import remove_extra_spaces
from spark.testing_pyspark.pyspark_test_case import PySparkTestCase


class TestTranformation(PySparkTestCase):
    def test_single_space(self):
        sample_data = [{"name": "John    D.", "age": 30},
                       {"name": "Alice   G.", "age": 25},
                       {"name": "Bob  T.", "age": 35},
                       {"name": "Eve   A.", "age": 28}]

        # Create a Spark DataFrame
        original_df = self.spark.createDataFrame(sample_data)

        # Apply the transformation function from before
        transformed_df = remove_extra_spaces(original_df, "name")

        expected_data = [{"name": "John D.", "age": 30},
        {"name": "Alice G.", "age": 25},
        {"name": "Bob T.", "age": 35},
        {"name": "Eve A.", "age": 28}]

        expected_df = self.spark.createDataFrame(expected_data)

        assertDataFrameEqual(transformed_df, expected_df)