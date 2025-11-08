# 🏗️ Environment: `env-prod`

## Overview
This branch represents the **production deployment environment** for the project.  
It is automatically updated by the Jenkins pipeline after each successful build and push of the Docker image `docker.io/cheeza42/dockerizing-project`.  
ArgoCD continuously monitors this branch and synchronizes any manifest changes to the production Kubernetes cluster defined for **Rolling_project_part_2**.

---

## 🔄 Integration with `main`
- The `main` branch contains the **application source code**, `Jenkinsfile`, `Dockerfile`, and Helm chart templates.
- The `env-prod` branch holds **deployment manifests** and **environment-specific values** used for the production environment.
- When Jenkins completes a successful build, it updates the image tag in `env-prod` (e.g., in `charts/app/values.yaml`).
- ArgoCD automatically detects this commit and performs **auto-sync**, deploying the updated image to the production cluster.

---

## ⚙️ Automated Flow
1. Developer merges or pushes new code into `main`.
2. Jenkins pipeline triggers automatically.
3. Jenkins builds the new Docker image → tags it → pushes to Docker Hub (`docker.io/cheeza42/dockerizing-project`).
4. Jenkins commits and pushes the updated image tag to the `env-prod` branch.
5. ArgoCD detects the change in Git and applies the new manifests to the cluster.

This flow ensures that production is **GitOps-based**, **fully traceable**, and **automated from build to deploy**.

---

## 🧩 Branch Structure
```
env-prod/
├── charts/
│   └── app/
│       ├── values.yaml
│       ├── deployment.yaml
│       ├── service.yaml
│       └── ingress.yaml
└── README.md
```

---

## 🚀 Manual Operations
If needed, you can manually trigger ArgoCD operations:
```bash
argocd app refresh rolling-project
argocd app sync rolling-project
```

---

## ✅ Best Practices
- Do **not** edit manifests directly in the ArgoCD UI — always via Git commits.  
- Keep this branch **protected**; allow updates only through Jenkins or reviewed PRs.  
- Use **unique image tags** for each build (timestamp or commit SHA) to ensure a valid diff.  
- Avoid pushing to `env-prod` manually; Jenkins should manage updates to guarantee GitOps integrity.

---

## 🧠 Summary
`env-prod` serves as the **single source of truth** for your production environment.  
It connects the CI/CD pipeline (Jenkins + Docker Hub) with GitOps delivery (ArgoCD), ensuring every change is versioned, reproducible, and automatically deployed.
