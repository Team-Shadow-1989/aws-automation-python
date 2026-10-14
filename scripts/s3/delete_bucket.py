"""
File: delete_bucket.py
Description:
    Deletes an S3 bucket after checking that it is empty.
    S3 does not allow deleting a bucket that still contains objects,
    so this script checks first and warns the user if it is not empty.

Usage:
    python delete_bucket.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import s3_client
from botocore.exceptions import ClientError


def delete_bucket():
    """Ask the user for a bucket name, verify it is empty, then delete it."""

    print("=== Delete S3 Bucket ===")
    bucket_name = input("Enter the bucket name to delete: ").strip()

    try:
        # Check whether the bucket contains any objects first
        response = s3_client.list_objects_v2(Bucket=bucket_name, MaxKeys=1)

        if response.get("KeyCount", 0) > 0:
            print("Error: The bucket is not empty. Delete all objects first.")
            print("Tip: Use delete_object.py to remove objects, or list_objects.py to see what's inside.")
            return

        confirm = input(f"Type 'yes' to confirm deletion of bucket '{bucket_name}': ").strip()

        if confirm.lower() != "yes":
            print("Deletion cancelled.")
            return

        s3_client.delete_bucket(Bucket=bucket_name)

        print("\nSuccess! Bucket deleted.")
        print(f"Bucket Name: {bucket_name}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            print("Error: The bucket you specified does not exist.")
        elif error_code == "BucketNotEmpty":
            print("Error: The bucket is not empty. Delete all objects first.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    delete_bucket()
