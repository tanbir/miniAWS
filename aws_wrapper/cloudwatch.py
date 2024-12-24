import boto3
import datetime


class CloudWatch:
    def __init__(self, region="us-east-1"):
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)
        self.logs = boto3.client("logs", region_name=region)

    # Metrics Management
    def put_metric_data(self, namespace, metric_name, value, unit="None", dimensions=None):
        """
        Publishes a custom metric to CloudWatch.
        """
        data = {
            "MetricName": metric_name,
            "Value": value,
            "Unit": unit
        }
        if dimensions:
            data["Dimensions"] = dimensions

        self.cloudwatch.put_metric_data(
            Namespace=namespace,
            MetricData=[data]
        )
        return f"Metric '{metric_name}' published to namespace '{namespace}'."

    def get_metric_statistics(self, namespace, metric_name, start_time, end_time, period, statistics, dimensions=None):
        """
        Retrieves metric statistics.
        """
        params = {
            "Namespace": namespace,
            "MetricName": metric_name,
            "StartTime": start_time,
            "EndTime": end_time,
            "Period": period,
            "Statistics": statistics,
        }
        if dimensions:
            params["Dimensions"] = dimensions

        response = self.cloudwatch.get_metric_statistics(**params)
        return response.get("Datapoints", [])

    # Alarms Management
    def create_alarm(self, alarm_name, metric_name, namespace, comparison_operator, threshold, evaluation_periods, period, statistic, actions=None):
        """
        Creates a CloudWatch alarm.
        """
        params = {
            "AlarmName": alarm_name,
            "MetricName": metric_name,
            "Namespace": namespace,
            "ComparisonOperator": comparison_operator,
            "Threshold": threshold,
            "EvaluationPeriods": evaluation_periods,
            "Period": period,
            "Statistic": statistic,
        }
        if actions:
            params["AlarmActions"] = actions

        self.cloudwatch.put_metric_alarm(**params)
        return f"Alarm '{alarm_name}' created successfully."

    def delete_alarm(self, alarm_name):
        """
        Deletes a CloudWatch alarm.
        """
        self.cloudwatch.delete_alarms(AlarmNames=[alarm_name])
        return f"Alarm '{alarm_name}' deleted successfully."

    def list_alarms(self):
        """
        Lists all CloudWatch alarms.
        """
        response = self.cloudwatch.describe_alarms()
        return [alarm["AlarmName"] for alarm in response.get("MetricAlarms", [])]

    # Logs Management
    def create_log_group(self, log_group_name):
        """
        Creates a CloudWatch log group.
        """
        self.logs.create_log_group(logGroupName=log_group_name)
        return f"Log group '{log_group_name}' created successfully."

    def delete_log_group(self, log_group_name):
        """
        Deletes a CloudWatch log group.
        """
        self.logs.delete_log_group(logGroupName=log_group_name)
        return f"Log group '{log_group_name}' deleted successfully."

    def create_log_stream(self, log_group_name, log_stream_name):
        """
        Creates a log stream within a log group.
        """
        self.logs.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        return f"Log stream '{log_stream_name}' created in log group '{log_group_name}'."

    def put_log_events(self, log_group_name, log_stream_name, messages):
        """
        Publishes log events to a log stream.
        """
        events = [{"timestamp": int(datetime.datetime.now().timestamp() * 1000), "message": msg} for msg in messages]
        response = self.logs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=events
        )
        return f"Published {len(events)} log events to stream '{log_stream_name}'."

    def get_log_events(self, log_group_name, log_stream_name, start_time=None, end_time=None):
        """
        Retrieves log events from a log stream.
        """
        params = {
            "logGroupName": log_group_name,
            "logStreamName": log_stream_name,
        }
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time

        response = self.logs.get_log_events(**params)
        return response.get("events", [])

    # Dashboard Management
    def create_dashboard(self, dashboard_name, dashboard_body):
        """
        Creates a CloudWatch dashboard.
        """
        self.cloudwatch.put_dashboard(
            DashboardName=dashboard_name,
            DashboardBody=dashboard_body
        )
        return f"Dashboard '{dashboard_name}' created successfully."

    def delete_dashboard(self, dashboard_name):
        """
        Deletes a CloudWatch dashboard.
        """
        self.cloudwatch.delete_dashboards(DashboardNames=[dashboard_name])
        return f"Dashboard '{dashboard_name}' deleted successfully."

    def get_dashboard(self, dashboard_name):
        """
        Retrieves a CloudWatch dashboard.
        """
        response = self.cloudwatch.get_dashboard(DashboardName=dashboard_name)
        return response.get("DashboardBody", "")

    def list_dashboards(self):
        """
        Lists all CloudWatch dashboards.
        """
        response = self.cloudwatch.list_dashboards()
        return [dashboard["DashboardName"] for dashboard in response.get("DashboardEntries", [])]
