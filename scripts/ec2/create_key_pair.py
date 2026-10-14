"""
File: create_key_pair.py
Description:
    Creates a new EC2 key pair and saves the private key (.pem file)
    to the local machine so it can be used to SSH into instances.

Usage:
    python create_key_pair.py
"""

import os
import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def create_key_pair():
    """Ask the user for a key pair name, create it, and save the .pem file."""

    print("=== Create EC2 Key Pair ===")
    key_name = input("Enter a name for the new key pair: ").strip()

    try:
        response = ec2_client.create_key_pair(KeyName=key_name)

        private_key = response["KeyMaterial"]
        file_name = f"{key_name}.pem"

        # Save the private key to a local file
        with open(file_name, "w") as key_file:
            key_file.write(private_key)

        # Restrict file permissions so SSH will accept the key (Linux/Mac)
        try:
            os.chmod(file_name, 0o400)
        except OSError:
            pass  # chmod may not work on all operating systems (e.g. Windows)

        print("\nSuccess! Key pair created.")
        print(f"Key Name: {key_name}")
        print(f"Private key saved as: {file_name}")
        print("Keep this file safe. AWS does not store a copy of it.")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidKeyPair.Duplicate":
            print("Error: A key pair with that name already exists.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    create_key_pair()
