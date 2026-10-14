"""
File: start_instance.py
Description:
    Starts a stopped EC2 instance based on an Instance ID entered by the user.

Usage:
    python start_instance.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def start_instance():
    """Ask the user for an instance ID and start that instance."""

    print("=== Start EC2 Instance ===")
    instance_id = input("Enter Instance ID to start: ").strip()

    try:
        response = ec2_client.start_instances(InstanceIds=[instance_id])

        current_state = response["StartingInstances"][0]["CurrentState"]["Name"]

        print("\nSuccess! Start request sent.")
        print(f"Instance ID: {instance_id}")
        print(f"Current State: {current_state}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidInstanceID.NotFound":
            print("Error: No instance found with that Instance ID.")
        elif error_code == "InvalidInstanceID.Malformed":
            print("Error: The Instance ID format is invalid.")
        elif error_code == "IncorrectInstanceState":
            print("Error: The instance is not in a state that allows starting.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    start_instance()
