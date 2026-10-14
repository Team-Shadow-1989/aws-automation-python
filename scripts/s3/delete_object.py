"""
File: delete_object.py
Description:
    Deletes a single object from a specified S3 bucket.

Usage:
    python delete_object.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import s3_client
from botocore.exceptions import ClientError


def delete_object():
    """Ask the user for a bucket and object name, then delete the object."""

    print("=== Delete Object from S3 Bucket ===")
    bucket_name = input("Enter the bucket name: ").strip()
    object_name = input("Enter the object name (key) to delete: ").strip()

    confirm = input(f"Type 'yes' to confirm deletion of '{object_name}': ").strip()

    if confirm.lower() != "yes":
        print("Deletion cancelled.")
        return

    try:
        s3_client.delete_object(Bucket=bucket_name, Key=object_name)

        print("\nSuccess! Object deleted.")
        print(f"Bucket     : {bucket_name}")
        print(f"Object Name: {object_name}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            print("Error: The bucket you specified does not exist.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_object()
