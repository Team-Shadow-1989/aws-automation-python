"""
File: list_metrics.py
Description:
    Lists available CloudWatch metrics, optionally filtered by namespace.

Usage:
    python list_metrics.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import cloudwatch_client
from botocore.exceptions import ClientError


def list_metrics():
    """Ask the user for a namespace filter and list matching metrics."""

    print("=== CloudWatch Metrics ===")
    namespace = input(
        "Enter a namespace to filter (e.g. AWS/EC2), or leave blank for all: "
    ).strip()

    try:
        params = {}
        if namespace:
            params["Namespace"] = namespace

        response = cloudwatch_client.list_metrics(**params)

        metrics = response.get("Metrics", [])

        if not metrics:
            print("\nNo metrics found.")
            return

        print()
        for index, metric in enumerate(metrics, start=1):
            print(f"Metric {index}")
            print(f"  Namespace  : {metric.get('Namespace', 'N/A')}")
            print(f"  Metric Name: {metric.get('MetricName', 'N/A')}")

            dimensions = metric.get("Dimensions", [])
            if dimensions:
                dim_text = ", ".join(
                    f"{d['Name']}={d['Value']}" for d in dimensions
                )
                print(f"  Dimensions : {dim_text}")

            print("-" * 40)

        print(f"\nTotal metrics found: {len(metrics)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_metrics()
