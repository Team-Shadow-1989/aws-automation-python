"""
File: create_vpc.py
Description:
    Creates a new VPC with a CIDR block entered by the user.

Usage:
    python create_vpc.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def create_vpc():
    """Ask the user for a CIDR block and create a new VPC."""

    print("=== Create VPC ===")
    cidr_block = input("Enter CIDR block (e.g. 10.0.0.0/16): ").strip()
    name_tag = input("Enter a Name tag for the VPC: ").strip()

    try:
        response = ec2_client.create_vpc(CidrBlock=cidr_block)

        vpc_id = response["Vpc"]["VpcId"]

        # Add a Name tag to make the VPC easier to identify later
        if name_tag:
            ec2_client.create_tags(
                Resources=[vpc_id],
                Tags=[{"Key": "Name", "Value": name_tag}],
            )

        print("\nSuccess! VPC created.")
        print(f"VPC ID     : {vpc_id}")
        print(f"CIDR Block : {cidr_block}")
        print(f"Name       : {name_tag if name_tag else 'N/A'}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidParameterValue":
            print("Error: The CIDR block format is invalid.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_vpc()
