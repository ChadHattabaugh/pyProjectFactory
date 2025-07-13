"""Data utilities for {{PROJECT_NAME}}."""

import logging
from pathlib import Path
from typing import Any, Dict, Optional, Union

import pandas as pd
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


def read_data(
    file_path: Union[str, Path],
    spark: Optional[SparkSession] = None,
    format_type: Optional[str] = None,
    **kwargs: Any,
) -> Union[pd.DataFrame, SparkDataFrame]:
    """Read data from various formats.
    
    Args:
        file_path: Path to the data file
        spark: SparkSession for reading with Spark (optional)
        format_type: Format type (csv, parquet, json, etc.)
        **kwargs: Additional arguments for the reader
        
    Returns:
        DataFrame (pandas or Spark depending on spark parameter)
    """
    file_path = Path(file_path)

    if format_type is None:
        format_type = file_path.suffix.lower().lstrip(".")

    if spark is not None:
        return _read_with_spark(spark, file_path, format_type, **kwargs)
    else:
        return _read_with_pandas(file_path, format_type, **kwargs)


def _read_with_pandas(
    file_path: Path,
    format_type: str,
    **kwargs: Any,
) -> pd.DataFrame:
    """Read data with pandas."""
    readers = {
        "csv": pd.read_csv,
        "json": pd.read_json,
        "parquet": pd.read_parquet,
        "xlsx": pd.read_excel,
        "xls": pd.read_excel,
    }

    if format_type not in readers:
        raise ValueError(f"Unsupported format: {format_type}")

    logger.info(f"Reading {file_path} with pandas")
    return readers[format_type](file_path, **kwargs)


def _read_with_spark(
    spark: SparkSession,
    file_path: Path,
    format_type: str,
    **kwargs: Any,
) -> SparkDataFrame:
    """Read data with Spark."""
    logger.info(f"Reading {file_path} with Spark")

    reader = spark.read

    # Apply options
    for key, value in kwargs.items():
        reader = reader.option(key, value)

    if format_type == "csv":
        return reader.csv(str(file_path), header=True, inferSchema=True)
    elif format_type == "json":
        return reader.json(str(file_path))
    elif format_type == "parquet":
        return reader.parquet(str(file_path))
    else:
        raise ValueError(f"Unsupported Spark format: {format_type}")


def write_data(
    df: Union[pd.DataFrame, SparkDataFrame],
    file_path: Union[str, Path],
    format_type: Optional[str] = None,
    mode: str = "overwrite",
    **kwargs: Any,
) -> None:
    """Write data to various formats.
    
    Args:
        df: DataFrame to write
        file_path: Output file path
        format_type: Format type (csv, parquet, json, etc.)
        mode: Write mode (overwrite, append, etc.)
        **kwargs: Additional arguments for the writer
    """
    file_path = Path(file_path)

    if format_type is None:
        format_type = file_path.suffix.lower().lstrip(".")

    if isinstance(df, SparkDataFrame):
        _write_with_spark(df, file_path, format_type, mode, **kwargs)
    else:
        _write_with_pandas(df, file_path, format_type, **kwargs)


def _write_with_pandas(
    df: pd.DataFrame,
    file_path: Path,
    format_type: str,
    **kwargs: Any,
) -> None:
    """Write data with pandas."""
    # Create parent directory if it doesn't exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    writers = {
        "csv": lambda df, path, **kw: df.to_csv(path, index=False, **kw),
        "json": lambda df, path, **kw: df.to_json(path, orient="records", **kw),
        "parquet": lambda df, path, **kw: df.to_parquet(path, **kw),
        "xlsx": lambda df, path, **kw: df.to_excel(path, index=False, **kw),
    }

    if format_type not in writers:
        raise ValueError(f"Unsupported format: {format_type}")

    logger.info(f"Writing to {file_path} with pandas")
    writers[format_type](df, file_path, **kwargs)


def _write_with_spark(
    df: SparkDataFrame,
    file_path: Path,
    format_type: str,
    mode: str,
    **kwargs: Any,
) -> None:
    """Write data with Spark."""
    logger.info(f"Writing to {file_path} with Spark")

    writer = df.write.mode(mode)

    # Apply options
    for key, value in kwargs.items():
        writer = writer.option(key, value)

    if format_type == "csv":
        writer.csv(str(file_path), header=True)
    elif format_type == "json":
        writer.json(str(file_path))
    elif format_type == "parquet":
        writer.parquet(str(file_path))
    else:
        raise ValueError(f"Unsupported Spark format: {format_type}")


def get_data_info(df: Union[pd.DataFrame, SparkDataFrame]) -> Dict[str, Any]:
    """Get information about a DataFrame.
    
    Args:
        df: DataFrame to analyze
        
    Returns:
        Dictionary with DataFrame information
    """
    if isinstance(df, SparkDataFrame):
        return _get_spark_info(df)
    else:
        return _get_pandas_info(df)


def _get_pandas_info(df: pd.DataFrame) -> Dict[str, Any]:
    """Get pandas DataFrame information."""
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.to_dict(),
        "memory_usage": df.memory_usage(deep=True).sum(),
        "null_counts": df.isnull().sum().to_dict(),
    }


def _get_spark_info(df: SparkDataFrame) -> Dict[str, Any]:
    """Get Spark DataFrame information."""
    return {
        "columns": df.columns,
        "schema": str(df.schema),
        "count": df.count(),
        "null_counts": {col: df.filter(df[col].isNull()).count() for col in df.columns},
    }
