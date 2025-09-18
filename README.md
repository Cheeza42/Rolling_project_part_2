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

## ⎈ Deploy on Kubernetes with Helm

This repo also includes a Helm chart (chart/helm_project) to deploy the app to Kubernetes.

## 📋 Prerequisites

Kubernetes cluster with kubectl configured

Helm v3+

NGINX Ingress Controller (required because ingress.enabled: true in values.yaml)

## 🚀 Install
```bash
helm install aws-viewer ./chart/helm_project
kubectl get pods,svc,ingress
```

## 🌐 Access the app
Ingress (enabled)

According to values.yaml:

- ingress.enabled: true

- ingress.ingressClassName: nginx

- ingress.host: awsviewer.com

So the app will be available at:

http://awsviewer.com/


## ⚠️ DNS for awsviewer.com must resolve to your Ingress controller’s IP.
For local testing (e.g., minikube), add an entry in /etc/hosts:
<INGRESS-IP> awsviewer.com

## Fallback: ClusterIP (port-forward)

If Ingress is not working, the Service is ClusterIP on port 80 → targetPort 5001.
You can forward locally:
```bash
kubectl port-forward svc/aws-viewer 8080:80
```
# Then open http://localhost:8080/

## 🔄 Upgrade / Uninstall
```bash
helm upgrade aws-viewer ./chart/helm_project -f chart/helm_project/values.yaml
helm uninstall aws-viewer
```
## 📑 Chart details

Replicas: 2

Image: cheeza42/dockerizing-project:v1

Service: ClusterIP (port 80 → container port 5001)

Ingress: NGINX, host awsviewer.com

AWS credentials: passed as environment variables

✅ Recommendation: In production, store AWS credentials in a Kubernetes Secret and reference them from the Deployment.