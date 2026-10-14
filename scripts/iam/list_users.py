"""
File: list_users.py
Description:
    Lists all IAM users in the AWS account.

Usage:
    python list_users.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import iam_client
from botocore.exceptions import ClientError


def list_users():
    """Fetch and display all IAM users in the account."""

    print("=== IAM Users ===\n")

    try:
        response = iam_client.list_users()

        users = response.get("Users", [])

        if not users:
            print("No IAM users found in this account.")
            return

        for index, user in enumerate(users, start=1):
            print(f"User {index}")
            print(f"  Username      : {user.get('UserName', 'N/A')}")
            print(f"  ARN           : {user.get('Arn', 'N/A')}")
            print(f"  Creation Date : {user.get('CreateDate', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal users found: {len(users)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_users()
