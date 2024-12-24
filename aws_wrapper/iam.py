import boto3


class IAM:
    def __init__(self, region="us-east-1"):
        self.iam = boto3.client("iam", region_name=region)

    # User Management
    def create_iam_user(self, user_name):
        """
        Creates a new IAM user.
        """
        response = self.iam.create_user(UserName=user_name)
        return f"IAM user '{user_name}' created successfully."

    def delete_iam_user(self, user_name):
        """
        Deletes an IAM user.
        """
        self.iam.delete_user(UserName=user_name)
        return f"IAM user '{user_name}' deleted successfully."

    def list_iam_users(self):
        """
        Lists all IAM users.
        """
        response = self.iam.list_users()
        return [user["UserName"] for user in response.get("Users", [])]

    # Group Management
    def create_group(self, group_name):
        """
        Creates a new IAM group.
        """
        response = self.iam.create_group(GroupName=group_name)
        return f"IAM group '{group_name}' created successfully."

    def delete_group(self, group_name):
        """
        Deletes an IAM group.
        """
        self.iam.delete_group(GroupName=group_name)
        return f"IAM group '{group_name}' deleted successfully."

    def list_groups(self):
        """
        Lists all IAM groups.
        """
        response = self.iam.list_groups()
        return [group["GroupName"] for group in response.get("Groups", [])]

    def add_user_to_group(self, user_name, group_name):
        """
        Adds a user to a group.
        """
        self.iam.add_user_to_group(UserName=user_name, GroupName=group_name)
        return f"User '{user_name}' added to group '{group_name}'."

    def remove_user_from_group(self, user_name, group_name):
        """
        Removes a user from a group.
        """
        self.iam.remove_user_from_group(UserName=user_name, GroupName=group_name)
        return f"User '{user_name}' removed from group '{group_name}'."

    # Role Management
    def create_role(self, role_name, assume_role_policy_document):
        """
        Creates a new IAM role.
        """
        response = self.iam.create_role(
            RoleName=role_name, AssumeRolePolicyDocument=assume_role_policy_document
        )
        return f"IAM role '{role_name}' created successfully."

    def delete_role(self, role_name):
        """
        Deletes an IAM role.
        """
        self.iam.delete_role(RoleName=role_name)
        return f"IAM role '{role_name}' deleted successfully."

    def list_roles(self):
        """
        Lists all IAM roles.
        """
        response = self.iam.list_roles()
        return [role["RoleName"] for role in response.get("Roles", [])]

    # Policy Management
    def create_policy(self, policy_name, policy_document):
        """
        Creates a new IAM policy.
        """
        response = self.iam.create_policy(
            PolicyName=policy_name, PolicyDocument=policy_document
        )
        return f"IAM policy '{policy_name}' created successfully."

    def delete_policy(self, policy_arn):
        """
        Deletes an IAM policy.
        """
        self.iam.delete_policy(PolicyArn=policy_arn)
        return f"IAM policy with ARN '{policy_arn}' deleted successfully."

    def list_policies(self, scope="All"):
        """
        Lists all IAM policies.
        """
        response = self.iam.list_policies(Scope=scope)
        return [policy["PolicyName"] for policy in response.get("Policies", [])]

    def attach_user_policy(self, user_name, policy_arn):
        """
        Attaches a policy to an IAM user.
        """
        self.iam.attach_user_policy(UserName=user_name, PolicyArn=policy_arn)
        return f"Policy '{policy_arn}' attached to user '{user_name}'."

    def detach_user_policy(self, user_name, policy_arn):
        """
        Detaches a policy from an IAM user.
        """
        self.iam.detach_user_policy(UserName=user_name, PolicyArn=policy_arn)
        return f"Policy '{policy_arn}' detached from user '{user_name}'."

    def attach_role_policy(self, role_name, policy_arn):
        """
        Attaches a policy to an IAM role.
        """
        self.iam.attach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        return f"Policy '{policy_arn}' attached to role '{role_name}'."

    def detach_role_policy(self, role_name, policy_arn):
        """
        Detaches a policy from an IAM role.
        """
        self.iam.detach_role_policy(RoleName=role_name, PolicyArn=policy_arn)
        return f"Policy '{policy_arn}' detached from role '{role_name}'."

    def attach_group_policy(self, group_name, policy_arn):
        """
        Attaches a policy to an IAM group.
        """
        self.iam.attach_group_policy(GroupName=group_name, PolicyArn=policy_arn)
        return f"Policy '{policy_arn}' attached to group '{group_name}'."

    def detach_group_policy(self, group_name, policy_arn):
        """
        Detaches a policy from an IAM group.
        """
        self.iam.detach_group_policy(GroupName=group_name, PolicyArn=policy_arn)
        return f"Policy '{policy_arn}' detached from group '{group_name}'."
