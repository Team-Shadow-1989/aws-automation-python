"""
File: list_security_groups.py
Description:
    Lists all Security Groups in the configured AWS region.

Usage:
    python list_security_groups.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def list_security_groups():
    """Fetch and display all Security Groups in the account/region."""

    print("=== Security Groups ===\n")

    try:
        response = ec2_client.describe_security_groups()

        groups = response.get("SecurityGroups", [])

        if not groups:
            print("No security groups found in this region.")
            return

        for index, group in enumerate(groups, start=1):
            print(f"Security Group {index}")
            print(f"  Group ID    : {group.get('GroupId', 'N/A')}")
            print(f"  Group Name  : {group.get('GroupName', 'N/A')}")
            print(f"  Description : {group.get('Description', 'N/A')}")
            print(f"  VPC ID      : {group.get('VpcId', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal security groups found: {len(groups)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_security_groups()
