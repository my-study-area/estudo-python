from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, regexp_replace


sample_data = [{"name": "John    D.", "age": 30},
  {"name": "Alice   G.", "age": 25},
  {"name": "Bob  T.", "age": 35},
  {"name": "Eve   A.", "age": 28}]

def main() -> None:
    # Create a SparkSession
    spark = SparkSession.builder.appName("Testing PySpark Example").getOrCreate()
    df = spark.createDataFrame(sample_data)
    print(f"Before transform data")
    df.show()
    df = transform_data(df, "name")
    print(f"After transform data")
    df.show()


# Remove additional spaces in name
def remove_extra_spaces(df, column_name):
    # Remove extra spaces from the specified column
    df_transformed = df.withColumn(column_name, regexp_replace(col(column_name), "\\s+", " "))
    return df_transformed


def transform_data(df, name="name") -> DataFrame:
    transformed_df = remove_extra_spaces(df, name)
    return transformed_df

if __name__ == '__main__':
    main()