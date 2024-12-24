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

    def list_metrics(self, namespace=None):
        response = self.cloudwatch.list_metrics(Namespace=namespace)
        metrics = [
            {
                "Namespace": metric["Namespace"],
                "MetricName": metric["MetricName"],
                "Dimensions": metric.get("Dimensions", []),
            }
            for metric in response.get("Metrics", [])
        ]
        return metrics

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
    def create_alarm(
        self,
        alarm_name,
        metric_name,
        namespace,
        threshold,
        comparison_operator,
        evaluation_periods,
        period,
        statistic,
        dimensions=None,
    ):
        """
        Create a CloudWatch alarm.
        :param alarm_name: Name of the alarm.
        :param metric_name: Metric to monitor.
        :param namespace: Namespace of the metric.
        :param threshold: Threshold value for the alarm.
        :param comparison_operator: Operator for comparing metric values.
        :param evaluation_periods: Number of periods to evaluate.
        :param period: Period in seconds for the metric.
        :param statistic: Statistic to apply (e.g., "Average").
        :param dimensions: Dimensions for the metric (optional).
        :return: Success message.
        """
        self.cloudwatch.put_metric_alarm(
            AlarmName=alarm_name,
            MetricName=metric_name,
            Namespace=namespace,
            Threshold=threshold,
            ComparisonOperator=comparison_operator,
            EvaluationPeriods=evaluation_periods,
            Period=period,
            Statistic=statistic,
            Dimensions=dimensions or [],
        )
        return f"Alarm '{alarm_name}' created successfully."


    def delete_alarm(self, alarm_name):
        """
        Deletes a CloudWatch alarm.
        """
        self.cloudwatch.delete_alarms(AlarmNames=[alarm_name])
        return f"Alarm '{alarm_name}' deleted successfully."

    def list_alarms(self):
        """
        List all CloudWatch alarms.
        :return: List of dictionaries containing alarm details.
        """
        response = self.cloudwatch.describe_alarms()
        return response.get("MetricAlarms", [])

    # Logs Management
    def create_log_group(self, log_group_name):
        """
        Creates a CloudWatch log group.
        """
        self.logs.create_log_group(logGroupName=log_group_name)
        return f"Log group '{log_group_name}' created successfully."

    def list_log_groups(self):
        response = self.logs.describe_log_groups()
        return [log_group["logGroupName"] for log_group in response.get("logGroups", [])]

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
