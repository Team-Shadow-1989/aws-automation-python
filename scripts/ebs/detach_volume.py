"""
File: detach_volume.py
Description:
    Detaches an EBS volume from its currently attached EC2 instance.

Usage:
    python detach_volume.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def detach_volume():
    """Ask the user for a volume ID and detach it from its instance."""

    print("=== Detach EBS Volume ===")
    volume_id = input("Enter Volume ID to detach: ").strip()

    try:
        response = ec2_client.detach_volume(VolumeId=volume_id)

        print("\nSuccess! Volume detachment requested.")
        print(f"Volume ID  : {volume_id}")
        print(f"State      : {response.get('State', 'N/A')}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidVolume.NotFound":
            print("Error: No volume found with that Volume ID.")
        elif error_code == "IncorrectState":
            print("Error: The volume is not currently attached to an instance.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    detach_volume()
