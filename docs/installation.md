# Installation Guide

This guide walks you through setting up the AWS Python Automation project on your local machine.

## 1. Prerequisites

Before you begin, make sure you have:

- **Python 3.8 or higher** installed
- **pip** (Python package manager)
- An **AWS account**
- **AWS CLI** installed (see `aws_cli_setup.md`)
- An IAM user with programmatic access (see `iam_setup.md`)

Check your Python version:

```bash
python3 --version
```

## 2. Clone or Download the Project

```bash
git clone https://github.com/your-username/aws-python-automation.git
cd aws-python-automation
```

## 3. Create a Virtual Environment

A virtual environment keeps this project's dependencies separate from other Python projects on your machine.

**Linux / macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

You'll know it worked when you see `(venv)` at the start of your terminal prompt.

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs `boto3` and `botocore`, the AWS SDK for Python.

## 5. Configure AWS Credentials

See `aws_cli_setup.md` for full details. In short:

```bash
aws configure
```

You'll be asked for:

- AWS Access Key ID
- AWS Secret Access Key
- Default region name (this project defaults to `ap-south-1`)
- Default output format (`json` is recommended)

## 6. Set the Region (Optional)

Open `config.py` in the project root and change the `REGION` variable if you want to use a region other than `ap-south-1`.

```python
REGION = "ap-south-1"
```

## 7. Run a Script

Every script can be run on its own. For example, to list your EC2 instances:

```bash
python scripts/ec2/list_instances.py
```

Or use the optional interactive menu:

```bash
python menu.py
```

## 8. Verify Everything Works

Run a safe, read-only script first, such as:

```bash
python scripts/s3/list_buckets.py
```

If it prints a list of buckets (or "No S3 buckets found"), your setup is working correctly.

## Troubleshooting

- **"Unable to locate credentials"** — Run `aws configure` again and double-check your Access Key ID and Secret Access Key.
- **"Access Denied"** — Your IAM user may not have the required permissions. See `iam_setup.md`.
- **"ModuleNotFoundError: No module named 'boto3'"** — Make sure your virtual environment is activated and you ran `pip install -r requirements.txt`.
