from pyspark.sql import SparkSession

from src.beef_avg_cook_time import calculate_beef_avg_cook_time
from src.load_events import load_events_to_s3
from src.recipes_dimension import create_recipes_dimension


def main():
    spark = SparkSession.builder.appName("RecipeClassifier").getOrCreate()

    input_path = "./data/input"
    bronze_layer_path = "./data/bronze/recipes"
    silver_layer_path = "./data/silver/recipes"
    output_path = "./data/output"

    load_events_to_s3(spark, input_path, bronze_layer_path)

    create_recipes_dimension(spark, bronze_layer_path, silver_layer_path)

    calculate_beef_avg_cook_time(spark, silver_layer_path, output_path)

    spark.stop()

if __name__ == "__main__":
    main()
