import re

import pyspark.sql.functions as F
import pyspark.sql.types as T


def iso_duration_to_minutes(iso_duration: str) -> int:
    """
    Convert ISO 8601 duration to minutes.
    """
    match = re.match(r"PT(\d+H)?(\d+M)?", iso_duration)
    if not match:
        return 0
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    return hours * 60 + minutes


iso_duration_to_minutes_udf = F.udf(iso_duration_to_minutes, T.IntegerType())
