# Cleanup Guide

AWS resources can incur charges if left running. Follow this guide after testing this project to make sure you don't get an unexpected bill.

## Recommended Cleanup Order

AWS resources often depend on each other, so deleting them in the wrong order will cause errors. Follow this order:

### 1. Terminate EC2 Instances

```bash
python scripts/ec2/list_instances.py
python scripts/ec2/terminate_instance.py
```

Wait for instances to reach the `terminated` state before continuing.

### 2. Delete EBS Volumes and Snapshots

Volumes attached to a terminated instance are sometimes deleted automatically (if "Delete on Termination" was enabled), but always double check:

```bash
python scripts/ebs/list_volumes.py
python scripts/ebs/detach_volume.py    # only if still attached
python scripts/ebs/delete_volume.py

python scripts/ebs/list_snapshots.py
python scripts/ebs/delete_snapshot.py
```

### 3. Delete Key Pairs (Optional)

```bash
python scripts/ec2/list_key_pairs.py
python scripts/ec2/delete_key_pair.py
```

Key pairs are free, so this step is optional, but it keeps your account tidy.

### 4. Empty and Delete S3 Buckets

S3 buckets must be empty before they can be deleted.

```bash
python scripts/s3/list_objects.py
python scripts/s3/delete_object.py     # repeat for every object
python scripts/s3/delete_bucket.py
```

### 5. Delete Security Groups

Security groups cannot be deleted while still attached to a running resource.

```bash
python scripts/security_group/list_security_groups.py
python scripts/security_group/revoke_ingress.py   # optional cleanup of rules
python scripts/security_group/delete_security_group.py
```

Note: the default security group of a VPC cannot be deleted; it is removed automatically when its VPC is deleted.

### 6. Delete Subnets

```bash
python scripts/vpc/list_subnets.py
python scripts/vpc/delete_subnet.py
```

### 7. Delete VPCs

```bash
python scripts/vpc/list_vpcs.py
python scripts/vpc/delete_vpc.py
```

Do not delete your account's default VPC unless you are certain you want to.

### 8. Delete CloudWatch Alarms

```bash
python scripts/cloudwatch/list_alarms.py
python scripts/cloudwatch/delete_alarm.py
```

CloudWatch alarms are inexpensive but unused alarms add clutter.

### 9. Clean Up IAM Resources

Only clean these up if you created test IAM users specifically for this project — do not delete your main automation user.

```bash
python scripts/iam/list_users.py
python scripts/iam/delete_access_key.py   # delete all access keys for the user first
python scripts/iam/delete_user.py
```

## Quick Verification Checklist

- [ ] No running or stopped EC2 instances you don't need
- [ ] No unused EBS volumes or snapshots
- [ ] No S3 buckets with unwanted data
- [ ] No unused security groups
- [ ] No unused subnets or VPCs
- [ ] No unused CloudWatch alarms
- [ ] No unused IAM test users or access keys

## Double-Check with the AWS Console

Scripts are a great way to automate cleanup, but it's good practice to also check the AWS Management Console billing dashboard and the **AWS Cost Explorer** to confirm no unexpected resources remain.
