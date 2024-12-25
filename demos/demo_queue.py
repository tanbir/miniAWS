import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_wrapper.queue import Queue
from moto import mock_aws

@mock_aws
def main():
    # Initialize the Queue wrapper
    queue_service = Queue(region="us-east-1")

    # Queue names
    standard_queue_name = "DemoQueue"
    fifo_queue_name = "DemoQueue.fifo"
    dlq_name = "DemoDLQ"

    print("\n--- Queue Management ---")
    # Create a standard queue
    standard_queue_url = queue_service.create_queue(standard_queue_name)
    print(f"Standard Queue URL: {standard_queue_url}")

    # Create a FIFO queue
    fifo_queue_url = queue_service.create_fifo_queue(fifo_queue_name)
    print(f"FIFO Queue URL: {fifo_queue_url}")

    # Create a dead-letter queue (DLQ)
    dlq_url, dlq_arn = queue_service.create_dead_letter_queue(dlq_name)
    print(f"DLQ URL: {dlq_url}")
    print(f"DLQ ARN: {dlq_arn}")

    # Associate DLQ with the standard queue
    print(queue_service.associate_dead_letter_queue(standard_queue_url, dlq_arn, max_receive_count=5))

    print("\n--- Send and Receive Messages ---")
    # Send a single message
    print(queue_service.send_message(standard_queue_url, "Hello, Queue!"))

    # Send batch messages
    messages = [
        {"Id": "1", "MessageBody": "Batch Message 1"},
        {"Id": "2", "MessageBody": "Batch Message 2"},
        {"Id": "3", "MessageBody": "Batch Message 3"},
    ]
    print(queue_service.send_message_batch(standard_queue_url, messages))

    # Receive messages
    received_messages = queue_service.receive_messages(standard_queue_url, max_number=10)
    for message in received_messages:
        print(f"Received: {message['Body']}")
        print(queue_service.delete_message(standard_queue_url, message["ReceiptHandle"]))

    print("\n--- Queue Attributes ---")
    # Get queue attributes
    attributes = queue_service.get_queue_attributes(standard_queue_url)
    print("Queue Attributes:", attributes)

    print("\n--- Monitoring ---")
    # Monitor message count
    message_count = queue_service.monitor_message_count(standard_queue_url)
    print(f"Approximate number of messages in queue: {message_count}")

    print("\n--- Queue Deletion ---")
    # Delete all queues
    print(queue_service.delete_queue(standard_queue_url))
    print(queue_service.delete_queue(fifo_queue_url))
    print(queue_service.delete_queue(dlq_url))


if __name__ == "__main__":
    main()
