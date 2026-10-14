"""
File: config.py
Description:
    Central configuration file for the AWS Python Automation project.
    This file creates reusable Boto3 clients so every script can simply
    import the client it needs instead of creating its own connection.

    This is the ONLY shared file in the project. No script depends on
    any other script, but every script depends on this file.

Usage:
    from config import ec2_client, s3_client, iam_client, cloudwatch_client, REGION
"""

import boto3

# ---------------------------------------------------------------------------
# AWS Region
# ---------------------------------------------------------------------------
# Change this value to switch the region used by every script in the project.
REGION = "ap-south-1"

# ---------------------------------------------------------------------------
# Boto3 Clients
# ---------------------------------------------------------------------------
# These clients are created once here and imported wherever needed.
# Boto3 automatically uses the credentials configured through
# `aws configure` (see docs/aws_cli_setup.md).

ec2_client = boto3.client("ec2", region_name=REGION)
s3_client = boto3.client("s3", region_name=REGION)
iam_client = boto3.client("iam", region_name=REGION)
cloudwatch_client = boto3.client("cloudwatch", region_name=REGION)

# ---------------------------------------------------------------------------
# Boto3 Resources (used for a few S3 operations that are easier with
# the higher-level resource interface, e.g. checking if a bucket is empty)
# ---------------------------------------------------------------------------
s3_resource = boto3.resource("s3", region_name=REGION)
