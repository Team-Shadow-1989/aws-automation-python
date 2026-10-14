"""
File: delete_user.py
Description:
    Deletes an IAM user based on a username entered by the user.
    Note: AWS requires that a user have no access keys, policies,
    or other resources attached before it can be deleted.

Usage:
    python delete_user.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import iam_client
from botocore.exceptions import ClientError


def delete_user():
    """Ask the user for a username and delete that IAM user."""

    print("=== Delete IAM User ===")
    username = input("Enter the IAM username to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{username}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        iam_client.delete_user(UserName=username)

        print("\nSuccess! IAM user deleted.")
        print(f"Username: {username}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "NoSuchEntity":
            print("Error: No IAM user found with that username.")
        elif error_code == "DeleteConflict":
            print("Error: This user still has access keys, policies, or groups attached. Remove them first.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_user()
