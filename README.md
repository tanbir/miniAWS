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

## **Installation**

### Prerequisites
- Python 3.8 or later
- [Pipenv](https://pipenv.pypa.io/en/latest/) or virtualenv (optional, for isolated environments)
- AWS credentials configured via the AWS CLI or environment variables (if running against AWS)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/tanbir/miniAWS.git
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
Manage IAM users, groups, roles, and policies.

```python
from aws_wrapper.iam import IAM

iam = IAM(region="us-east-1")

# Create a new user
print(iam.create_iam_user("test-user"))

# Create and attach a policy
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
print(iam.attach_user_policy("test-user", policy_arn))
```

---

### **CloudWatch**
Manage CloudWatch metrics, alarms, logs, and dashboards.

```python
from aws_wrapper.cloudwatch import CloudWatch

cw = CloudWatch(region="us-east-1")

# Publish a metric
print(cw.put_metric_data("MyNamespace", "MyMetric", 100, unit="Count"))

# Create a CloudWatch log group
print(cw.create_log_group("MyLogGroup"))
```

---

### **CloudFormation**
Handle infrastructure as code with CloudFormation stacks.

```python
from aws_wrapper.cloudformation import CloudFormation

cf = CloudFormation(region="us-east-1")

# Create a stack
template_body = """{
    "Resources": {
        "MyBucket": {
            "Type": "AWS::S3::Bucket",
            "Properties": {
                "BucketName": "my-cloudformation-bucket"
            }
        }
    }
}"""
print(cf.create_stack("MyTestStack", template_body))
```

---

### **Queue**
Manage SQS queues and messages.

```python
from aws_wrapper.queue import Queue

queue = Queue(region="us-east-1")

# Create a queue
queue_url = queue.create_queue("test-queue")

# Send and receive messages
queue.send_message(queue_url, "Hello, World!")
messages = queue.receive_messages(queue_url)
print(messages)
```

---

### **Storage**
Handle S3 buckets and objects.

```python
from aws_wrapper.storage import Storage

storage = Storage(region="us-east-1")

# Create a bucket and upload a file
storage.create_bucket("test-bucket")
storage.upload_file("test-bucket", "local_file.txt", "remote_file.txt")
```

---

### **Database**
Interact with DynamoDB tables and records.

```python
from aws_wrapper.database import Database

db = Database(region="us-east-1")

# Create a DynamoDB table
db.create_table(
    "test-table",
    key_schema=[{"AttributeName": "id", "KeyType": "HASH"}],
    attribute_definitions=[{"AttributeName": "id", "AttributeType": "S"}],
    provisioned_throughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1},
)
```

---

### **Compute**
Manage EC2 instances and related resources.

```python
from aws_wrapper.compute import Compute

compute = Compute(region="us-east-1")

# Create an EC2 instance
print(compute.create_instance("t2.micro", "test-key"))
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
