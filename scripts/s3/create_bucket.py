"""
File: create_bucket.py
Description:
    Creates a new S3 bucket with a name entered by the user.

Usage:
    python create_bucket.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import s3_client, REGION
from botocore.exceptions import ClientError


def create_bucket():
    """Ask the user for a bucket name and create a new S3 bucket."""

    print("=== Create S3 Bucket ===")
    bucket_name = input("Enter a globally unique bucket name: ").strip()

    try:
        # S3 requires a special format when the region is not us-east-1
        if REGION == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": REGION},
            )

        print("\nSuccess! Bucket created.")
        print(f"Bucket Name: {bucket_name}")
        print(f"Region: {REGION}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "BucketAlreadyExists":
            print("Error: That bucket name is already taken globally. Try another.")
        elif error_code == "BucketAlreadyOwnedByYou":
            print("Error: You already own a bucket with that name.")
        elif error_code == "InvalidBucketName":
            print("Error: The bucket name is invalid. Use lowercase letters, numbers, and hyphens.")
        elif error_code == "AccessDenied":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_bucket()
