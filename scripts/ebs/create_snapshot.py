"""
File: create_snapshot.py
Description:
    Creates a point-in-time snapshot of an EBS volume.

Usage:
    python create_snapshot.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def create_snapshot():
    """Ask the user for a volume ID and create a snapshot of it."""

    print("=== Create EBS Snapshot ===")
    volume_id = input("Enter Volume ID to snapshot: ").strip()
    description = input("Enter a description for the snapshot: ").strip()

    try:
        response = ec2_client.create_snapshot(
            VolumeId=volume_id,
            Description=description,
        )

        snapshot_id = response["SnapshotId"]
        state = response["State"]

        print("\nSuccess! Snapshot creation started.")
        print(f"Snapshot ID: {snapshot_id}")
        print(f"Volume ID  : {volume_id}")
        print(f"State      : {state}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidVolume.NotFound":
            print("Error: No volume found with that Volume ID.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_snapshot()
