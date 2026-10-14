"""
File: list_subnets.py
Description:
    Lists all subnets in the configured AWS region.

Usage:
    python list_subnets.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def get_name_tag(tags):
    """Return the value of the 'Name' tag, or 'N/A' if it does not exist."""
    if not tags:
        return "N/A"
    for tag in tags:
        if tag["Key"] == "Name":
            return tag["Value"]
    return "N/A"


def list_subnets():
    """Fetch and display all subnets in the account/region."""

    print("=== Subnets ===\n")

    try:
        response = ec2_client.describe_subnets()

        subnets = response.get("Subnets", [])

        if not subnets:
            print("No subnets found in this region.")
            return

        for index, subnet in enumerate(subnets, start=1):
            print(f"Subnet {index}")
            print(f"  Subnet ID    : {subnet.get('SubnetId', 'N/A')}")
            print(f"  Name         : {get_name_tag(subnet.get('Tags'))}")
            print(f"  VPC ID       : {subnet.get('VpcId', 'N/A')}")
            print(f"  CIDR Block   : {subnet.get('CidrBlock', 'N/A')}")
            print(f"  State        : {subnet.get('State', 'N/A')}")
            print(f"  Availability Zone: {subnet.get('AvailabilityZone', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal subnets found: {len(subnets)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_subnets()
