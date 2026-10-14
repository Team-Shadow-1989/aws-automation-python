# IAM Setup Guide

This guide explains how to create a dedicated IAM user for this project with the correct permissions.

## Why Use a Dedicated IAM User?

You should never use your AWS root account credentials for day-to-day work or automation. Instead, create a separate IAM user with only the permissions this project needs. This limits the damage if credentials are ever leaked.

## 1. Create an IAM User

1. Sign in to the AWS Management Console as an administrator.
2. Open the **IAM** service.
3. Click **Users** in the left sidebar, then **Create user**.
4. Enter a username, for example `aws-automation-project`.
5. Select **Provide user access to the AWS Management Console** only if you also want console login (optional for this project — you mainly need programmatic access).
6. Click **Next**.

## 2. Attach Permissions

For learning and portfolio purposes, you can attach these AWS managed policies directly:

- `AmazonEC2FullAccess`
- `AmazonS3FullAccess`
- `IAMFullAccess`
- `CloudWatchFullAccess`

Alternatively, for a more production-realistic setup, create a **custom policy** that only allows the specific actions used by the scripts in this project (e.g. `ec2:RunInstances`, `ec2:DescribeInstances`, `s3:CreateBucket`, `cloudwatch:PutMetricAlarm`, etc.).

> **Note:** `IAMFullAccess` is a broad permission. In a real production environment, scope this down to only the IAM actions this project needs (`iam:CreateUser`, `iam:ListUsers`, `iam:DeleteUser`, `iam:ListRoles`, `iam:CreateAccessKey`, `iam:DeleteAccessKey`).

## 3. Create Access Keys

1. After creating the user, open the user's detail page.
2. Go to the **Security credentials** tab.
3. Click **Create access key**.
4. Choose **Command Line Interface (CLI)**.
5. Acknowledge the recommendation and click **Create access key**.
6. Copy the **Access Key ID** and **Secret Access Key**, or download the `.csv` file.

## 4. Configure the Credentials Locally

Follow `aws_cli_setup.md` to run `aws configure` with these credentials.

## 5. Minimum Permissions Reference

| Service      | Example Actions Needed                                                   |
|--------------|----------------------------------------------------------------------------|
| EC2          | RunInstances, DescribeInstances, StartInstances, StopInstances, RebootInstances, TerminateInstances, CreateKeyPair, DescribeKeyPairs, DeleteKeyPair |
| S3           | CreateBucket, ListBuckets, PutObject, GetObject, ListObjects, DeleteObject, DeleteBucket |
| EBS (EC2)    | CreateVolume, DescribeVolumes, AttachVolume, DetachVolume, DeleteVolume, CreateSnapshot, DescribeSnapshots, DeleteSnapshot |
| VPC (EC2)    | CreateVpc, DescribeVpcs, CreateSubnet, DescribeSubnets, DeleteSubnet, DeleteVpc |
| Security Groups (EC2) | CreateSecurityGroup, DescribeSecurityGroups, AuthorizeSecurityGroupIngress, RevokeSecurityGroupIngress, DeleteSecurityGroup |
| IAM          | CreateUser, ListUsers, DeleteUser, ListRoles, CreateAccessKey, DeleteAccessKey |
| CloudWatch   | ListMetrics, DescribeAlarms, PutMetricAlarm, DeleteAlarms                 |

## Security Reminders

- Delete IAM users and access keys you no longer need using `scripts/iam/delete_user.py` and `scripts/iam/delete_access_key.py`.
- Never hard-code access keys inside any script. This project always reads credentials from your AWS CLI configuration.
- Enable MFA on your AWS root account and any console-enabled IAM users.
