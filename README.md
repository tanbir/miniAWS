---

# **MiniAWS Simulator**

MiniAWS is a Python-based library that simulates interactions with AWS services using classes to abstract AWS SDK (boto3) functionality. It enables developers to prototype, test, and interact with AWS-like services locally or in real environments.

---

## **Features**

The project includes several classes to interact with AWS services:

| **Class**            | **Description**                                                                                     |
|----------------------|-----------------------------------------------------------------------------------------------------|
| `IAM`                | Manage IAM users, groups, roles, and policies.                                                     |
| `CloudWatch`         | Handle CloudWatch metrics, alarms, logs, and dashboards.                                           |
| `CloudFormation`     | Create, update, and delete CloudFormation stacks; manage templates, events, and policies.           |
| `Queue`              | Manage SQS queues, messages, and dead-letter queues.                                               |
| `Storage`            | Interact with S3 buckets and objects.                                                              |
| `Database`           | Manage DynamoDB tables and records.                                                                |
| `Compute`            | Manage EC2 instances, security groups, and related compute resources.                              |

---

## **IAM Class**

The `IAM` class provides methods to manage IAM users, groups, roles, and policies.

### **Functionalities Demonstrated in `demo_iam.py`**

1. **User Management**:
   - Create, list, and delete IAM users.
   ```python
   iam.create_iam_user("test-user")
   iam.list_iam_users()
   iam.delete_iam_user("test-user")
   ```

2. **Group Management**:
   - Create, list, delete groups, and manage user-group relationships.
   ```python
   iam.create_group("test-group")
   iam.add_user_to_group("test-user", "test-group")
   iam.remove_user_from_group("test-user", "test-group")
   iam.delete_group("test-group")
   ```

3. **Role Management**:
   - Create, list, and delete IAM roles.
   - Attach a policy to a role.
   ```python
   assume_role_policy = """{
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "Service": "ec2.amazonaws.com"
               },
               "Action": "sts:AssumeRole"
           }
       ]
   }"""
   iam.create_role("test-role", assume_role_policy)
   iam.attach_role_policy("test-role", policy_arn)
   iam.delete_role("test-role")
   ```

4. **Policy Management**:
   - Create, list, attach, and delete policies.
   - Attach policies to users, groups, and roles.
   ```python
   policy_document = """{
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": "s3:ListBucket",
               "Resource": "arn:aws:s3:::example-bucket"
           }
       ]
   }"""
   policy_arn = iam.create_policy("test-policy", policy_document)
   iam.attach_user_policy("test-user", policy_arn)
   iam.attach_group_policy("test-group", policy_arn)
   iam.delete_policy(policy_arn)
   ```

---

## **Installation**

### Prerequisites
- Python 3.8 or later
- [Pipenv](https://pipenv.pypa.io/en/latest/) or virtualenv (optional, for isolated environments)
- AWS credentials configured via the AWS CLI or environment variables (if running against AWS)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/miniAWS.git
   cd miniAWS
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Install `moto` for testing:
   ```bash
   pip install moto
   ```

---

## **Usage**

### **IAM**

#### **User Management**
```python
iam = IAM(region="us-east-1")
print(iam.create_iam_user("test-user"))
print(iam.list_iam_users())
print(iam.delete_iam_user("test-user"))
```

#### **Group Management**
```python
iam.create_group("test-group")
iam.add_user_to_group("test-user", "test-group")
iam.remove_user_from_group("test-user", "test-group")
iam.delete_group("test-group")
```

#### **Role Management**
```python
assume_role_policy = """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}"""
iam.create_role("test-role", assume_role_policy)
iam.attach_role_policy("test-role", policy_arn)
iam.delete_role("test-role")
```

#### **Policy Management**
```python
policy_document = """{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::example-bucket"
        }
    ]
}"""
policy_arn = iam.create_policy("test-policy", policy_document)
iam.attach_user_policy("test-user", policy_arn)
iam.delete_policy(policy_arn)
```

---

## **Testing**

Unit tests are implemented for all classes using the **`moto`** library to mock AWS services.

### Run All Tests

```bash
pytest tests
```

### Run Tests for a Specific Class

```bash
pytest tests/test_iam.py
```

---

## **Directory Structure**

```
miniAWS/
├── aws_wrapper/
│   ├── __init__.py
│   ├── iam.py
│   ├── cloudwatch.py
│   ├── cloudformation.py
│   ├── queue.py
│   ├── storage.py
│   ├── database.py
│   ├── compute.py
├── demos/
│   ├── demo_iam.py
├── tests/
│   ├── test_iam.py
│   ├── test_cloudwatch.py
│   ├── test_cloudformation.py
│   ├── test_queue.py
│   ├── test_storage.py
│   ├── test_database.py
│   ├── test_compute.py
├── requirements.txt
└── README.md
```

---

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request to propose changes or add new features.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---

## **Acknowledgments**

- [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html): Python SDK for AWS.
- [Moto](https://github.com/spulec/moto): Library for mocking AWS services in tests.

---
