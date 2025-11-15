import os
import boto3
from flask import Flask, render_template_string, request, Response, g
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from prometheus_flask_exporter import PrometheusMetrics
from time import time

app = Flask(__name__)
metrics = PrometheusMetrics(app)

REQUEST_COUNT = Counter("flask_request_total", "Total request count", ["method", "endpoint", "status"])
REQUEST_LATENCY = Histogram("flask_request_latency_seconds", "Request latency", ["endpoint"])

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION = "us-east-1"

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

ec2_client = session.client("ec2")
elb_client = session.client("elbv2")

@app.before_request
def _start_timer():
    g._start = time()

@app.after_request
def _record_metrics(response):
    try:
        latency = time() - getattr(g, "_start", time())
        endpoint = request.endpoint or "unknown"
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, status=str(response.status_code)).inc()
    finally:
        return response

@app.route("/metrics")
def _metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route("/")
def home():
    instances = ec2_client.describe_instances()
    instance_data = []
    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            instance_data.append({
                "ID": instance["InstanceId"],
                "State": instance["State"]["Name"],
                "Type": instance["InstanceType"],
                "Public IP": instance.get("PublicIpAddress", "N/A")
            })

    vpcs = ec2_client.describe_vpcs()
    lbs = elb_client.describe_load_balancers()
    amis = ec2_client.describe_images(Owners=['self'])

    vpc_data = [{"VPC ID": vpc["VpcId"], "CIDR": vpc["CidrBlock"]} for vpc in vpcs["Vpcs"]]
    lb_data = [{"LB Name": lb["LoadBalancerName"], "DNS Name": lb["DNSName"]} for lb in lbs["LoadBalancers"]]
    ami_data = [{"AMI ID": ami["ImageId"], "Name": ami.get("Name", "N/A")} for ami in amis["Images"]]

    html_template = """
    <html>
    <head><title>AWS Resources</title></head>
    <body>
        <h1>Running EC2 Instances</h1>
        <table border='1'>
            <tr><th>ID</th><th>State</th><th>Type</th><th>Public IP</th></tr>
            {% for instance in instance_data %}
            <tr><td>{{ instance['ID'] }}</td><td>{{ instance['State'] }}</td><td>{{ instance['Type'] }}</td><td>{{ instance['Public IP'] }}</td></tr>
            {% endfor %}
        </table>
        
        <h1>VPCs</h1>
        <table border='1'>
            <tr><th>VPC ID</th><th>CIDR</th></tr>
            {% for vpc in vpc_data %}
            <tr><td>{{ vpc['VPC ID'] }}</td><td>{{ vpc['CIDR'] }}</td></tr>
            {% endfor %}
        </table>
        
        <h1>Load Balancers</h1>
        <table border='1'>
            <tr><th>LB Name</th><th>DNS Name</th></tr>
            {% for lb in lb_data %}
            <tr><td>{{ lb['LB Name'] }}</td><td>{{ lb['DNS Name'] }}</td></tr>
            {% endfor %}
        </table>
        
        <h1>Available AMIs</h1>
        <table border='1'>
            <tr><th>AMI ID</th><th>Name</th></tr>
            {% for ami in ami_data %}
            <tr><td>{{ ami['AMI ID'] }}</td><td>{{ ami['Name'] }}</td></tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """

    return render_template_string(html_template, instance_data=instance_data, vpc_data=vpc_data, lb_data=lb_data, ami_data=ami_data)

if __name__ == "__main__":
    print("Starting Flask on 0.0.0.0:5001")
    app.run(host="0.0.0.0", port=5001, debug=False, use_reloader=False)
