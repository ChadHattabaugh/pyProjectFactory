#!/usr/bin/env python3
"""Script to set up Spark environment and validate installation."""

import sys
from pathlib import Path

from {{PROJECT_NAME}}.spark_utils import get_local_spark_session


def check_java_installation() -> bool:
    """Check if Java is installed."""
    import subprocess
    
    try:
        result = subprocess.run(
            ["java", "-version"],
            capture_output=True,
            text=True,
            check=True
        )
        print("Java installation found:")
        print(result.stderr.split('\n')[0])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Java not found. Please install Java 8 or higher.")
        return False


def test_spark_session() -> bool:
    """Test Spark session creation."""
    try:
        print("Creating Spark session...")
        spark = get_local_spark_session("spark_test")
        
        # Create test DataFrame
        data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
        columns = ["name", "age"]
        
        df = spark.createDataFrame(data, columns)
        count = df.count()
        
        print(f"✅ Spark session created successfully!")
        print(f"✅ Test DataFrame created with {count} rows")
        print(f"✅ Spark UI available at: http://localhost:4040")
        
        spark.stop()
        return True
        
    except Exception as e:
        print(f"❌ Spark session creation failed: {e}")
        return False


def main() -> None:
    """Main setup function."""
    print("Setting up Spark environment...\n")
    
    # Check Java
    if not check_java_installation():
        sys.exit(1)
    
    print()
    
    # Test Spark
    if not test_spark_session():
        sys.exit(1)
    
    print("\n✅ Spark environment setup complete!")
    print("\nNext steps:")
    print("1. Start Jupyter Lab: nox -s jupyter")
    print("2. Open notebooks/02_spark_example.ipynb")
    print("3. Run the example Spark code")


if __name__ == "__main__":
    main()