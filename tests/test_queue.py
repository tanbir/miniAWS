import unittest
from moto import mock_aws
import boto3
from aws_wrapper.queue import Queue


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    @mock_aws
    def test_create_and_delete_queue(self):
        self.queue.sqs = boto3.client("sqs", region_name="us-east-1")
        queue_url = self.queue.create_queue("test-queue")
        self.assertTrue(queue_url.startswith("https://"))
        self.assertEqual(
            self.queue.delete_queue(queue_url),
            f"Queue at '{queue_url}' deleted successfully.",
        )

    @mock_aws
    def test_send_and_receive_message(self):
        self.queue.sqs = boto3.client("sqs", region_name="us-east-1")
        queue_url = self.queue.create_queue("test-queue")
        message_id = self.queue.send_message(queue_url, "Hello, World!")
        self.assertIsInstance(message_id, str)

        messages = self.queue.receive_messages(queue_url)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0]["Body"], "Hello, World!")

    @mock_aws
    def test_send_and_delete_batch_messages(self):
        self.queue.sqs = boto3.client("sqs", region_name="us-east-1")
        queue_url = self.queue.create_queue("test-queue")
        messages = [{"Id": "1", "MessageBody": "Message 1"}, {"Id": "2", "MessageBody": "Message 2"}]
        self.assertEqual(
            self.queue.send_message_batch(queue_url, messages),
            "2 messages sent successfully.",
        )

        received_messages = self.queue.receive_messages(queue_url)
        receipt_handles = [msg["ReceiptHandle"] for msg in received_messages]
        self.assertEqual(
            self.queue.delete_messages_batch(queue_url, receipt_handles),
            "2 messages deleted successfully.",
        )

    @mock_aws
    def test_create_and_associate_dlq(self):
        self.queue.sqs = boto3.client("sqs", region_name="us-east-1")
        dlq_url, dlq_arn = self.queue.create_dead_letter_queue("test-dlq")
        queue_url = self.queue.create_queue("test-queue")
        self.assertEqual(
            self.queue.associate_dead_letter_queue(queue_url, dlq_arn),
            f"Dead-letter queue associated with queue at '{queue_url}'.",
        )

    @mock_aws
    def test_get_and_set_queue_attributes(self):
        self.queue.sqs = boto3.client("sqs", region_name="us-east-1")
        queue_url = self.queue.create_queue("test-queue")
        attributes = self.queue.get_queue_attributes(queue_url)
        self.assertIn("ApproximateNumberOfMessages", attributes)

        updated_attributes = {"VisibilityTimeout": "60"}
        self.assertEqual(
            self.queue.set_queue_attributes(queue_url, updated_attributes),
            f"Attributes updated for queue at '{queue_url}'.",
        )

    @mock_aws
    def test_fifo_queue(self):
        self.queue.sqs = boto3.client("sqs", region_name="us-east-1")
        fifo_queue_url = self.queue.create_fifo_queue("test-queue.fifo")
        self.assertTrue(fifo_queue_url.startswith("https://"))


if __name__ == "__main__":
    unittest.main()
