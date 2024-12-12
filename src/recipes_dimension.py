import pyspark.sql.types as T
from pyspark.sql import SparkSession


def create_recipes_dimension(spark: SparkSession, input_path: str, output_path: str) -> None:
    """
    Process the data to create or update the recipes dimension table.
    """

    input_schema = T.StructType([
        T.StructField("recipe_name", T.StringType(), False),
        T.StructField("cook_time_mins", T.IntegerType(), False),
        T.StructField("prep_time_mins", T.IntegerType(), False),
        T.StructField("description", T.StringType(), False),
        T.StructField("ingredients", T.StringType(), False),
        T.StructField("url", T.StringType(), False),
        T.StructField("image", T.StringType(), False),
        T.StructField("date_published", T.DateType(), False),
    ])

    df = spark.read.schema(input_schema).parquet(input_path)

    df.createOrReplaceTempView("recipes")

    result_df = spark.sql(
        """
        WITH deduped_recipes AS (
            SELECT
                recipe_name,
                max_by(cook_time_mins, date_published) AS cook_time_mins,
                max_by(prep_time_mins, date_published) AS prep_time_mins,
                max_by(description, date_published) AS description,
                max_by(ingredients, date_published) AS ingredients,
                max_by(url, date_published) AS url,
                max_by(image, date_published) AS image,
                max(date_published) AS date_published
            FROM recipes
            GROUP BY recipe_name
        )

        SELECT
            recipe_name,
            cook_time_mins,
            prep_time_mins,
            description,
            ingredients,
            url,
            image,
            date_published,
            cook_time_mins + prep_time_mins AS total_cook_time_mins,
            CASE
                WHEN cook_time_mins + prep_time_mins < 30 THEN 'easy'
                WHEN cook_time_mins + prep_time_mins < 60 THEN 'medium'
                ELSE 'hard'
            END AS difficulty
        FROM deduped_recipes
        """
    )

    result_df.write.parquet(output_path, mode="overwrite")
