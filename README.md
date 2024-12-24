---

# **MiniAWS Simulator**

MiniAWS is a Python-based library that simulates interactions with AWS services using classes to abstract AWS SDK (`boto3`) functionality. It enables developers to prototype, test, and interact with AWS-like services locally or in real environments.

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

## **Testing**

Unit tests are implemented for all classes using the **`moto`** library to mock AWS services.

### Run All Tests

```bash
pytest tests
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
│   ├── demo_cloudwatch.py
│   ├── demo_cloudformation.py
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

## **Demo Scripts**

### **`demo_iam.py`**
Demonstrates the use of the `IAM` class for managing AWS IAM resources.

#### **Functionalities**

1. **User Management**:
   - Create, list, and delete IAM users.

   ```python
   iam.create_iam_user("test-user")
   users = iam.list_iam_users()
   iam.delete_iam_user("test-user")
   ```

2. **Group Management**:
   - Create, list, and delete groups.
   - Add and remove users from groups.

   ```python
   iam.create_group("test-group")
   iam.add_user_to_group("test-user", "test-group")
   iam.remove_user_from_group("test-user", "test-group")
   iam.delete_group("test-group")
   ```

3. **Role Management**:
   - Create, list, and delete roles.

   ```python
   assume_role_policy = """{
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {"Service": "ec2.amazonaws.com"},
               "Action": "sts:AssumeRole"
           }
       ]
   }"""
   iam.create_role("test-role", assume_role_policy)
   roles = iam.list_roles()
   iam.delete_role("test-role")
   ```

4. **Policy Management**:
   - Create, attach, detach, and delete policies for users, groups, and roles.

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
   iam.detach_user_policy("test-user", policy_arn)
   iam.delete_policy(policy_arn)
   ```

---

### **`demo_cloudwatch.py`**
Demonstrates the use of the `CloudWatch` class for managing AWS CloudWatch resources.

#### **Functionalities**

1. **Log Group Management**:
   - Create, list, and delete log groups.

   ```python
   cw.create_log_group("test-log-group")
   log_groups = cw.list_log_groups()
   cw.delete_log_group("test-log-group")
   ```

2. **Metric Management**:
   - Publish custom metrics to CloudWatch.
   - List metrics in a specific namespace.

   ```python
   namespace = "MyNamespace"
   metric_name = "MyMetric"
   dimensions = [{"Name": "InstanceId", "Value": "i-12345678"}]
   cw.put_metric_data(namespace, metric_name, value=100, dimensions=dimensions)
   metrics = cw.list_metrics(namespace=namespace)
   ```

3. **Alarm Management**:
   - Create and delete alarms.
   - List active alarms.

   ```python
   alarm_name = "HighCPUUtilization"
   cw.create_alarm(
       alarm_name=alarm_name,
       metric_name=metric_name,
       namespace=namespace,
       threshold=80,
       comparison_operator="GreaterThanThreshold",
       evaluation_periods=1,
       period=60,
       statistic="Average",
       dimensions=dimensions,
   )
   alarms = cw.list_alarms()
   cw.delete_alarm(alarm_name)
   ```

4. **Dashboard Management**:
   - Create, list, and delete dashboards.

   ```python
   dashboard_name = "TestDashboard"
   dashboard_body = """{
       "widgets": [
           {
               "type": "metric",
               "x": 0,
               "y": 0,
               "width": 6,
               "height": 6,
               "properties": {
                   "metrics": [
                       ["MyNamespace", "MyMetric"]
                   ],
                   "period": 300,
                   "stat": "Average",
                   "region": "us-east-1",
                   "title": "MyMetric Dashboard"
               }
           }
       ]
   }"""
   cw.create_dashboard(dashboard_name, dashboard_body)
   dashboards = cw.list_dashboards()
   cw.delete_dashboard(dashboard_name)
   ```

---

### **`demo_cloudformation.py`**
Demonstrates the use of the `CloudFormation` class for managing AWS CloudFormation stacks.

#### **Functionalities**

1. **Create a Stack**:
   - Creates a CloudFormation stack with a simple S3 bucket template.

   ```python
   stack_name = "DemoStack"
   template_body = """{
       "Resources": {
           "MyBucket": {
               "Type": "AWS::S3::Bucket",
               "Properties": {
                   "BucketName": "demo-cloudformation-bucket"
               }
           }
       }
   }"""
   print(cloudformation.create_stack(stack_name, template_body))
   ```

2. **List Stacks**:
   - Lists all existing CloudFormation stacks.

   ```python
   stacks = cloudformation.list_stacks()
   print("Stacks:", stacks)
   ```

3. **Describe a Stack**:
   - Retrieves details of the specified stack.

   ```python
   stack_description = cloudformation.describe_stack(stack_name)
   print("Description:", stack_description)
   ```

4. **Update a Stack**:
   - Updates the stack using a new template.

   ```python
   updated_template_body = """{
       "Resources": {
           "MyBucket": {
               "Type": "AWS::S3::Bucket",
               "Properties": {
                   "BucketName": "updated-cloudformation-bucket"
               }
           }
       }
   }"""
   print(cloudformation.update_stack(stack_name, updated_template_body))
   ```

5. **Delete a Stack**:
   - Deletes the specified CloudFormation stack.

   ```python
   print(cloudformation.delete_stack(stack_name))
   ```

---

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request to propose changes or add new features.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---
