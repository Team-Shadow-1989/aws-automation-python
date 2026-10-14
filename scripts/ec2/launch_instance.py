"""
File: launch_instance.py
Description:
    Launches a new EC2 instance using details provided by the user.
    This script only launches an instance. It does nothing else.

Usage:
    python launch_instance.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def launch_instance():
    """Ask the user for instance details and launch a new EC2 instance."""

    print("=== Launch a New EC2 Instance ===")

    # Get input from the user
    ami_id = input("Enter AMI ID (e.g. ami-0abcdef1234567890): ").strip()
    instance_type = input("Enter instance type (e.g. t2.micro): ").strip()
    key_name = input("Enter key pair name: ").strip()
    instance_name = input("Enter a Name tag for the instance: ").strip()

    security_group_id = input(
        "Enter Security Group ID (leave blank for default): "
    ).strip()
    subnet_id = input("Enter Subnet ID (leave blank for default): ").strip()

    try:
        # Build the parameters for the API call
        run_params = {
            "ImageId": ami_id,
            "InstanceType": instance_type,
            "KeyName": key_name,
            "MinCount": 1,
            "MaxCount": 1,
            "TagSpecifications": [
                {
                    "ResourceType": "instance",
                    "Tags": [{"Key": "Name", "Value": instance_name}],
                }
            ],
        }

        if security_group_id:
            run_params["SecurityGroupIds"] = [security_group_id]

        if subnet_id:
            run_params["SubnetId"] = subnet_id

        # Call the AWS API to launch the instance
        response = ec2_client.run_instances(**run_params)

        instance_id = response["Instances"][0]["InstanceId"]

        print("\nSuccess! EC2 instance launched.")
        print(f"Instance ID: {instance_id}")
        print(f"Instance Name: {instance_name}")
        print(f"Instance Type: {instance_type}")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        if error_code == "InvalidAMIID.NotFound":
            print("Error: The AMI ID you entered does not exist.")
        elif error_code == "InvalidKeyPair.NotFound":
            print("Error: The key pair name you entered does not exist.")
        elif error_code == "InvalidGroup.NotFound":
            print("Error: The security group ID you entered does not exist.")
        elif error_code == "InvalidSubnetID.NotFound":
            print("Error: The subnet ID you entered does not exist.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    launch_instance()
