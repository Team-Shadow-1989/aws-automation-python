"""
File: create_security_group.py
Description:
    Creates a new Security Group inside a specified VPC.

Usage:
    python create_security_group.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def create_security_group():
    """Ask the user for group details and create a new Security Group."""

    print("=== Create Security Group ===")
    group_name = input("Enter Security Group name: ").strip()
    description = input("Enter a description: ").strip()
    vpc_id = input("Enter VPC ID: ").strip()

    try:
        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description=description,
            VpcId=vpc_id,
        )

        group_id = response["GroupId"]

        print("\nSuccess! Security Group created.")
        print(f"Group ID   : {group_id}")
        print(f"Group Name : {group_name}")
        print(f"VPC ID     : {vpc_id}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidVpcID.NotFound":
            print("Error: No VPC found with that VPC ID.")
        elif error_code == "InvalidGroup.Duplicate":
            print("Error: A security group with that name already exists in this VPC.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_security_group()
