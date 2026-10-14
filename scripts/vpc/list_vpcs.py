"""
File: list_vpcs.py
Description:
    Lists all VPCs in the configured AWS region.

Usage:
    python list_vpcs.py
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


def list_vpcs():
    """Fetch and display all VPCs in the account/region."""

    print("=== VPCs ===\n")

    try:
        response = ec2_client.describe_vpcs()

        vpcs = response.get("Vpcs", [])

        if not vpcs:
            print("No VPCs found in this region.")
            return

        for index, vpc in enumerate(vpcs, start=1):
            print(f"VPC {index}")
            print(f"  VPC ID       : {vpc.get('VpcId', 'N/A')}")
            print(f"  Name         : {get_name_tag(vpc.get('Tags'))}")
            print(f"  CIDR Block   : {vpc.get('CidrBlock', 'N/A')}")
            print(f"  State        : {vpc.get('State', 'N/A')}")
            print(f"  Is Default   : {vpc.get('IsDefault', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal VPCs found: {len(vpcs)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_vpcs()
