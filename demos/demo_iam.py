import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_wrapper.iam import IAM
from moto import mock_aws

@mock_aws
def main():
    iam = IAM(region="us-east-1")

    # **User Management**
    print("\n--- User Management ---")
    print(iam.create_iam_user("test-user"))
    print("All users:", iam.list_iam_users())
    print(iam.delete_iam_user("test-user"))
    print("Users after deletion:", iam.list_iam_users())

    # **Group Management**
    print("\n--- Group Management ---")
    print(iam.create_group("test-group"))
    print("All groups:", iam.list_groups())

    # Recreate the user for group testing
    print(iam.create_iam_user("test-user"))
    print(iam.add_user_to_group("test-user", "test-group"))
    print(iam.remove_user_from_group("test-user", "test-group"))
    print(iam.delete_iam_user("test-user"))
    print(iam.delete_group("test-group"))
    print("Groups after deletion:", iam.list_groups())

    # **Role Management**
    print("\n--- Role Management ---")
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
    print(iam.create_role("test-role", assume_role_policy))
    print("All roles:", iam.list_roles())
    print(iam.delete_role("test-role"))
    print("Roles after deletion:", iam.list_roles())

    # **Policy Management**
    print("\n--- Policy Management ---")

    # Recreate the user for policy testing
    print(iam.create_iam_user("test-user"))

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
    print(f"Policy created with ARN: {policy_arn}")
    print("All policies:", iam.list_policies())
    print(iam.attach_user_policy("test-user", policy_arn))
    print(iam.detach_user_policy("test-user", policy_arn))
    print(iam.delete_iam_user("test-user"))
    print("Policies after testing user attachment:", iam.list_policies())

    # **Policy and Role Attachments**
    print("\n--- Attach Policies to Role ---")
    # Ensure the role and policy exist
    print(iam.create_role("test-role", assume_role_policy))
    print(f"Reusing policy with ARN: {policy_arn}")
    print(iam.attach_role_policy("test-role", policy_arn))
    print(iam.detach_role_policy("test-role", policy_arn))
    print(iam.delete_role("test-role"))

    # **Group Policy Attachments**
    print("\n--- Attach Policies to Group ---")
    print(iam.create_group("test-group"))
    print(f"Reusing policy with ARN: {policy_arn}")
    print(iam.attach_group_policy("test-group", policy_arn))
    print(iam.detach_group_policy("test-group", policy_arn))
    print(iam.delete_group("test-group"))

    # Cleanup the policy after all tests
    print(iam.delete_policy(policy_arn))
    print("Policies after deletion:", iam.list_policies())


if __name__ == "__main__":
    main()
