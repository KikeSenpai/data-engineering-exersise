# Data Engineering Test

Hello there! My name is Enrique Perez and this is my solution to the HF Data Engineering take-home test.

The original requirements are [here](./requirements.md).

## Development setup

To set up the development environment please follow the following steps:

1. Install Python 3.10+
2. In the project directory run `make install-deps-dev`.
3. Done! You are ready to start developing the app.

## Running tests

In the project directory run:
```bash
make unit-tests
```

## How to run the app

We will run the app from the virtual environment, while in the project directory run:

```bash
make run-spark-app
```

**Done!**

## Approach explanation

### Project structure

The basic structure is the following:

```text
├── app.py
├── data
├── input
├── output
├── src
│   ├── __init__.py
│   ├── custom_exceptions.py
│   ├── data_processing.py
│   ├── load_events.py
│   └── utils.py
```

* The `src` folder contains all the functions required to read and process the data, as well as other utilities for error handling and logging.
* `load_events.py` contains the code required to fulfill Task #1.
* The `data` folder contains the persisted output from Task #1 in parquet file format.
* `data_processing.py` contains the code required to fulfill Task #2.
* `app.py` executes both tasks in order to produce the desired dataset.

### Data exploring and assumptions

* As source events are coming in JSON format, and JSON does not enforce a strict schema by default, no schema is enforced during the reading of these events.
* The `cookTime` and `prepTime` fields are strings representing duration of time in the ISO 8601 format, so during Task #1 these fields are transform to duration in minutes of integer datatype, persisting the data in a easier way for further processing later. As there's no a built-in way to do this and preferred to not rely on additional packages or UDF, regular expressions were used in order to accomplish this transformation.
* Few duplicated recipes were found on the data, nonetheless one of them had the same `datePulished` value, so no clear criteria for eliminating duplicate values was found; but as none of these recipes have no beef the final output wouldn't be affected.
* Three (3) recipes without name were spotted these were filtered out during Task #1.

### Code style and type checks

* `make code-style` will keep the code tidy, using `black` for the format, `isort` to organize import statements and `flake8` for style.
* `make check-types` will help you prevent type-related bugs, using `mypy` and the type annotations.

## Bonus points

### Ideas for next steps

* For deployment a cloud-based cluster could be used, e.g., AWS EMR, and a configuration management tool like Terraform can be used to define and manage the deployment infrastructure. As the latest version of AWS EMR is 6.13 for the moment of this writing, `pyspark 3.4.1` was used, which is the lastest version of `spark` compatible with EMR 6.13.
* In case of performance problems I'd consider the use of `repartition()` or `coalesce()` operations to control the partitioning and minimize data shuffling, especially before aggregating data.
* To run the app periodically I would use AWS Lambda, creating a Lambda function that triggers the execution of our app using AWS EventBridge.
