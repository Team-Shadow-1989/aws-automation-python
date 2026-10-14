"""
File: create_subnet.py
Description:
    Creates a new subnet inside a specified VPC.

Usage:
    python create_subnet.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def create_subnet():
    """Ask the user for VPC and subnet details, then create the subnet."""

    print("=== Create Subnet ===")
    vpc_id = input("Enter VPC ID: ").strip()
    cidr_block = input("Enter Subnet CIDR block (e.g. 10.0.1.0/24): ").strip()
    availability_zone = input(
        "Enter Availability Zone (leave blank to let AWS choose): "
    ).strip()

    try:
        params = {"VpcId": vpc_id, "CidrBlock": cidr_block}

        if availability_zone:
            params["AvailabilityZone"] = availability_zone

        response = ec2_client.create_subnet(**params)

        subnet_id = response["Subnet"]["SubnetId"]

        print("\nSuccess! Subnet created.")
        print(f"Subnet ID  : {subnet_id}")
        print(f"VPC ID     : {vpc_id}")
        print(f"CIDR Block : {cidr_block}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidVpcID.NotFound":
            print("Error: No VPC found with that VPC ID.")
        elif error_code == "InvalidSubnet.Range":
            print("Error: The CIDR block is not valid for this VPC.")
        elif error_code == "InvalidSubnet.Conflict":
            print("Error: The CIDR block overlaps with an existing subnet.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_subnet()
