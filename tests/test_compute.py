import unittest
from moto import mock_aws
import boto3
from aws_wrapper.compute import Compute


class TestCompute(unittest.TestCase):
    def setUp(self):
        self.compute = Compute()

    @mock_aws
    def test_create_and_terminate_instance(self):
        self.compute.ec2 = boto3.client("ec2", region_name="us-east-1")
        instance_id = self.compute.create_instance("t2.micro", "test-key")
        self.assertTrue(instance_id.startswith("i-"))
        self.assertEqual(self.compute.terminate_instance(instance_id), f"Instance '{instance_id}' terminated successfully.")

    @mock_aws
    def test_stop_and_start_instance(self):
        self.compute.ec2 = boto3.client("ec2", region_name="us-east-1")
        instance_id = self.compute.create_instance("t2.micro", "test-key")
        self.assertEqual(self.compute.stop_instance(instance_id), f"Instance '{instance_id}' stopped successfully.")
        self.assertEqual(self.compute.start_instance(instance_id), f"Instance '{instance_id}' started successfully.")

    @mock_aws
    def test_create_key_pair(self):
        self.compute.ec2 = boto3.client("ec2", region_name="us-east-1")
        key_material = self.compute.create_key_pair("test-key")
        self.assertIn("-----BEGIN RSA PRIVATE KEY-----", key_material)

    @mock_aws
    def test_allocate_and_associate_elastic_ip(self):
        self.compute.ec2 = boto3.client("ec2", region_name="us-east-1")
        allocation = self.compute.allocate_elastic_ip()
        instance_id = self.compute.create_instance("t2.micro", "test-key")
        self.assertEqual(
            self.compute.associate_elastic_ip(allocation["AllocationId"], instance_id),
            f"Elastic IP associated with instance '{instance_id}'.",
        )

    @mock_aws
    def test_tag_resource(self):
        self.compute.ec2 = boto3.client("ec2", region_name="us-east-1")
        instance_id = self.compute.create_instance("t2.micro", "test-key")
        tags = [{"Key": "Name", "Value": "TestInstance"}]
        self.assertEqual(
            self.compute.tag_resource(instance_id, tags),
            f"Tags {str(tags)} added to resource '{instance_id}'.",
        )

    @mock_aws
    def test_create_and_attach_volume(self):
        self.compute.ec2 = boto3.client("ec2", region_name="us-east-1")
        instance_id = self.compute.create_instance("t2.micro", "test-key")
        volume_id = self.compute.create_volume("us-east-1a", 10)
        self.assertTrue(volume_id.startswith("vol-"))
        self.assertEqual(
            self.compute.attach_volume(volume_id, instance_id, "/dev/xvdf"),
            f"Volume '{volume_id}' attached to instance '{instance_id}'.",
        )


if __name__ == "__main__":
    unittest.main()
