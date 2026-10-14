"""
File: get_instance_status.py
Description:
    Retrieves and displays the status of a single EC2 instance
    based on an Instance ID entered by the user.

Usage:
    python get_instance_status.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def get_instance_status():
    """Ask the user for an instance ID and display its current status."""

    print("=== Get EC2 Instance Status ===")
    instance_id = input("Enter Instance ID: ").strip()

    try:
        response = ec2_client.describe_instance_status(
            InstanceIds=[instance_id], IncludeAllInstances=True
        )

        statuses = response.get("InstanceStatuses", [])

        if not statuses:
            print("No status information found for this instance.")
            return

        status_info = statuses[0]

        instance_state = status_info["InstanceState"]["Name"]
        system_status = status_info["SystemStatus"]["Status"]
        instance_status = status_info["InstanceStatus"]["Status"]
        availability_zone = status_info["AvailabilityZone"]

        print("\nSuccess! Instance status retrieved.")
        print(f"Instance ID       : {instance_id}")
        print(f"Instance State    : {instance_state}")
        print(f"System Status     : {system_status}")
        print(f"Instance Status   : {instance_status}")
        print(f"Availability Zone : {availability_zone}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidInstanceID.NotFound":
            print("Error: No instance found with that Instance ID.")
        elif error_code == "InvalidInstanceID.Malformed":
            print("Error: The Instance ID format is invalid.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    get_instance_status()
