"""
File: delete_snapshot.py
Description:
    Deletes an EBS snapshot based on a Snapshot ID entered by the user.

Usage:
    python delete_snapshot.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def delete_snapshot():
    """Ask the user for a snapshot ID and delete that snapshot."""

    print("=== Delete EBS Snapshot ===")
    snapshot_id = input("Enter Snapshot ID to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{snapshot_id}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        ec2_client.delete_snapshot(SnapshotId=snapshot_id)

        print("\nSuccess! Snapshot deleted.")
        print(f"Snapshot ID: {snapshot_id}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidSnapshot.NotFound":
            print("Error: No snapshot found with that Snapshot ID.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_snapshot()
