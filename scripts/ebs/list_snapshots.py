"""
File: list_snapshots.py
Description:
    Lists all EBS snapshots owned by the current AWS account.

Usage:
    python list_snapshots.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def list_snapshots():
    """Fetch and display all EBS snapshots owned by this account."""

    print("=== EBS Snapshots ===\n")

    try:
        response = ec2_client.describe_snapshots(OwnerIds=["self"])

        snapshots = response.get("Snapshots", [])

        if not snapshots:
            print("No snapshots found for this account.")
            return

        for index, snapshot in enumerate(snapshots, start=1):
            print(f"Snapshot {index}")
            print(f"  Snapshot ID : {snapshot.get('SnapshotId', 'N/A')}")
            print(f"  Volume ID   : {snapshot.get('VolumeId', 'N/A')}")
            print(f"  State       : {snapshot.get('State', 'N/A')}")
            print(f"  Size (GiB)  : {snapshot.get('VolumeSize', 'N/A')}")
            print(f"  Start Time  : {snapshot.get('StartTime', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal snapshots found: {len(snapshots)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_snapshots()
