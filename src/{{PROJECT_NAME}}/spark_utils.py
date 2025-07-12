"""Spark utilities and configuration for {{PROJECT_NAME}}."""

import os
from typing import Dict, Optional

from pyspark.sql import SparkSession


def create_spark_session(
    app_name: str = "{{PROJECT_NAME}}",
    master: str = "local[*]",
    config: Optional[Dict[str, str]] = None,
) -> SparkSession:
    """Create and configure a Spark session.
    
    Args:
        app_name: Name of the Spark application
        master: Spark master URL
        config: Additional Spark configuration options
        
    Returns:
        Configured SparkSession
    """
    builder = SparkSession.builder.appName(app_name).master(master)
    
    # Default configuration
    default_config = {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true",
        "spark.sql.adaptive.localShuffleReader.enabled": "true",
        "spark.sql.adaptive.skewJoin.enabled": "true",
        "spark.sql.execution.arrow.pyspark.enabled": "true",
        "spark.sql.execution.arrow.maxRecordsPerBatch": "10000",
        "spark.sql.shuffle.partitions": "200",
        "spark.default.parallelism": "100",
        "spark.driver.memory": "2g",
        "spark.driver.maxResultSize": "1g",
        "spark.executor.memory": "2g",
        "spark.executor.cores": "2",
    }
    
    # Merge with user config
    if config:
        default_config.update(config)
    
    # Apply configuration
    for key, value in default_config.items():
        builder = builder.config(key, value)
    
    # Enable Hive support if available
    try:
        spark = builder.enableHiveSupport().getOrCreate()
    except Exception:
        spark = builder.getOrCreate()
    
    # Set log level
    spark.sparkContext.setLogLevel("WARN")
    
    return spark


def get_local_spark_session(
    app_name: str = "{{PROJECT_NAME}}_local",
    cores: str = "*",
) -> SparkSession:
    """Get a local Spark session for development.
    
    Args:
        app_name: Name of the Spark application
        cores: Number of cores to use (* for all available)
        
    Returns:
        Local SparkSession
    """
    config = {
        "spark.driver.memory": "4g",
        "spark.driver.maxResultSize": "2g",
        "spark.sql.shuffle.partitions": str(os.cpu_count() or 4),
    }
    
    return create_spark_session(
        app_name=app_name,
        master=f"local[{cores}]",
        config=config,
    )


def stop_spark_session(spark: SparkSession) -> None:
    """Stop a Spark session.
    
    Args:
        spark: SparkSession to stop
    """
    spark.stop()


class SparkSessionManager:
    """Context manager for Spark sessions."""
    
    def __init__(
        self,
        app_name: str = "{{PROJECT_NAME}}",
        master: str = "local[*]",
        config: Optional[Dict[str, str]] = None,
    ):
        """Initialize the Spark session manager.
        
        Args:
            app_name: Name of the Spark application
            master: Spark master URL
            config: Additional Spark configuration options
        """
        self.app_name = app_name
        self.master = master
        self.config = config
        self.spark: Optional[SparkSession] = None
    
    def __enter__(self) -> SparkSession:
        """Enter the context and create Spark session."""
        self.spark = create_spark_session(
            app_name=self.app_name,
            master=self.master,
            config=self.config,
        )
        return self.spark
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context and stop Spark session."""
        if self.spark:
            stop_spark_session(self.spark)