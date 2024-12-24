import boto3
import json
from aws_wrapper.aws_manager import AWSManager


class Queue(AWSManager):
    def __init__(self, region="us-east-1"):
        super().__init__(region)
        self.sqs = boto3.client("sqs", region_name=self.region)

    # Queue Operations
    def create_queue(self, queue_name):
        response = self.sqs.create_queue(QueueName=queue_name)
        return response["QueueUrl"]

    def create_queue_with_attributes(self, queue_name, attributes):
        response = self.sqs.create_queue(QueueName=queue_name, Attributes=attributes)
        return response["QueueUrl"]

    def delete_queue(self, queue_url):
        self.sqs.delete_queue(QueueUrl=queue_url)
        return f"Queue at '{queue_url}' deleted successfully."

    # Message Handling
    def send_message(self, queue_url, message_body):
        response = self.sqs.send_message(QueueUrl=queue_url, MessageBody=message_body)
        return response["MessageId"]

    def send_message_batch(self, queue_url, messages):
        response = self.sqs.send_message_batch(QueueUrl=queue_url, Entries=messages)
        return f"{len(response['Successful'])} messages sent successfully."

    def receive_messages(self, queue_url, max_number=10):
        response = self.sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_number,
            WaitTimeSeconds=10,
        )
        return response.get("Messages", [])

    def delete_message(self, queue_url, receipt_handle):
        self.sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        return f"Message deleted from queue at '{queue_url}'."

    def delete_messages_batch(self, queue_url, receipt_handles):
        entries = [{"Id": str(i), "ReceiptHandle": receipt_handle} for i, receipt_handle in enumerate(receipt_handles)]
        response = self.sqs.delete_message_batch(QueueUrl=queue_url, Entries=entries)
        return f"{len(response['Successful'])} messages deleted successfully."

    # Queue Attributes
    def get_queue_attributes(self, queue_url):
        response = self.sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["All"])
        return response["Attributes"]

    def set_queue_attributes(self, queue_url, attributes):
        self.sqs.set_queue_attributes(QueueUrl=queue_url, Attributes=attributes)
        return f"Attributes updated for queue at '{queue_url}'."

    # Dead-Letter Queue (DLQ) Management
    def create_dead_letter_queue(self, dlq_name):
        dlq_url = self.sqs.create_queue(QueueName=dlq_name)["QueueUrl"]
        dlq_arn = self.get_queue_attributes(dlq_url)["QueueArn"]
        return dlq_url, dlq_arn

    def associate_dead_letter_queue(self, queue_url, dlq_arn, max_receive_count=5):
        redrive_policy = {
            "deadLetterTargetArn": dlq_arn,
            "maxReceiveCount": str(max_receive_count),
        }
        self.sqs.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={"RedrivePolicy": json.dumps(redrive_policy)},
        )
        return f"Dead-letter queue associated with queue at '{queue_url}'."

    # FIFO Queue
    def create_fifo_queue(self, queue_name, attributes=None):
        if not queue_name.endswith(".fifo"):
            raise ValueError("FIFO queue names must end with '.fifo'")
        if attributes is None:
            attributes = {}
        attributes["FifoQueue"] = "true"
        response = self.sqs.create_queue(QueueName=queue_name, Attributes=attributes)
        return response["QueueUrl"]

    # Monitoring
    def monitor_message_count(self, queue_url):
        attributes = self.get_queue_attributes(queue_url)
        return int(attributes["ApproximateNumberOfMessages"])
