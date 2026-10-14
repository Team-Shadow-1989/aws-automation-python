"""
File: delete_security_group.py
Description:
    Deletes a Security Group based on a Group ID entered by the user.

Usage:
    python delete_security_group.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def delete_security_group():
    """Ask the user for a group ID and delete that security group."""

    print("=== Delete Security Group ===")
    group_id = input("Enter Security Group ID to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{group_id}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        ec2_client.delete_security_group(GroupId=group_id)

        print("\nSuccess! Security Group deleted.")
        print(f"Group ID: {group_id}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidGroup.NotFound":
            print("Error: No security group found with that Group ID.")
        elif error_code == "DependencyViolation":
            print("Error: This security group is still in use by another resource.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_security_group()
