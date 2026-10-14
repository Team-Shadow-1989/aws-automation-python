"""
File: list_buckets.py
Description:
    Lists all S3 buckets in the AWS account along with their creation date.

Usage:
    python list_buckets.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import s3_client
from botocore.exceptions import ClientError


def list_buckets():
    """Fetch and display all S3 buckets in the account."""

    print("=== S3 Buckets ===\n")

    try:
        response = s3_client.list_buckets()

        buckets = response.get("Buckets", [])

        if not buckets:
            print("No S3 buckets found in this account.")
            return

        for index, bucket in enumerate(buckets, start=1):
            print(f"Bucket {index}")
            print(f"  Bucket Name    : {bucket.get('Name', 'N/A')}")
            print(f"  Creation Date  : {bucket.get('CreationDate', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal buckets found: {len(buckets)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_buckets()
