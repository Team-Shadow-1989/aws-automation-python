"""
File: list_alarms.py
Description:
    Lists all CloudWatch alarms in the configured AWS region.

Usage:
    python list_alarms.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import cloudwatch_client
from botocore.exceptions import ClientError


def list_alarms():
    """Fetch and display all CloudWatch alarms in the account/region."""

    print("=== CloudWatch Alarms ===\n")

    try:
        response = cloudwatch_client.describe_alarms()

        alarms = response.get("MetricAlarms", [])

        if not alarms:
            print("No CloudWatch alarms found in this region.")
            return

        for index, alarm in enumerate(alarms, start=1):
            print(f"Alarm {index}")
            print(f"  Alarm Name : {alarm.get('AlarmName', 'N/A')}")
            print(f"  State      : {alarm.get('StateValue', 'N/A')}")
            print(f"  Metric Name: {alarm.get('MetricName', 'N/A')}")
            print(f"  Namespace  : {alarm.get('Namespace', 'N/A')}")
            print(f"  Threshold  : {alarm.get('Threshold', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal alarms found: {len(alarms)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_alarms()
