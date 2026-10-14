"""
File: delete_key_pair.py
Description:
    Deletes an EC2 key pair based on a key name entered by the user.
    This does not delete the local .pem file, only the key pair in AWS.

Usage:
    python delete_key_pair.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def delete_key_pair():
    """Ask the user for a key pair name and delete it from AWS."""

    print("=== Delete EC2 Key Pair ===")
    key_name = input("Enter the key pair name to delete: ").strip()

    try:
        ec2_client.delete_key_pair(KeyName=key_name)

        print("\nSuccess! Key pair deleted.")
        print(f"Key Name: {key_name}")
        print("Note: Any local .pem file was not deleted automatically.")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidKeyPair.NotFound":
            print("Error: No key pair found with that name.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_key_pair()
