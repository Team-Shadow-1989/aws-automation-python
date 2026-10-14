"""
File: list_instances.py
Description:
    Lists all EC2 instances in the configured AWS region along with
    useful details such as instance ID, name, type, state, and IPs.

Usage:
    python list_instances.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def get_name_tag(tags):
    """Return the value of the 'Name' tag, or 'N/A' if it does not exist."""
    if not tags:
        return "N/A"
    for tag in tags:
        if tag["Key"] == "Name":
            return tag["Value"]
    return "N/A"


def list_instances():
    """Fetch and display all EC2 instances in the account/region."""

    print("=== EC2 Instances ===\n")

    try:
        response = ec2_client.describe_instances()

        reservations = response.get("Reservations", [])

        if not reservations:
            print("No EC2 instances found in this region.")
            return

        instance_count = 0

        for reservation in reservations:
            for instance in reservation["Instances"]:
                instance_count += 1

                instance_id = instance.get("InstanceId", "N/A")
                instance_type = instance.get("InstanceType", "N/A")
                state = instance.get("State", {}).get("Name", "N/A")
                public_ip = instance.get("PublicIpAddress", "N/A")
                private_ip = instance.get("PrivateIpAddress", "N/A")
                launch_time = instance.get("LaunchTime", "N/A")
                az = instance.get("Placement", {}).get(
                    "AvailabilityZone", "N/A"
                )
                name = get_name_tag(instance.get("Tags"))

                print(f"Instance {instance_count}")
                print(f"  Instance ID     : {instance_id}")
                print(f"  Name            : {name}")
                print(f"  Instance Type   : {instance_type}")
                print(f"  State           : {state}")
                print(f"  Public IP       : {public_ip}")
                print(f"  Private IP      : {private_ip}")
                print(f"  Availability Zone: {az}")
                print(f"  Launch Time     : {launch_time}")
                print("-" * 40)

        print(f"\nTotal instances found: {instance_count}")

    except ClientError as error:
        print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    list_instances()
