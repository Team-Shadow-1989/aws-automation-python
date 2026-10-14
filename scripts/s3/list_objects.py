"""
File: list_objects.py
Description:
    Lists all objects inside a specified S3 bucket along with their size.

Usage:
    python list_objects.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import s3_client
from botocore.exceptions import ClientError


def list_objects():
    """Ask the user for a bucket name and list all objects inside it."""

    print("=== List Objects in S3 Bucket ===")
    bucket_name = input("Enter the bucket name: ").strip()

    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        objects = response.get("Contents", [])

        if not objects:
            print("This bucket is empty or does not contain any objects.")
            return

        for index, obj in enumerate(objects, start=1):
            print(f"Object {index}")
            print(f"  Object Name : {obj.get('Key', 'N/A')}")
            print(f"  Size (bytes): {obj.get('Size', 'N/A')}")
            print(f"  Last Modified: {obj.get('LastModified', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal objects found: {len(objects)}")

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
    list_objects()
