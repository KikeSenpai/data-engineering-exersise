# Data Engineering Test

## Context

Events are ingested from a Kafka cluster and stored in our Data Lake on S3.
Events are sorted by arriving date. For example `events/recipe_changes/2019/11/29`.
During events processing we heavily rely on execution day to make sure we pick proper chunks of data and keep historical results.
We use Apache Spark to work with data and store it on S3 in parquet format. Our primary programming language is Python.
We have a service that can ingest data in JSON format to a selected S3 location.
We are interested in tracking changes to see available recipes, their cooking time and difficulty level.

### Task 1

Using Apache Spark and Python, read the source data, pre-process it and persist (write) it to ensure optimal structure and performance for further processing.
The source events are located on the `./data/input/` folder.

### Task 2

Using Apache Spark and Python read the processed dataset from *Task 1* and:
1. Extract only recipes that have `beef` as one of the ingredients.
2. Calculate average cooking time duration per difficulty level.
3. Persist dataset as CSV to the `output` folder. The dataset should have 2 columns: `difficulty` and `avg_total_cooking_time`.

Total cooking time duration can be calculated by the following formula:
```
total_cook_time = cookTime + prepTime
```

**Hint:** `cookTime` and `prepTime` are represented as durations in ISO format.

Criteria for levels based on total cook time duration:
- **easy** => less than 30 mins
- **medium** => between 30 and 60 mins
- **hard** => more than 60 mins.

## Deliverables

- A deployable Spark Application written in Python.
- A `README.md` file with a brief explanation of the approach, data exploration, assumptions/considerations and instructions on how to run the application.
- CSV output dataset from *Task 2*.

## Requirements

- Well structured code: we expect maintainability, extensibility, readability and well defined abstractions with clear responsibilities.
- Resiliency and scalability: the application should be able to handle variability of the data, and to scale if data volume increases.
- Solution is runnable locally on an isolated environment (e.g. Python virtual env or Docker container) and also deployable on a cluster (including dependency packaging). An iPython notebook is not sufficient.
- Unit tests for the different components.
- Proper exception handling.
- Logging.
- Documentation.

## Bonus points

- Config management.
- Data quality checks (like input/output dataset validation).
- How would you implement CI/CD for this application?
- How would you diagnose and tune the application in case of performance problems?
- How would you schedule this pipeline to run periodically?

*Good Luck!*
