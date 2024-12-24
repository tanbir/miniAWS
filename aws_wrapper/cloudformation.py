import boto3
import json


class CloudFormation:
    def __init__(self, region="us-east-1"):
        self.cloudformation = boto3.client("cloudformation", region_name=region)

    # Stack Management
    def create_stack(self, stack_name, template_body, parameters=None, capabilities=None):
        """
        Creates a new CloudFormation stack.
        """
        if parameters is None:
            parameters = []
        if capabilities is None:
            capabilities = ["CAPABILITY_NAMED_IAM"]

        self.cloudformation.create_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=capabilities,
        )
        return f"CloudFormation stack '{stack_name}' creation initiated."

    def update_stack(self, stack_name, template_body, parameters=None, capabilities=None):
        """
        Updates an existing CloudFormation stack.
        """
        if parameters is None:
            parameters = []
        if capabilities is None:
            capabilities = ["CAPABILITY_NAMED_IAM"]

        self.cloudformation.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=capabilities,
        )
        return f"CloudFormation stack '{stack_name}' update initiated."

    def delete_stack(self, stack_name):
        """
        Deletes a CloudFormation stack.
        """
        self.cloudformation.delete_stack(StackName=stack_name)
        return f"CloudFormation stack '{stack_name}' deletion initiated."

    def list_stacks(self, status_filter=None):
        """
        Lists all CloudFormation stacks.
        """
        response = self.cloudformation.list_stacks(StackStatusFilter=status_filter or ["CREATE_COMPLETE", "UPDATE_COMPLETE"])
        return [stack["StackName"] for stack in response.get("StackSummaries", [])]

    def describe_stack(self, stack_name):
        """
        Describes a CloudFormation stack.
        """
        response = self.cloudformation.describe_stacks(StackName=stack_name)
        return response["Stacks"][0]

    def describe_stack_resources(self, stack_name):
        """
        Retrieves the resources of a CloudFormation stack.
        """
        response = self.cloudformation.describe_stack_resources(StackName=stack_name)
        return response["StackResources"]

    # Template Management
    def validate_template(self, template_body):
        """
        Validates a CloudFormation template.
        """
        response = self.cloudformation.validate_template(TemplateBody=template_body)
        return response

    def get_template(self, stack_name):
        """
        Retrieves the template body of an existing stack.
        """
        response = self.cloudformation.get_template(StackName=stack_name)
        return response["TemplateBody"]

    # Monitoring Stack Events
    def describe_stack_events(self, stack_name):
        """
        Describes the events of a CloudFormation stack.
        """
        response = self.cloudformation.describe_stack_events(StackName=stack_name)
        return response["StackEvents"]

    # Change Set Management
    def create_change_set(self, stack_name, template_body, change_set_name, parameters=None, capabilities=None):
        """
        Creates a change set for a CloudFormation stack.
        """
        if parameters is None:
            parameters = []
        if capabilities is None:
            capabilities = ["CAPABILITY_NAMED_IAM"]

        self.cloudformation.create_change_set(
            StackName=stack_name,
            TemplateBody=template_body,
            ChangeSetName=change_set_name,
            Parameters=parameters,
            Capabilities=capabilities,
        )
        return f"Change set '{change_set_name}' creation initiated for stack '{stack_name}'."

    def describe_change_set(self, change_set_name, stack_name):
        """
        Describes a change set.
        """
        response = self.cloudformation.describe_change_set(
            ChangeSetName=change_set_name,
            StackName=stack_name,
        )
        return response

    def execute_change_set(self, change_set_name, stack_name):
        """
        Executes a change set for a CloudFormation stack.
        """
        self.cloudformation.execute_change_set(
            ChangeSetName=change_set_name,
            StackName=stack_name,
        )
        return f"Change set '{change_set_name}' executed for stack '{stack_name}'."

    # Stack Policy Management
    def set_stack_policy(self, stack_name, policy_body):
        """
        Sets a stack policy for a CloudFormation stack.
        """
        self.cloudformation.set_stack_policy(
            StackName=stack_name,
            StackPolicyBody=policy_body,
        )
        return f"Stack policy set for stack '{stack_name}'."

    def get_stack_policy(self, stack_name):
        """
        Retrieves the stack policy of a CloudFormation stack.
        """
        response = self.cloudformation.get_stack_policy(StackName=stack_name)
        return response["StackPolicyBody"]
