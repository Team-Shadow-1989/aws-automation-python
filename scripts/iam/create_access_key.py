"""
File: create_access_key.py
Description:
    Creates a new access key (Access Key ID and Secret Access Key)
    for a specified IAM user. The secret key is shown only once,
    so it must be saved immediately.

Usage:
    python create_access_key.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import iam_client
from botocore.exceptions import ClientError


def create_access_key():
    """Ask the user for a username and create a new access key for them."""

    print("=== Create IAM Access Key ===")
    username = input("Enter the IAM username: ").strip()

    try:
        response = iam_client.create_access_key(UserName=username)

        key = response["AccessKey"]

        print("\nSuccess! Access key created.")
        print(f"Username         : {key.get('UserName', 'N/A')}")
        print(f"Access Key ID    : {key.get('AccessKeyId', 'N/A')}")
        print(f"Secret Access Key: {key.get('SecretAccessKey', 'N/A')}")
        print("\nIMPORTANT: Save the secret key now. AWS will not show it again.")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "NoSuchEntity":
            print("Error: No IAM user found with that username.")
        elif error_code == "LimitExceeded":
            print("Error: This user already has the maximum number of access keys (2).")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_access_key()
