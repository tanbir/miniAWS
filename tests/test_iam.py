import unittest
from moto import mock_aws
import boto3
from aws_wrapper.iam import IAM


class TestIAM(unittest.TestCase):
    def setUp(self):
        self.iam = IAM(region="us-east-1")

    @mock_aws
    def test_create_and_delete_iam_user(self):
        self.iam.iam = boto3.client("iam", region_name="us-east-1")
        # Test user creation
        response = self.iam.create_iam_user("test-user")
        self.assertEqual(response, "IAM user 'test-user' created successfully.")

        # Test listing users
        users = self.iam.list_iam_users()
        self.assertIn("test-user", users)

        # Test user deletion
        response = self.iam.delete_iam_user("test-user")
        self.assertEqual(response, "IAM user 'test-user' deleted successfully.")

        # Test listing users after deletion
        users = self.iam.list_iam_users()
        self.assertNotIn("test-user", users)

    @mock_aws
    def test_create_and_delete_group(self):
        self.iam.iam = boto3.client("iam", region_name="us-east-1")
        # Test group creation
        response = self.iam.create_group("test-group")
        self.assertEqual(response, "IAM group 'test-group' created successfully.")

        # Test listing groups
        groups = self.iam.list_groups()
        self.assertIn("test-group", groups)

        # Test group deletion
        response = self.iam.delete_group("test-group")
        self.assertEqual(response, "IAM group 'test-group' deleted successfully.")

        # Test listing groups after deletion
        groups = self.iam.list_groups()
        self.assertNotIn("test-group", groups)

    @mock_aws
    def test_add_and_remove_user_from_group(self):
        self.iam.iam = boto3.client("iam", region_name="us-east-1")
        # Setup: create user and group
        self.iam.create_iam_user("test-user")
        self.iam.create_group("test-group")

        # Test adding user to group
        response = self.iam.add_user_to_group("test-user", "test-group")
        self.assertEqual(response, "User 'test-user' added to group 'test-group'.")

        # Test removing user from group
        response = self.iam.remove_user_from_group("test-user", "test-group")
        self.assertEqual(response, "User 'test-user' removed from group 'test-group'.")

    @mock_aws
    def test_create_and_delete_role(self):
        self.iam.iam = boto3.client("iam", region_name="us-east-1")
        # Define assume role policy
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

        # Test role creation
        response = self.iam.create_role("test-role", assume_role_policy)
        self.assertEqual(response, "IAM role 'test-role' created successfully.")

        # Test listing roles
        roles = self.iam.list_roles()
        self.assertIn("test-role", roles)

        # Test role deletion
        response = self.iam.delete_role("test-role")
        self.assertEqual(response, "IAM role 'test-role' deleted successfully.")

        # Test listing roles after deletion
        roles = self.iam.list_roles()
        self.assertNotIn("test-role", roles)

    @mock_aws
    def test_create_and_delete_policy(self):
        self.iam.iam = boto3.client("iam", region_name="us-east-1")
        # Define policy document
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

        # Test policy creation
        response = self.iam.create_policy("test-policy", policy_document)
        self.assertEqual(response, "IAM policy 'test-policy' created successfully.")

        # Test listing policies
        policies = self.iam.list_policies()
        self.assertIn("test-policy", policies)

        # Test policy deletion
        policy_arn = "arn:aws:iam::123456789012:policy/test-policy"
        response = self.iam.delete_policy(policy_arn)
        self.assertEqual(response, f"IAM policy with ARN '{policy_arn}' deleted successfully.")

        # Test listing policies after deletion
        policies = self.iam.list_policies()
        self.assertNotIn("test-policy", policies)

    @mock_aws
    def test_attach_and_detach_user_policy(self):
        self.iam.iam = boto3.client("iam", region_name="us-east-1")
        # Setup: create user and policy
        self.iam.create_iam_user("test-user")
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
        self.iam.create_policy("test-policy", policy_document)
        policy_arn = "arn:aws:iam::123456789012:policy/test-policy"

        # Test attaching policy to user
        response = self.iam.attach_user_policy("test-user", policy_arn)
        self.assertEqual(response, f"Policy '{policy_arn}' attached to user 'test-user'.")

        # Test detaching policy from user
        response = self.iam.detach_user_policy("test-user", policy_arn)
        self.assertEqual(response, f"Policy '{policy_arn}' detached from user 'test-user'.")


if __name__ == "__main__":
    unittest.main()
