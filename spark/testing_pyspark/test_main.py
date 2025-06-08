import unittest
from unittest.mock import patch, MagicMock

from pyspark.sql import DataFrame, SparkSession
from pyspark.testing.utils import assertDataFrameEqual

from spark.testing_pyspark.main import create_spark_session, transform_data, remove_extra_spaces, main, sample_data


class TestMainUnitTest(unittest.TestCase):

    @patch('spark.testing_pyspark.main.transform_data')
    def test_main(self, mock_tranform_data):
        mock_spark_session = MagicMock(spec=SparkSession)
        mock_create_df_return = MagicMock(spec=DataFrame)
        mock_tranform_data_return = MagicMock(spec=DataFrame)
        mock_spark_session.createDataFrame.return_value = mock_create_df_return
        mock_tranform_data.return_value = mock_tranform_data_return

        main(mock_spark_session)

        mock_spark_session.createDataFrame.assert_called_once_with(sample_data)
        mock_tranform_data.assert_called_once_with(mock_create_df_return, 'name')
        mock_create_df_return.show.assert_called_once()
        mock_tranform_data_return.show.assert_called_once()


    @patch('spark.testing_pyspark.main.SparkSession', spec=SparkSession)
    def test_create_session(self, mock_spark_session):
        mock_builder = MagicMock(spec=SparkSession.Builder)
        mock_app_name = MagicMock(spec=SparkSession.Builder)
        mock_get_create_return = MagicMock(spec=SparkSession)
        mock_spark_session.builder = mock_builder
        mock_builder.appName.return_value = mock_app_name
        mock_app_name.getOrCreate.return_value = mock_get_create_return

        session = create_spark_session()

        self.assertTrue(mock_app_name.getOrCreate.called)
        self.assertEqual(mock_get_create_return, session)


    @patch('spark.testing_pyspark.main.remove_extra_spaces')
    @patch('spark.testing_pyspark.main.SparkSession', spec=SparkSession)
    def test_transform_data(self, mock_spark_session, mock_remove_extra_spaces: MagicMock):
        sample_data = [{"name": "John    D.", "age": 30},
                       {"name": "Alice   G.", "age": 25},
                       {"name": "Bob  T.", "age": 35},
                       {"name": "Eve   A.", "age": 28}]
        df = mock_spark_session.createDataFrame(sample_data)
        df_without_extra_spaces = [{"name": "John D.", "age": 30},
        {"name": "Alice G.", "age": 25},
        {"name": "Bob T.", "age": 35},
        {"name": "Eve A.", "age": 28}]
        mock_remove_extra_spaces.return_value = df_without_extra_spaces

        result = transform_data(df, 'name')

        self.assertTrue(mock_remove_extra_spaces.called)
        assertDataFrameEqual(df_without_extra_spaces, result)
        mock_remove_extra_spaces.assert_called_once_with(df, 'name')

    @patch('spark.testing_pyspark.main.DataFrame', spec=DataFrame)
    @patch('spark.testing_pyspark.main.col')
    @patch('spark.testing_pyspark.main.regexp_replace')
    def test_remove_extra_spaces(self, mock_regexp_replace: MagicMock, mock_col, mock_spark_session: MagicMock):
        mock_col_return = MagicMock()
        mock_regex_return = MagicMock()
        mock_with_column_return = MagicMock()
        mock_col.return_value = mock_col_return
        mock_regexp_replace.return_value = mock_regex_return
        mock_spark_session.withColumn.return_value = mock_with_column_return

        result: DataFrame = remove_extra_spaces(mock_spark_session, "name")

        mock_col.assert_called_once_with('name')
        mock_regexp_replace.assert_called_once_with(mock_col_return, "\\s+", " ")
        mock_spark_session.withColumn.assert_called_once_with('name', mock_regex_return)
        self.assertEqual(result, mock_with_column_return)
