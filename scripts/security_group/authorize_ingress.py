"""
File: authorize_ingress.py
Description:
    Adds an inbound (ingress) rule to a Security Group, allowing traffic
    on a specified port from a specified IP range.

Usage:
    python authorize_ingress.py
"""

import sys
import os

# Allow this script to find config.py in the project root, even when
# run directly from inside its subfolder (e.g. scripts/ec2/).
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from config import ec2_client
from botocore.exceptions import ClientError


def authorize_ingress():
    """Ask the user for rule details and add an ingress rule."""

    print("=== Authorize Security Group Ingress Rule ===")
    group_id = input("Enter Security Group ID: ").strip()
    protocol = input("Enter protocol (tcp, udp, icmp) [tcp]: ").strip() or "tcp"
    port_input = input("Enter port number (e.g. 22 for SSH, 80 for HTTP): ").strip()
    cidr_ip = input("Enter CIDR IP range (e.g. 0.0.0.0/0): ").strip()

    try:
        port = int(port_input)

        ec2_client.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=[
                {
                    "IpProtocol": protocol,
                    "FromPort": port,
                    "ToPort": port,
                    "IpRanges": [{"CidrIp": cidr_ip}],
                }
            ],
        )

        print("\nSuccess! Ingress rule added.")
        print(f"Group ID : {group_id}")
        print(f"Protocol : {protocol}")
        print(f"Port     : {port}")
        print(f"CIDR IP  : {cidr_ip}")

    except ValueError:
        print("Error: Port number must be a whole number.")
    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code == "InvalidGroup.NotFound":
            print("Error: No security group found with that Group ID.")
        elif error_code == "InvalidPermission.Duplicate":
            print("Error: This rule already exists on the security group.")
        elif error_code == "UnauthorizedOperation":
            print("Error: Access denied. Check your IAM permissions.")
        else:
            print(f"Error: {error.response['Error']['Message']}")
    except Exception as error:
        print(f"An unexpected error occurred: {error}")


if __name__ == "__main__":
    authorize_ingress()
