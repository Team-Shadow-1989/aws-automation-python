"""
File: list_key_pairs.py
Description:
    Lists all EC2 key pairs available in the configured AWS region.

Usage:
    python list_key_pairs.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def list_key_pairs():
    """Fetch and display all EC2 key pairs in the account/region."""

    print("=== EC2 Key Pairs ===\n")

    try:
        response = ec2_client.describe_key_pairs()

        key_pairs = response.get("KeyPairs", [])

        if not key_pairs:
            print("No key pairs found in this region.")
            return

        for index, key_pair in enumerate(key_pairs, start=1):
            print(f"Key Pair {index}")
            print(f"  Key Name       : {key_pair.get('KeyName', 'N/A')}")
            print(f"  Key Pair ID    : {key_pair.get('KeyPairId', 'N/A')}")
            print(f"  Key Type       : {key_pair.get('KeyType', 'N/A')}")
            print(f"  Fingerprint    : {key_pair.get('KeyFingerprint', 'N/A')}")
            print("-" * 40)

        print(f"\nTotal key pairs found: {len(key_pairs)}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_key_pairs()
