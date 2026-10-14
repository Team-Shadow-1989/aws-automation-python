"""
File: delete_subnet.py
Description:
    Deletes a subnet based on a Subnet ID entered by the user.

Usage:
    python delete_subnet.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def delete_subnet():
    """Ask the user for a subnet ID and delete that subnet."""

    print("=== Delete Subnet ===")
    subnet_id = input("Enter Subnet ID to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{subnet_id}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        ec2_client.delete_subnet(SubnetId=subnet_id)

        print("\nSuccess! Subnet deleted.")
        print(f"Subnet ID: {subnet_id}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidSubnetID.NotFound":
            print("Error: No subnet found with that Subnet ID.")
        elif error_code == "DependencyViolation":
            print("Error: The subnet has dependent resources (e.g. instances). Remove them first.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_subnet()
