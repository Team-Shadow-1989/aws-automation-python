"""
File: create_volume.py
Description:
    Creates a new EBS volume in a specified Availability Zone.

Usage:
    python create_volume.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def create_volume():
    """Ask the user for volume details and create a new EBS volume."""

    print("=== Create EBS Volume ===")
    availability_zone = input("Enter Availability Zone (e.g. ap-south-1a): ").strip()
    size_input = input("Enter volume size in GiB (e.g. 8): ").strip()
    volume_type = input("Enter volume type (e.g. gp3, gp2, io1) [gp3]: ").strip() or "gp3"

    try:
        size_gib = int(size_input)

        response = ec2_client.create_volume(
            AvailabilityZone=availability_zone,
            Size=size_gib,
            VolumeType=volume_type,
        )

        volume_id = response["VolumeId"]
        state = response["State"]

        print("\nSuccess! EBS volume created.")
        print(f"Volume ID  : {volume_id}")
        print(f"Size       : {size_gib} GiB")
        print(f"State      : {state}")
        print(f"AZ         : {availability_zone}")

    except ValueError:
        print("Error: Volume size must be a whole number.")
    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidParameterValue":
            print("Error: One of the values entered is invalid.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_volume()
