"""
File: delete_vpc.py
Description:
    Deletes a VPC based on a VPC ID entered by the user.
    The VPC must not contain any dependent resources (subnets,
    instances, gateways, etc.) before it can be deleted.

Usage:
    python delete_vpc.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def delete_vpc():
    """Ask the user for a VPC ID and delete that VPC."""

    print("=== Delete VPC ===")
    vpc_id = input("Enter VPC ID to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{vpc_id}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        ec2_client.delete_vpc(VpcId=vpc_id)

        print("\nSuccess! VPC deleted.")
        print(f"VPC ID: {vpc_id}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidVpcID.NotFound":
            print("Error: No VPC found with that VPC ID.")
        elif error_code == "DependencyViolation":
            print("Error: The VPC has dependent resources (subnets, instances, etc.). Remove them first.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_vpc()
