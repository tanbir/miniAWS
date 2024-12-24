import boto3
from aws_wrapper.aws_manager import AWSManager


class Compute(AWSManager):
    def __init__(self, region="us-east-1"):
        super().__init__(region)
        self.ec2 = boto3.client("ec2", region_name=self.region)

    # Instance Operations
    def create_instance(self, instance_type, key_name):
        """
        Launches a new EC2 instance.

        :param instance_type: Instance type (e.g., 't2.micro').
        :param key_name: Key pair name for the instance.
        :return: Instance ID.
        """
        response = self.ec2.run_instances(
            ImageId="ami-12345678",  # Dummy AMI ID for moto
            InstanceType=instance_type,
            MinCount=1,
            MaxCount=1,
            KeyName=key_name,
        )
        return response["Instances"][0]["InstanceId"]

    def stop_instance(self, instance_id):
        """
        Stops a running EC2 instance.

        :param instance_id: ID of the instance to stop.
        :return: Success message.
        """
        self.ec2.stop_instances(InstanceIds=[instance_id])
        return f"Instance '{instance_id}' stopped successfully."

    def start_instance(self, instance_id):
        """
        Starts a stopped EC2 instance.

        :param instance_id: ID of the instance to start.
        :return: Success message.
        """
        self.ec2.start_instances(InstanceIds=[instance_id])
        return f"Instance '{instance_id}' started successfully."

    def terminate_instance(self, instance_id):
        """
        Terminates an EC2 instance.

        :param instance_id: ID of the instance to terminate.
        :return: Success message.
        """
        self.ec2.terminate_instances(InstanceIds=[instance_id])
        return f"Instance '{instance_id}' terminated successfully."

    def describe_instance_status(self, instance_id):
        """
        Describes the status of an EC2 instance.

        :param instance_id: ID of the instance.
        :return: Instance status as a string.
        """
        response = self.ec2.describe_instance_status(InstanceIds=[instance_id])
        if response["InstanceStatuses"]:
            return response["InstanceStatuses"][0]["InstanceState"]["Name"]
        return "No status found for the instance."

    # Key Pair Management
    def create_key_pair(self, key_name):
        """
        Creates a new EC2 key pair.

        :param key_name: Name of the key pair.
        :return: Key material (private key) as a string.
        """
        response = self.ec2.create_key_pair(KeyName=key_name)
        return response["KeyMaterial"]

    # Elastic IP Management
    def allocate_elastic_ip(self):
        """
        Allocates a new Elastic IP.

        :return: Allocation ID and Elastic IP address.
        """
        response = self.ec2.allocate_address(Domain="vpc")
        return {"AllocationId": response["AllocationId"], "PublicIp": response["PublicIp"]}

    def associate_elastic_ip(self, allocation_id, instance_id):
        """
        Associates an Elastic IP with an instance.

        :param allocation_id: Allocation ID of the Elastic IP.
        :param instance_id: ID of the instance to associate the IP with.
        :return: Success message.
        """
        self.ec2.associate_address(AllocationId=allocation_id, InstanceId=instance_id)
        return f"Elastic IP associated with instance '{instance_id}'."

    # Tagging Resources
    def tag_resource(self, resource_id, tags):
        """
        Tags an EC2 resource.

        :param resource_id: ID of the resource to tag.
        :param tags: List of tags (key-value pairs) to assign.
        :return: Success message.
        """
        self.ec2.create_tags(Resources=[resource_id], Tags=tags)
        return f"Tags {tags} added to resource '{resource_id}'."

    # Volume Management
    def create_volume(self, availability_zone, size):
        """
        Creates a new EBS volume.

        :param availability_zone: The availability zone to create the volume in.
        :param size: Size of the volume in GB.
        :return: Volume ID.
        """
        response = self.ec2.create_volume(AvailabilityZone=availability_zone, Size=size)
        return response["VolumeId"]

    def attach_volume(self, volume_id, instance_id, device_name):
        """
        Attaches an EBS volume to an instance.

        :param volume_id: ID of the volume.
        :param instance_id: ID of the instance.
        :param device_name: Device name for the volume attachment (e.g., /dev/xvdf).
        :return: Success message.
        """
        self.ec2.attach_volume(VolumeId=volume_id, InstanceId=instance_id, Device=device_name)
        return f"Volume '{volume_id}' attached to instance '{instance_id}'."

    # Monitoring
    def enable_monitoring(self, instance_id):
        """
        Enables detailed monitoring for an instance.

        :param instance_id: ID of the instance.
        :return: Success message.
        """
        self.ec2.monitor_instances(InstanceIds=[instance_id])
        return f"Monitoring enabled for instance '{instance_id}'."

    def disable_monitoring(self, instance_id):
        """
        Disables detailed monitoring for an instance.

        :param instance_id: ID of the instance.
        :return: Success message.
        """
        self.ec2.unmonitor_instances(InstanceIds=[instance_id])
        return f"Monitoring disabled for instance '{instance_id}'."
