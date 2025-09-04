# Rolling_project_part_2
This is the second part of the rolling project 

# AWS Flask Viewer

This project is a simple **Flask web application** packaged in a Docker container.  
It connects to AWS using boto3 and displays basic information about your AWS resources, including:
- EC2 instances
- VPCs
- Load Balancers
- AMIs (owned by your account)

The application runs on **port 5001**.

---

## Prerequisites
- Docker installed locally.
- An AWS IAM user with:
  - **Access Key ID**
  - **Secret Access Key**
- The IAM user should have permissions to list EC2, VPC, and ELB resources (e.g., `AdministratorAccess` for testing).

---

## Build the Docker Image
Clone the repository and build the image:

docker build -t aws-flask .
Run the Container
Run the container while passing your AWS credentials as environment variables:


docker run -d --name aws-flask \
  -p 5001:5001 \
  -e AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY \
  -e AWS_DEFAULT_REGION=us-east-1 \
  aws-flask

## Access the Application
## Open your browser and go to:

http://localhost:5001/

You should see an HTML page with tables listing your AWS resources.

To stop the Container
When finished, stop and remove the container:

docker stop aws-flask
docker rm aws-flask