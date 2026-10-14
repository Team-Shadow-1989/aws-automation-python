"""
File: attach_volume.py
Description:
    Attaches an EBS volume to an EC2 instance at a specified device name.

Usage:
    python attach_volume.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def attach_volume():
    """Ask the user for volume/instance details and attach the volume."""

    print("=== Attach EBS Volume ===")
    volume_id = input("Enter Volume ID: ").strip()
    instance_id = input("Enter Instance ID: ").strip()
    device_name = input("Enter device name (e.g. /dev/sdf): ").strip()

    try:
        response = ec2_client.attach_volume(
            VolumeId=volume_id,
            InstanceId=instance_id,
            Device=device_name,
        )

        print("\nSuccess! Volume attachment requested.")
        print(f"Volume ID  : {volume_id}")
        print(f"Instance ID: {instance_id}")
        print(f"Device     : {device_name}")
        print(f"State      : {response.get('State', 'N/A')}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidVolume.NotFound":
            print("Error: No volume found with that Volume ID.")
        elif error_code == "InvalidInstanceID.NotFound":
            print("Error: No instance found with that Instance ID.")
        elif error_code == "VolumeInUse":
            print("Error: The volume is already attached to an instance.")
        elif error_code == "IncorrectState":
            print("Error: The volume or instance is not in the correct state.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    attach_volume()
