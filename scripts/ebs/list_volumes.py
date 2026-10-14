"""
File: list_volumes.py
Description:
    Lists all EBS volumes in the configured AWS region.

Usage:
    python list_volumes.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def list_volumes():
    """Fetch and display all EBS volumes in the account/region."""

    print("=== EBS Volumes ===\n")

    try:
        response = ec2_client.describe_volumes()

        volumes = response.get("Volumes", [])

        if not volumes:
            print("No EBS volumes found in this region.")
            return

        for index, volume in enumerate(volumes, start=1):
            print(f"Volume {index}")
            print(f"  Volume ID  : {volume.get('VolumeId', 'N/A')}")
            print(f"  State      : {volume.get('State', 'N/A')}")
            print(f"  Size (GiB) : {volume.get('Size', 'N/A')}")
            print(f"  Volume Type: {volume.get('VolumeType', 'N/A')}")
            print(f"  AZ         : {volume.get('AvailabilityZone', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal volumes found: {len(volumes)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_volumes()
