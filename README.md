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
│   ├── cloudformation.py
│   ├── cloudwatch.py
│   ├── compute.py
│   ├── database.py
│   ├── iam.py
│   ├── queue.py
│   ├── storage.py
├── demos/
│   ├── demo_cloudformation.py
│   ├── demo_cloudwatch.py
│   ├── demo_compute.py
│   ├── demo_database.py
│   ├── demo_iam.py
|   ├── demo_queue.py
|   ├── demo_storage.py
├── tests/
│   ├── test_compute.py
│   ├── test_cloudformation.py
│   ├── test_cloudwatch.pyv
│   ├── test_database.py
│   ├── test_iam.py
│   ├── test_queue.py
│   ├── test_storage.py
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

### **`demo_queue.py`**
Demonstrates the use of the `Queue` class for managing AWS SQS queues and messages.

#### **Functionalities**

1. **Queue Management**:
   - Create standard and FIFO queues.
   - Create and associate dead-letter queues (DLQs).
   - Delete queues.

   ```python
   standard_queue_url = queue_service.create_queue("DemoQueue")
   fifo_queue_url = queue_service.create_fifo_queue("DemoQueue.fifo")
   dlq_url, dlq_arn = queue_service.create_dead_letter_queue("DemoDLQ")
   queue_service.associate_dead_letter_queue(standard_queue_url, dlq_arn, max_receive_count=5)
   queue_service.delete_queue(standard_queue_url)
   ```

2. **Message Handling**:
   - Send individual and batch messages.
   - Receive and delete messages.

   ```python
   queue_service.send_message(standard_queue_url, "Hello, Queue!")
   batch_messages = [
       {"Id": "1", "MessageBody": "Message 1"},
       {"Id": "2", "MessageBody": "Message 2"},
   ]
   queue_service.send_message_batch(standard_queue_url, batch_messages)
   messages = queue_service.receive_messages(standard_queue_url, max_number=5)
   for message in messages:
       queue_service.delete_message(standard_queue_url, message["ReceiptHandle"])
   ```

3. **Queue Attributes**:
   - Retrieve and update queue attributes.

   ```python
   attributes = queue_service.get_queue_attributes(standard_queue_url)
   queue_service.set_queue_attributes(standard_queue_url, {"VisibilityTimeout": "30"})
   ```

4. **Monitoring**:
   - Monitor the approximate number of messages in a queue.

   ```python
   message_count = queue_service.monitor_message_count(standard_queue_url)
   print(f"Messages in queue: {message_count}")
   ```

---

### **`demo_compute.py`**
Demonstrates the use of the `Compute` class for managing AWS EC2 resources.

#### **Functionalities**

1. **Key Pair Management**:
   - Create a key pair.

   ```python
   key_material = compute.create_key_pair("demo-key")
   print(f"Private key:\n{key_material}")
   ```

2. **Instance Operations**:
   - Launch, stop, start, and terminate instances.
   - Describe instance status.

   ```python
   instance_id = compute.create_instance("t2.micro", "demo-key")
   print(f"Instance '{instance_id}' launched successfully.")
   status = compute.describe_instance_status(instance_id)
   print(f"Instance status: {status}")
   compute.stop_instance(instance_id)
   compute.start_instance(instance_id)
   compute.terminate_instance(instance_id)
   ```

3. **Elastic IP Management**:
   - Allocate and associate an Elastic IP.

   ```python
   elastic_ip = compute.allocate_elastic_ip()
   print(f"Elastic IP allocated: {elastic_ip['PublicIp']}")
   compute.associate_elastic_ip(elastic_ip["AllocationId"], instance_id)
   ```

4. **Tagging Resources**:
   - Add tags to EC2 resources.

   ```python
   compute.tag_resource(instance_id, [{"Key": "Name", "Value": "DemoInstance"}])
   ```

5. **Volume Management**:
   - Create and attach EBS volumes.

   ```python
   volume_id = compute.create_volume("us-east-1a", 10)
   compute.attach_volume(volume_id, instance_id, "/dev/xvdf")
   ```

---

### **`demo_storage.py`**
Demonstrates the use of the `Storage` class for managing AWS S3 buckets and objects.

#### **Functionalities**

1. **Bucket Management**:
   - Create and list buckets.

   ```python
   storage.create_bucket("demo-bucket")
   buckets = storage.list_buckets()
   print(f"Buckets: {[bucket['Name'] for bucket in buckets]}")
   ```

2. **File Upload**:
   - Upload a file to a bucket.

   ```python
   storage.upload_file("demo-bucket", "example.txt", "This is a test file for the demo.")
   ```

3. **List Objects in Bucket**:
   - List all objects in a bucket.

   ```python
   objects = storage.list_objects("demo-bucket")
   print(f"Objects: {[obj['Key'] for obj in objects]}")
   ```

4. **Delete Object**:
   - Delete an object from a bucket.

   ```python
   storage.delete_object("demo-bucket", "example.txt")
   ```

5. **Verify Deletion**:
   - Verify that the object is deleted.

   ```python
   objects_after_deletion = storage.list_objects("demo-bucket")
   print(f"Objects after deletion: {[obj['Key'] for obj in objects_after_deletion]}")
   ```

---

### **`demo_database.py`**
Demonstrates the use of the `Database` class for managing AWS DynamoDB resources.

#### **Functionalities**

1. **Table Management**:
   - Create and describe DynamoDB tables.

   ```python
   key_schema = [{"AttributeName": "id", "KeyType": "HASH"}]
   attribute_definitions = [{"AttributeName": "id", "AttributeType": "S"}]
   provisioned_throughput = {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}
   print(database.create_table("DemoTable", key_schema, attribute_definitions, provisioned_throughput))
   table_info = database.describe_table("DemoTable")
   print(f"Table Info: {table_info}")
   ```

2. **Item Operations**:
   - Add, update, delete, and scan items in the table.

   ```python
   item = {"id": {"S": "1"}, "name": {"S": "Alice"}, "age": {"N": "30"}}
   print(database.put_item("DemoTable", item))
   items = database.scan_table("DemoTable")
   print(f"Items in table: {items}")

   update_expression = "SET #name = :name, age = :age"
   expression_attribute_values = {":name": {"S": "Alice Updated"}, ":age": {"N": "31"}}
   expression_attribute_names = {"#name": "name"}
   print(database.update_item("DemoTable", {"id": {"S": "1"}}, update_expression, expression_attribute_values, expression_attribute_names))
   print(database.delete_item("DemoTable", {"id": {"S": "1"}}))
   ```

3. **Batch Operations**:
   - Insert multiple items into a table.

   ```python
   batch_items = [
       {"id": {"S": "2"}, "name": {"S": "Bob"}, "age": {"N": "25"}},
       {"id": {"S": "3"}, "name": {"S": "Charlie"}, "age": {"N": "28"}},
   ]
   print(database.batch_write_items("DemoTable", batch_items))
   ```

4. **Table Deletion**:
   - Delete a DynamoDB table.

   ```python
   print(database.delete_table("DemoTable"))
   ```

---

## **Contributing**

Contributions are welcome! Please open an issue or submit a pull request to propose changes or add new features.

---

## **License**

This project is licensed under the [MIT License](LICENSE).

---
