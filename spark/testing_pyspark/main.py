from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import Column
from pyspark.sql.functions import col, regexp_replace

sample_data = [{"name": "John    D.", "age": 30},
  {"name": "Alice   G.", "age": 25},
  {"name": "Bob  T.", "age": 35},
  {"name": "Eve   A.", "age": 28}]


def main(spark_session: SparkSession) -> None:
    # Create a SparkSession
    df: DataFrame = spark_session.createDataFrame(sample_data)
    print(f"Before transform data")
    df.show()
    df: DataFrame = transform_data(df, "name")
    print(f"After transform data")
    df.show()


def create_spark_session() -> SparkSession:
    return SparkSession.builder.appName("Testing PySpark Example").getOrCreate()


# Remove additional spaces in name
def remove_extra_spaces(df: DataFrame, column_name: str) -> DataFrame:
    # Remove extra spaces from the specified column
    replace: Column = regexp_replace(col(column_name), "\\s+", " ")
    df_transformed: DataFrame = df.withColumn(column_name, replace)
    return df_transformed


def transform_data(df: DataFrame, name: str ="name") -> DataFrame:
    transformed_df: DataFrame = remove_extra_spaces(df, name)
    return transformed_df


if __name__ == '__main__': # pragma: no cover
    session = create_spark_session()
    main(session)