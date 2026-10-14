"""
File: create_user.py
Description:
    Creates a new IAM user based on a username entered by the user.

Usage:
    python create_user.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import iam_client
from botocore.exceptions import ClientError


def create_user():
    """Ask the user for a username and create a new IAM user."""

    print("=== Create IAM User ===")
    username = input("Enter the new IAM username: ").strip()

    try:
        response = iam_client.create_user(UserName=username)

        user = response["User"]

        print("\nSuccess! IAM user created.")
        print(f"Username      : {user.get('UserName', 'N/A')}")
        print(f"ARN           : {user.get('Arn', 'N/A')}")
        print(f"Creation Date : {user.get('CreateDate', 'N/A')}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "EntityAlreadyExists":
            print("Error: An IAM user with that username already exists.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_user()
