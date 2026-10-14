"""
File: create_alarm.py
Description:
    Creates a new CloudWatch alarm that watches a metric and triggers
    when it crosses a threshold entered by the user.

Usage:
    python create_alarm.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import cloudwatch_client
from botocore.exceptions import ClientError


def create_alarm():
    """Ask the user for alarm details and create a new CloudWatch alarm."""

    print("=== Create CloudWatch Alarm ===")
    alarm_name = input("Enter Alarm Name: ").strip()
    namespace = input("Enter Namespace (e.g. AWS/EC2): ").strip()
    metric_name = input("Enter Metric Name (e.g. CPUUtilization): ").strip()
    instance_id = input("Enter Instance ID to monitor (leave blank if not applicable): ").strip()
    threshold_input = input("Enter threshold value (e.g. 80): ").strip()
    comparison = input(
        "Enter comparison operator (GreaterThanThreshold, LessThanThreshold) [GreaterThanThreshold]: "
    ).strip() or "GreaterThanThreshold"

    try:
        threshold = float(threshold_input)

        params = {
            "AlarmName": alarm_name,
            "MetricName": metric_name,
            "Namespace": namespace,
            "Statistic": "Average",
            "Period": 300,
            "EvaluationPeriods": 1,
            "Threshold": threshold,
            "ComparisonOperator": comparison,
        }

        if instance_id:
            params["Dimensions"] = [{"Name": "InstanceId", "Value": instance_id}]

        cloudwatch_client.put_metric_alarm(**params)

        print("\nSuccess! CloudWatch alarm created.")
        print(f"Alarm Name : {alarm_name}")
        print(f"Metric     : {namespace} / {metric_name}")
        print(f"Threshold  : {threshold}")
        print(f"Comparison : {comparison}")

    except ValueError:
        print("Error: Threshold must be a valid number.")
    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidParameterValue" or error_code == "InvalidParameterCombination":
            print("Error: One of the values entered is invalid.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_alarm()
