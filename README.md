# Rolling_project_part_2
This is the second part of the rolling project 

# AWS Flask Viewer

This project is a simple Flask web application packaged in a Docker container.  
It uses boto3 to connect to AWS and displays the following resources in an HTML page:
- EC2 instances
- VPCs
- Load Balancers
- AMIs

The application runs on **port 5001**.

## Prerequisites
- Docker installed
- AWS IAM user with:
  - Access Key ID
  - Secret Access Key
- Permissions to list EC2, VPC, ELB, and AMI resources (for testing, `AdministratorAccess` is sufficient)

## Build the Docker Image
```bash
docker build -t aws-flask .
```

## Run the Container
```bash
docker run -d --name aws-flask \
  -p 5001:5001 \
  -e AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY \
  -e AWS_DEFAULT_REGION=eu-west-1 \
  aws-flask
```

## Access the Application
Open your browser at:

```
http://localhost:5001/
```

You will see an HTML page displaying your AWS resources.

## Stop the Container
```bash
docker stop aws-flask
docker rm aws-flask
```

