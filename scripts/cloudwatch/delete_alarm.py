"""
File: delete_alarm.py
Description:
    Deletes a CloudWatch alarm based on an alarm name entered by the user.

Usage:
    python delete_alarm.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import cloudwatch_client
from botocore.exceptions import ClientError


def delete_alarm():
    """Ask the user for an alarm name and delete that alarm."""

    print("=== Delete CloudWatch Alarm ===")
    alarm_name = input("Enter Alarm Name to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{alarm_name}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        cloudwatch_client.delete_alarms(AlarmNames=[alarm_name])

        print("\nSuccess! CloudWatch alarm deleted.")
        print(f"Alarm Name: {alarm_name}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "ResourceNotFound":
            print("Error: No alarm found with that name.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_alarm()
