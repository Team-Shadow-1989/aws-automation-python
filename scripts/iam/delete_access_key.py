"""
File: delete_access_key.py
Description:
    Deletes an access key belonging to a specified IAM user.

Usage:
    python delete_access_key.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import iam_client
from botocore.exceptions import ClientError


def delete_access_key():
    """Ask the user for a username and access key ID, then delete it."""

    print("=== Delete IAM Access Key ===")
    username = input("Enter the IAM username: ").strip()
    access_key_id = input("Enter the Access Key ID to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{access_key_id}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        iam_client.delete_access_key(UserName=username, AccessKeyId=access_key_id)

        print("\nSuccess! Access key deleted.")
        print(f"Username     : {username}")
        print(f"Access Key ID: {access_key_id}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "NoSuchEntity":
            print("Error: No matching IAM user or access key was found.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_access_key()
