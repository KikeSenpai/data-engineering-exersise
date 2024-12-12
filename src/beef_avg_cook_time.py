import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql import SparkSession


def calculate_beef_avg_cook_time(spark: SparkSession, input_path: str, output_path: str) -> None:
    """
    Process the data to calculate the average cooking time for beef recipes by recipe difficulty level.
    """

    select_cols = ["recipe_name", "ingredients", "difficulty", "total_cook_time_mins"]

    input_schema = T.StructType([
        T.StructField("recipe_name", T.StringType(), False),
        T.StructField("cook_time_mins", T.IntegerType(), False),
        T.StructField("prep_time_mins", T.IntegerType(), False),
        T.StructField("description", T.StringType(), False),
        T.StructField("ingredients", T.StringType(), False),
        T.StructField("url", T.StringType(), False),
        T.StructField("image", T.StringType(), False),
        T.StructField("date_published", T.DateType(), False),
        T.StructField("total_cook_time_mins", T.IntegerType(), False),
        T.StructField("difficulty", T.StringType(), False),
    ])

    df = spark.read.schema(input_schema).parquet(input_path).select(*select_cols)

    df = (
        df
        .filter(F.lower(F.col("ingredients")).contains("beef"))
        .groupBy("difficulty")
        .agg(F.coalesce(F.avg("total_cook_time_mins"), F.lit(0)).alias("avg_total_cook_time_mins"))
    )

    df.write.csv(output_path, mode="overwrite", header=True)
