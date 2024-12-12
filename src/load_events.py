import os

import pyspark.sql.functions as F
from pyspark.sql import SparkSession

from src.utils import iso_duration_to_minutes_udf


def load_events_to_s3(spark: SparkSession, input_path: str, output_path: str) -> None:
    """
    Load events data to S3.
    """

    files = [os.path.join(input_path, file) for file in os.listdir(input_path) if file.endswith(".jsonl")]

    df = spark.read.json(files)

    df = (
        df
        .select(
            F.col("name").alias("recipe_name"),
            F.col("datePublished").alias("date_published").cast("date"),
            iso_duration_to_minutes_udf(F.col("cookTime")).alias("cook_time_mins").cast("int"),
            iso_duration_to_minutes_udf(F.col("prepTime")).alias("prep_time_mins").cast("int"),
            F.col("description"),
            F.col("ingredients"),
            F.col("url"),
            F.col("image"),
        )
        .filter((F.col("recipe_name").isNotNull()) & (F.col("recipe_name") != ""))
    )

    df.write.partitionBy("date_published").parquet(output_path, mode="overwrite")
