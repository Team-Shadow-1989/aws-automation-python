# Project Structure

This document explains how the project is organized and why.

## Folder Layout

```text
aws-python-automation/
│
├── README.md                  Main project overview
├── requirements.txt            Python dependencies
├── .gitignore                  Files excluded from git
├── config.py                   Shared AWS client configuration (the ONLY shared file)
├── menu.py                     Optional interactive launcher
├── architecture.png            Simple architecture diagram
│
├── docs/                       Documentation
│   ├── installation.md
│   ├── aws_cli_setup.md
│   ├── iam_setup.md
│   ├── project_structure.md
│   └── cleanup_guide.md
│
├── screenshots/                Placeholder folders for screenshots
│   ├── ec2/
│   ├── s3/
│   ├── ebs/
│   ├── vpc/
│   ├── security_group/
│   ├── iam/
│   ├── cloudwatch/
│   └── menu/
│
└── scripts/                    All AWS automation scripts, grouped by service
    ├── ec2/
    ├── s3/
    ├── ebs/
    ├── vpc/
    ├── security_group/
    ├── iam/
    └── cloudwatch/
```

## Design Principles

### 1. One Script, One Task

Every file inside `scripts/` performs exactly one AWS operation. For example:

- `scripts/ec2/list_instances.py` only lists instances.
- `scripts/ec2/start_instance.py` only starts an instance.

This makes the project easy to read, test, and reuse. You can copy a single script into another project without needing the rest of the repository (aside from `config.py`).

### 2. Only One Shared File

`config.py` is the only file every script depends on. It creates the Boto3 clients (`ec2_client`, `s3_client`, `iam_client`, `cloudwatch_client`) and stores the AWS region in one place.

No script imports another script. This keeps every file independent and easy to understand in isolation.

### 3. Scripts Are Fully Standalone

Every script can be run directly:

```bash
python scripts/ec2/list_instances.py
```

Each script contains a small snippet near the top that adds the project root to Python's import path, so it can find `config.py` even though it lives in a subfolder. You never need to run scripts as a package or set `PYTHONPATH` manually.

### 4. menu.py Is Optional

`menu.py` is a convenience launcher that simply runs the scripts in `scripts/` using Python's `subprocess` module. It contains no AWS logic. Deleting `menu.py` does not break any other part of the project.

### 5. Consistent Script Format

Every script follows the same internal structure:

1. File header comment (file name, description, usage)
2. Imports (standard library, then `config`, then `botocore.exceptions`)
3. A single function containing the script's logic
4. User input (if the operation needs it)
5. The AWS API call, wrapped in `try/except`
6. A clear success message
7. Friendly error messages for common AWS errors
8. An `if __name__ == "__main__":` block that runs the function

This consistency means once you understand one script, you understand the pattern used by all 46 scripts in the project.
