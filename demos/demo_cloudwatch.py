import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from moto import mock_aws
from aws_wrapper.cloudwatch import CloudWatch


@mock_aws
def main():
    cw = CloudWatch(region="us-east-1")

    # **Log Group Management**
    print("\n--- Log Group Management ---")
    print(cw.create_log_group("test-log-group"))
    print("Log groups:", cw.list_log_groups())
    print(cw.delete_log_group("test-log-group"))
    print("Log groups after deletion:", cw.list_log_groups())

    # **Metric Management**
    print("\n--- Metric Management ---")
    namespace = "MyNamespace"
    metric_name = "MyMetric"
    dimensions = [{"Name": "InstanceId", "Value": "i-12345678"}]
    print(cw.put_metric_data(namespace, metric_name, value=100, dimensions=dimensions))
    metrics = cw.list_metrics(namespace=namespace)
    print("Metrics:", metrics)

    # **Alarm Management**
    print("\n--- Alarm Management ---")
    alarm_name = "HighCPUUtilization"
    print(cw.create_alarm(
        alarm_name=alarm_name,
        metric_name=metric_name,
        namespace=namespace,
        threshold=80,
        comparison_operator="GreaterThanThreshold",
        evaluation_periods=1,
        period=60,
        statistic="Average",
        dimensions=dimensions,
    ))
    alarms = cw.list_alarms()
    print("Alarms:", alarms)
    print(cw.delete_alarm(alarm_name))
    print("Alarms after deletion:", cw.list_alarms())

    # **Dashboard Management**
    print("\n--- Dashboard Management ---")
    dashboard_name = "TestDashboard"
    dashboard_body = """{
        "widgets": [
            {
                "type": "metric",
                "x": 0,
                "y": 0,
                "width": 6,
                "height": 6,
                "properties": {
                    "metrics": [
                        ["MyNamespace", "MyMetric"]
                    ],
                    "period": 300,
                    "stat": "Average",
                    "region": "us-east-1",
                    "title": "MyMetric Dashboard"
                }
            }
        ]
    }"""
    print(cw.create_dashboard(dashboard_name, dashboard_body))
    print("Dashboards:", cw.list_dashboards())
    print(cw.delete_dashboard(dashboard_name))
    print("Dashboards after deletion:", cw.list_dashboards())


if __name__ == "__main__":
    main()
