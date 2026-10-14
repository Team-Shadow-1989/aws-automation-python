"""
File: terminate_instance.py
Description:
    Permanently terminates an EC2 instance based on an Instance ID
    entered by the user. This action cannot be undone.

Usage:
    python terminate_instance.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def terminate_instance():
    """Ask the user for an instance ID and terminate that instance."""

    print("=== Terminate EC2 Instance ===")
    print("WARNING: This action is permanent and cannot be undone.")
    instance_id = input("Enter Instance ID to terminate: ").strip()

    confirm = input(f"Type 'yes' to confirm termination of {instance_id}: ").strip()

    if confirm.lower() != "yes":
        print("Termination cancelled.")
        return

    try:
        response = ec2_client.terminate_instances(InstanceIds=[instance_id])

        current_state = response["TerminatingInstances"][0]["CurrentState"]["Name"]

        print("\nSuccess! Termination request sent.")
        print(f"Instance ID: {instance_id}")
        print(f"Current State: {current_state}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidInstanceID.NotFound":
            print("Error: No instance found with that Instance ID.")
        elif error_code == "InvalidInstanceID.Malformed":
            print("Error: The Instance ID format is invalid.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    terminate_instance()
