# 🚀 Rolling_project_part_2
This is the second part of the rolling project  

---

# 🌐 AWS Flask Viewer
A simple Flask web application packaged in a Docker container.  
It uses **boto3** to connect to AWS and displays the following resources in an HTML page:
- 🖥️ EC2 instances  
- 🌉 VPCs  
- ⚖️ Load Balancers  
- 📸 AMIs  

The application runs on **port 5001**.

---

## ✅ Prerequisites
- 🐳 Docker installed  
- 🔑 AWS IAM user with:  
  - Access Key ID  
  - Secret Access Key  
- 👮 Permissions to list EC2, VPC, ELB, and AMI resources (for testing, `AdministratorAccess` is sufficient)  

---

## 🛠️ Instructions

### 🛠️ Build Locally
```bash
docker build -t project-flask .
```
## 📦 Pull from Docker Hub
```bash
docker pull cheeza42/dockerizing-project:v1
```
**View on Docker Hub:**
 https://hub.docker.com/r/cheeza42/dockerizing-project


## ▶️ Run the Container on AWS
 ```bash
docker run -d --name project-flask \
  -p 5001:5001 \
  -e AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY \
  -e AWS_DEFAULT_REGION=eu-west-1 \
  cheeza42/dockerizing-project:v1
 ```
## 🌍 Access the Application
Open your browser at:
👉 http://localhost:5001/


## 🛑 Stop and Remove the Container
```bash
docker stop project-flask
docker rm project-flask
```