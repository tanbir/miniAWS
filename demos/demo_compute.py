import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aws_wrapper.compute import Compute
from moto import mock_aws

@mock_aws
def main():
    # Initialize Compute wrapper
    compute = Compute(region="us-east-1")

    # Define key parameters
    instance_type = "t2.micro"
    key_name = "demo-key"
    availability_zone = "us-east-1a"
    volume_size = 10

    print("\n--- Key Pair Management ---")
    # Create a key pair
    key_material = compute.create_key_pair(key_name)
    print(f"Key pair '{key_name}' created successfully. Private key:\n{key_material}")

    print("\n--- Instance Operations ---")
    # Launch an instance
    instance_id = compute.create_instance(instance_type, key_name)
    print(f"Instance '{instance_id}' launched successfully.")

    # Describe instance status
    status = compute.describe_instance_status(instance_id)
    print(f"Instance '{instance_id}' status: {status}")

    # Enable monitoring (Mocked or commented due to moto limitations)
    try:
        print(compute.enable_monitoring(instance_id))
    except NotImplementedError as e:
        print(f"Skipping monitoring enablement: {e}")

    # Stop the instance
    print(compute.stop_instance(instance_id))

    # Start the instance
    print(compute.start_instance(instance_id))

    # Disable monitoring (Mocked or commented due to moto limitations)
    try:
        print(compute.disable_monitoring(instance_id))
    except NotImplementedError as e:
        print(f"Skipping monitoring disablement: {e}")

    # Terminate the instance
    print(compute.terminate_instance(instance_id))

    print("\n--- Elastic IP Management ---")
    # Allocate an Elastic IP
    elastic_ip = compute.allocate_elastic_ip()
    allocation_id = elastic_ip["AllocationId"]
    public_ip = elastic_ip["PublicIp"]
    print(f"Elastic IP allocated: {public_ip} (Allocation ID: {allocation_id})")

    print("\n--- Resource Tagging ---")
    # Tag the Elastic IP
    tags = [{"Key": "Name", "Value": "DemoElasticIP"}]
    print(compute.tag_resource(allocation_id, tags))

    print("\n--- Volume Management ---")
    # Create a new EBS volume
    volume_id = compute.create_volume(availability_zone, volume_size)
    print(f"Volume '{volume_id}' created successfully.")

    print("\nDemo complete!")


if __name__ == "__main__":
    main()
