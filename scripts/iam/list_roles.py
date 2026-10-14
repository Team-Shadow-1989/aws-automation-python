"""
File: list_roles.py
Description:
    Lists all IAM roles in the AWS account.

Usage:
    python list_roles.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import iam_client
from botocore.exceptions import ClientError


def list_roles():
    """Fetch and display all IAM roles in the account."""

    print("=== IAM Roles ===\n")

    try:
        response = iam_client.list_roles()

        roles = response.get("Roles", [])

        if not roles:
            print("No IAM roles found in this account.")
            return

        for index, role in enumerate(roles, start=1):
            print(f"Role {index}")
            print(f"  Role Name     : {role.get('RoleName', 'N/A')}")
            print(f"  ARN           : {role.get('Arn', 'N/A')}")
            print(f"  Creation Date : {role.get('CreateDate', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal roles found: {len(roles)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_roles()
