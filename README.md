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

## **IAM Class**

### **Functionality**

| **Function**                     | **Description**                                                                                   |
|-----------------------------------|---------------------------------------------------------------------------------------------------|
| `create_iam_user(user_name)`      | Creates a new IAM user.                                                                           |
| `list_iam_users()`                | Lists all IAM users.                                                                              |
| `delete_iam_user(user_name)`      | Deletes an IAM user.                                                                              |
| `create_group(group_name)`        | Creates a new IAM group.                                                                          |
| `list_groups()`                   | Lists all IAM groups.                                                                             |
| `delete_group(group_name)`        | Deletes an IAM group.                                                                             |
| `add_user_to_group(user, group)`  | Adds a user to a group.                                                                           |
| `remove_user_from_group(user, group)` | Removes a user from a group.                                                                  |
| `create_role(role_name, policy)`  | Creates a new IAM role.                                                                           |
| `list_roles()`                    | Lists all IAM roles.                                                                              |
| `delete_role(role_name)`          | Deletes an IAM role.                                                                              |
| `create_policy(name, document)`   | Creates a new IAM policy.                                                                         |
| `delete_policy(policy_arn)`       | Deletes an IAM policy.                                                                            |
| `attach_user_policy(user, policy)`| Attaches a policy to a user.                                                                      |
| `detach_user_policy(user, policy)`| Detaches a policy from a user.                                                                    |
| `attach_group_policy(group, policy)` | Attaches a policy to a group.                                                                  |
| `detach_group_policy(group, policy)` | Detaches a policy from a group.                                                                |

---

## **CloudWatch Class**

### **Functionality**

| **Function**                     | **Description**                                                                                   |
|-----------------------------------|---------------------------------------------------------------------------------------------------|
| `create_log_group(name)`          | Creates a new CloudWatch log group.                                                               |
| `list_log_groups()`               | Lists all CloudWatch log groups.                                                                  |
| `delete_log_group(name)`          | Deletes a CloudWatch log group.                                                                   |
| `put_metric_data(ns, name, value, dimensions, unit)` | Publishes a custom metric to CloudWatch.                                       |
| `list_metrics(ns)`                | Lists all metrics in a specific namespace.                                                       |
| `create_alarm(name, metric, ns, threshold, ...)` | Creates a CloudWatch alarm.                                                               |
| `list_alarms()`                   | Lists all CloudWatch alarms.                                                                      |
| `delete_alarm(name)`              | Deletes a CloudWatch alarm.                                                                       |
| `create_dashboard(name, body)`    | Creates a CloudWatch dashboard.                                                                   |
| `list_dashboards()`               | Lists all CloudWatch dashboards.                                                                  |
| `delete_dashboard(name)`          | Deletes a CloudWatch dashboard.                                                                   |

---

## **CloudFormation Class**

### **Functionality**

| **Function**                     | **Description**                                                                                   |
|-----------------------------------|---------------------------------------------------------------------------------------------------|
| `create_stack(name, template)`    | Creates a CloudFormation stack using a given template.                                            |
| `delete_stack(name)`              | Deletes a CloudFormation stack.                                                                   |
| `list_stacks()`                   | Lists all CloudFormation stacks.                                                                  |
| `update_stack(name, template)`    | Updates a stack with a new template.                                                              |
| `describe_stack(name)`            | Describes the details of a specific stack.                                                        |

---

## **Queue Class**

### **Functionality**

| **Function**                     | **Description**                                                                                   |
|-----------------------------------|---------------------------------------------------------------------------------------------------|
| `create_queue(name)`              | Creates a new SQS queue.                                                                          |
| `list_queues()`                   | Lists all SQS queues.                                                                             |
| `delete_queue(name)`              | Deletes an SQS queue.                                                                             |
| `send_message(queue, message)`    | Sends a message to an SQS queue.                                                                  |
| `receive_message(queue)`          | Receives messages from an SQS queue.                                                              |
| `delete_message(queue, receipt)`  | Deletes a message from an SQS queue using its receipt handle.                                     |

---

## **Usage**

### **Demo Scripts**

#### **`demo_iam.py`**
Demonstrates the use of the `IAM` class for managing AWS IAM resources.

Run the script:
```bash
python demos/demo_iam.py
```

#### **`demo_cloudwatch.py`**
Demonstrates the use of the `CloudWatch` class for managing AWS CloudWatch resources.

Run the script:
```bash
python demos/demo_cloudwatch.py
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

## **License**

This project is licensed under the [MIT License](LICENSE).

---
