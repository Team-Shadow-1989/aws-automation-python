"""
File: download_file.py
Description:
    Downloads a file from a specified S3 bucket to the local machine.

Usage:
    python download_file.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import s3_client
from botocore.exceptions import ClientError


def download_file():
    """Ask the user for a bucket and object name, then download the file."""

    print("=== Download File from S3 ===")
    bucket_name = input("Enter the bucket name: ").strip()
    object_name = input("Enter the object name (key) to download: ").strip()
    destination_path = input(
        "Enter the local path to save the file (leave blank to use the object name): "
    ).strip()

    if not destination_path:
        destination_path = object_name

    try:
        s3_client.download_file(bucket_name, object_name, destination_path)

        print("\nSuccess! File downloaded.")
        print(f"Bucket      : {bucket_name}")
        print(f"Object Name : {object_name}")
        print(f"Saved To    : {destination_path}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "404" or error_code == "NoSuchKey":
            print("Error: The object was not found in the bucket.")
        elif error_code == "NoSuchBucket":
            print("Error: The bucket you specified does not exist.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    download_file()
