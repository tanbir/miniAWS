import unittest
from moto import mock_aws
import boto3
from aws_wrapper.cloudwatch import CloudWatch
import os

class TestCloudWatch(unittest.TestCase):
    def setUp(self):
        # Set mock AWS credentials
        os.environ["AWS_ACCESS_KEY_ID"] = "mock_access_key"
        os.environ["AWS_SECRET_ACCESS_KEY"] = "mock_secret_key"
        os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
        # Initialize the CloudWatch wrapper
        self.cloudwatch = CloudWatch(region="us-east-1")

    @mock_aws
    def test_put_and_get_metric_data(self):
        self.cloudwatch.cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

        # Test putting metric data
        response = self.cloudwatch.put_metric_data(
            namespace="TestNamespace",
            metric_name="TestMetric",
            value=100,
            unit="Count",
        )
        self.assertEqual(response, "Metric 'TestMetric' published to namespace 'TestNamespace'.")

        # Test getting metric statistics
        datapoints = self.cloudwatch.get_metric_statistics(
            namespace="TestNamespace",
            metric_name="TestMetric",
            start_time="2023-01-01T00:00:00Z",
            end_time="2023-01-02T00:00:00Z",
            period=60,
            statistics=["Average"],
        )
        self.assertIsInstance(datapoints, list)

    @mock_aws
    def test_create_and_delete_alarm(self):
        self.cloudwatch.cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

        # Test creating an alarm
        response = self.cloudwatch.create_alarm(
            alarm_name="TestAlarm",
            metric_name="TestMetric",
            namespace="TestNamespace",
            comparison_operator="GreaterThanThreshold",
            threshold=50,
            evaluation_periods=1,
            period=300,
            statistic="Average",
        )
        self.assertEqual(response, "Alarm 'TestAlarm' created successfully.")

        # Test listing alarms
        alarms = self.cloudwatch.list_alarms()
        self.assertIn("TestAlarm", alarms)

        # Test deleting an alarm
        response = self.cloudwatch.delete_alarm("TestAlarm")
        self.assertEqual(response, "Alarm 'TestAlarm' deleted successfully.")

    @mock_aws
    def test_create_and_delete_log_group(self):
        self.cloudwatch.logs = boto3.client("logs", region_name="us-east-1")

        # Test creating a log group
        response = self.cloudwatch.create_log_group("TestLogGroup")
        self.assertEqual(response, "Log group 'TestLogGroup' created successfully.")

        # Test deleting a log group
        response = self.cloudwatch.delete_log_group("TestLogGroup")
        self.assertEqual(response, "Log group 'TestLogGroup' deleted successfully.")

    @mock_aws
    def test_create_log_stream_and_put_logs(self):
        self.cloudwatch.logs = boto3.client("logs", region_name="us-east-1")

        # Setup: create log group
        self.cloudwatch.create_log_group("TestLogGroup")

        # Test creating a log stream
        response = self.cloudwatch.create_log_stream("TestLogGroup", "TestLogStream")
        self.assertEqual(response, "Log stream 'TestLogStream' created in log group 'TestLogGroup'.")

        # Test putting log events
        response = self.cloudwatch.put_log_events(
            log_group_name="TestLogGroup",
            log_stream_name="TestLogStream",
            messages=["Test log message 1", "Test log message 2"],
        )
        self.assertEqual(response, "Published 2 log events to stream 'TestLogStream'.")

    @mock_aws
    def test_get_log_events(self):
        self.cloudwatch.logs = boto3.client("logs", region_name="us-east-1")

        # Setup: create log group and log stream
        self.cloudwatch.create_log_group("TestLogGroup")
        self.cloudwatch.create_log_stream("TestLogGroup", "TestLogStream")
        self.cloudwatch.put_log_events(
            log_group_name="TestLogGroup",
            log_stream_name="TestLogStream",
            messages=["Test log message"],
        )

        # Test getting log events
        events = self.cloudwatch.get_log_events("TestLogGroup", "TestLogStream")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["message"], "Test log message")

    @mock_aws
    def test_create_and_delete_dashboard(self):
        self.cloudwatch.cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")

        # Define dashboard body
        dashboard_body = """{
            "widgets": [
                {
                    "type": "metric",
                    "properties": {
                        "metrics": [
                            ["AWS/EC2", "CPUUtilization"]
                        ],
                        "title": "CPU Utilization"
                    }
                }
            ]
        }"""

        # Test creating a dashboard
        response = self.cloudwatch.create_dashboard("TestDashboard", dashboard_body)
        self.assertEqual(response, "Dashboard 'TestDashboard' created successfully.")

        # Test listing dashboards
        dashboards = self.cloudwatch.list_dashboards()
        self.assertIn("TestDashboard", dashboards)

        # Test deleting a dashboard
        response = self.cloudwatch.delete_dashboard("TestDashboard")
        self.assertEqual(response, "Dashboard 'TestDashboard' deleted successfully.")

    @mock_aws
    def test_list_log_groups(self):
        self.cloudwatch.cloudwatch_logs = boto3.client("logs", region_name="us-east-1")
        self.cloudwatch.create_log_group("test-log-group")
        log_groups = self.cloudwatch.list_log_groups()
        self.assertIn("test-log-group", log_groups)

    @mock_aws
    def test_list_metrics(self):
        self.cloudwatch.cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
        namespace = "TestNamespace"
        metric_name = "TestMetric"
        dimensions = [{"Name": "InstanceId", "Value": "i-12345678"}]
        self.cloudwatch.put_metric_data(namespace, metric_name, 100, dimensions=dimensions)
        metrics = self.cloudwatch.list_metrics(namespace=namespace)
        self.assertTrue(any(metric["MetricName"] == metric_name for metric in metrics))

    @mock_aws
    def test_create_and_delete_alarm(self):
        self.cloudwatch.cloudwatch = boto3.client("cloudwatch", region_name="us-east-1")
        namespace = "TestNamespace"
        metric_name = "TestMetric"
        alarm_name = "TestAlarm"
        self.cloudwatch.create_alarm(
            alarm_name=alarm_name,
            metric_name=metric_name,
            namespace=namespace,
            threshold=80,
            comparison_operator="GreaterThanThreshold",
            evaluation_periods=1,
            period=60,
            statistic="Average",
            dimensions=[{"Name": "InstanceId", "Value": "i-12345678"}],
        )
        alarms = self.cloudwatch.list_alarms()
        self.assertTrue(any(alarm["AlarmName"] == alarm_name for alarm in alarms))
        self.cloudwatch.delete_alarm(alarm_name)