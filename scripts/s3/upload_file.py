"""
File: upload_file.py
Description:
    Uploads a local file to a specified S3 bucket.

Usage:
    python upload_file.py
"""

import os
import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import s3_client
from botocore.exceptions import ClientError


def upload_file():
    """Ask the user for a local file path and bucket name, then upload it."""

    print("=== Upload File to S3 ===")
    file_path = input("Enter the path of the file to upload: ").strip()
    bucket_name = input("Enter the destination bucket name: ").strip()
    object_name = input(
        "Enter the object name in S3 (leave blank to use the file name): "
    ).strip()

    if not object_name:
        object_name = os.path.basename(file_path)

    try:
        if not os.path.isfile(file_path):
            print("Error: The file path you entered does not exist.")
            return

        s3_client.upload_file(file_path, bucket_name, object_name)

        print("\nSuccess! File uploaded.")
        print(f"Local File : {file_path}")
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
    except FileNotFoundError:
        print("Error: The file was not found on your local machine.")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    upload_file()
