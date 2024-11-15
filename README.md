# apigw-security

`apigw-security` is a Python tool designed to retrieve API Gateway stages across all regions of an AWS account and run security assessments using the OWASP Offensive API Testing (OWASP OffSec API Testing) module. The results are output to HTML files, allowing easy review of each API's security posture.

This project was inspired by the need to transition away from the existing vendor, Data Theorem.

## Features

- Scans API Gateway stages across all AWS regions in the specified AWS account.
- Utilizes the OWASP OffSec API Testing module to perform security checks.
- Outputs detailed results to HTML files for each API Gateway.
- Supports multi-region scanning for comprehensive coverage.

## Requirements

- **Python** 3.8+
- **AWS CLI** configured with appropriate permissions.
- **boto3** library for AWS interactions.
- **requests** library for HTTP requests (if required by the OffSec module).
- **OWASP OffSec API Testing** module.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/gar-rock/apigw-security.git
    cd apigw-security
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Ensure that the AWS CLI is configured for your account**:

    ```bash
    aws configure
    ```

## Usage

To run the tool, use the following command:

```bash
python main.py
```