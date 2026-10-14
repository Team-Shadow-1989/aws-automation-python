"""
File: delete_volume.py
Description:
    Deletes an EBS volume. The volume must not be attached to any instance.

Usage:
    python delete_volume.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def delete_volume():
    """Ask the user for a volume ID and delete that volume."""

    print("=== Delete EBS Volume ===")
    volume_id = input("Enter Volume ID to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{volume_id}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        ec2_client.delete_volume(VolumeId=volume_id)

        print("\nSuccess! Volume deleted.")
        print(f"Volume ID: {volume_id}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidVolume.NotFound":
            print("Error: No volume found with that Volume ID.")
        elif error_code == "VolumeInUse":
            print("Error: The volume is still attached to an instance. Detach it first.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_volume()
