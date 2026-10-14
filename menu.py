"""
File: menu.py
Description:
    An OPTIONAL interactive launcher for the AWS Python Automation project.

    This file contains NO AWS logic of its own. It simply runs the
    standalone scripts inside the scripts/ folder using the same Python
    interpreter that started this menu. Each script still works perfectly
    on its own with `python script_name.py` -- this menu is only a
    convenience so you don't have to remember every file path.

    You can safely delete this file. The project works without it.

Usage:
    python menu.py
"""

import os
import subprocess
import sys

# Base folder that contains this file (the project root)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")

# Menu structure: category -> list of (display name, script path)
MENU = {
    "EC2": [
        ("Launch Instance", "ec2/launch_instance.py"),
        ("List Instances", "ec2/list_instances.py"),
        ("Get Instance Status", "ec2/get_instance_status.py"),
        ("Start Instance", "ec2/start_instance.py"),
        ("Stop Instance", "ec2/stop_instance.py"),
        ("Reboot Instance", "ec2/reboot_instance.py"),
        ("Terminate Instance", "ec2/terminate_instance.py"),
        ("Create Key Pair", "ec2/create_key_pair.py"),
        ("List Key Pairs", "ec2/list_key_pairs.py"),
        ("Delete Key Pair", "ec2/delete_key_pair.py"),
    ],
    "S3": [
        ("Create Bucket", "s3/create_bucket.py"),
        ("List Buckets", "s3/list_buckets.py"),
        ("Upload File", "s3/upload_file.py"),
        ("Download File", "s3/download_file.py"),
        ("List Objects", "s3/list_objects.py"),
        ("Delete Object", "s3/delete_object.py"),
        ("Delete Bucket", "s3/delete_bucket.py"),
    ],
    "EBS": [
        ("Create Volume", "ebs/create_volume.py"),
        ("List Volumes", "ebs/list_volumes.py"),
        ("Attach Volume", "ebs/attach_volume.py"),
        ("Detach Volume", "ebs/detach_volume.py"),
        ("Delete Volume", "ebs/delete_volume.py"),
        ("Create Snapshot", "ebs/create_snapshot.py"),
        ("List Snapshots", "ebs/list_snapshots.py"),
        ("Delete Snapshot", "ebs/delete_snapshot.py"),
    ],
    "VPC": [
        ("Create VPC", "vpc/create_vpc.py"),
        ("List VPCs", "vpc/list_vpcs.py"),
        ("Create Subnet", "vpc/create_subnet.py"),
        ("List Subnets", "vpc/list_subnets.py"),
        ("Delete Subnet", "vpc/delete_subnet.py"),
        ("Delete VPC", "vpc/delete_vpc.py"),
    ],
    "Security Group": [
        ("Create Security Group", "security_group/create_security_group.py"),
        ("List Security Groups", "security_group/list_security_groups.py"),
        ("Authorize Ingress Rule", "security_group/authorize_ingress.py"),
        ("Revoke Ingress Rule", "security_group/revoke_ingress.py"),
        ("Delete Security Group", "security_group/delete_security_group.py"),
    ],
    "IAM": [
        ("Create User", "iam/create_user.py"),
        ("List Users", "iam/list_users.py"),
        ("Delete User", "iam/delete_user.py"),
        ("List Roles", "iam/list_roles.py"),
        ("Create Access Key", "iam/create_access_key.py"),
        ("Delete Access Key", "iam/delete_access_key.py"),
    ],
    "CloudWatch": [
        ("List Metrics", "cloudwatch/list_metrics.py"),
        ("List Alarms", "cloudwatch/list_alarms.py"),
        ("Create Alarm", "cloudwatch/create_alarm.py"),
        ("Delete Alarm", "cloudwatch/delete_alarm.py"),
    ],
}

CATEGORY_ORDER = ["EC2", "S3", "EBS", "VPC", "Security Group", "IAM", "CloudWatch"]


def show_main_menu():
    """Print the list of AWS service categories."""
    print("\n=== AWS Python Automation - Main Menu ===")
    for index, category in enumerate(CATEGORY_ORDER, start=1):
        print(f"{index}. {category}")
    print("0. Exit")


def show_category_menu(category):
    """Print the list of scripts available for a given category."""
    print(f"\n=== {category} ===")
    scripts = MENU[category]
    for index, (display_name, _) in enumerate(scripts, start=1):
        print(f"{index}. {display_name}")
    print("0. Back to Main Menu")


def run_script(relative_path):
    """Run a script from the scripts/ folder using its own Python process."""
    script_path = os.path.join(SCRIPTS_DIR, relative_path)
    print(f"\nRunning: {relative_path}\n" + ("-" * 40))
    subprocess.run([sys.executable, script_path])


def main():
    """Main loop: show categories, then show scripts, then run the chosen one."""
    while True:
        show_main_menu()
        choice = input("\nSelect a category number: ").strip()

        if choice == "0":
            print("Goodbye!")
            break

        if not choice.isdigit() or not (1 <= int(choice) <= len(CATEGORY_ORDER)):
            print("Invalid choice. Please try again.")
            continue

        category = CATEGORY_ORDER[int(choice) - 1]

        while True:
            show_category_menu(category)
            sub_choice = input("\nSelect a script number: ").strip()

            if sub_choice == "0":
                break

            scripts = MENU[category]
            if not sub_choice.isdigit() or not (1 <= int(sub_choice) <= len(scripts)):
                print("Invalid choice. Please try again.")
                continue

            _, relative_path = scripts[int(sub_choice) - 1]
            run_script(relative_path)


if __name__ == "__main__":
    main()
