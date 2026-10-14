# AWS CLI Setup Guide

This project uses Boto3, which relies on the same credential system as the AWS CLI. Setting up the AWS CLI is the easiest way to configure your credentials.

## 1. Install the AWS CLI

**Linux:**

```bash
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

**macOS:**

```bash
brew install awscli
```

**Windows:**

Download and run the installer from the official AWS CLI page.

Verify the installation:

```bash
aws --version
```

## 2. Get Your AWS Access Keys

1. Sign in to the AWS Management Console.
2. Go to **IAM** (see `iam_setup.md` for creating a dedicated automation user).
3. Select your IAM user.
4. Go to the **Security credentials** tab.
5. Click **Create access key**.
6. Choose **Command Line Interface (CLI)** as the use case.
7. Save the **Access Key ID** and **Secret Access Key** somewhere safe. AWS will not show the secret key again.

## 3. Configure the CLI

Run:

```bash
aws configure
```

You will be prompted for:

```text
AWS Access Key ID [None]: YOUR_ACCESS_KEY_ID
AWS Secret Access Key [None]: YOUR_SECRET_ACCESS_KEY
Default region name [None]: ap-south-1
Default output format [None]: json
```

This saves your credentials to:

- `~/.aws/credentials` (Access Key ID and Secret Access Key)
- `~/.aws/config` (region and output format)

## 4. Verify Your Credentials Work

```bash
aws sts get-caller-identity
```

If configured correctly, this returns your AWS account ID, user ID, and ARN.

## 5. Using Multiple AWS Profiles (Optional)

If you work with more than one AWS account, you can create named profiles:

```bash
aws configure --profile automation-project
```

To use a named profile with this project, you can set an environment variable before running any script:

```bash
export AWS_PROFILE=automation-project
```

## Security Best Practices

- Never commit your AWS credentials to GitHub. The `.gitignore` file in this project already excludes common credential file patterns.
- Use an IAM user with only the permissions this project needs (see `iam_setup.md`), not your AWS root account.
- Rotate access keys periodically and delete ones you no longer use.
