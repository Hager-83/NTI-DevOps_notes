# DevOps Lab Setup

This README contains the main commands and steps used to start and check the DevOps lab environment.

## 1. Linux

### Check system information

```bash
lsb_release -a
uname -a
```

### Check memory

```bash
free -h
```

### Check disk space

```bash
df -h
```

### Check running processes

```bash
top
```

or:

```bash
htop
```

### Check network

```bash
ip a
```

Check network neighbors:

```bash
ip neigh
```

Test internet connection:

```bash
ping -c 4 google.com
```

### Git

Check Git:

```bash
git --version
```

Check repository status:

```bash
git status
```

Add files:

```bash
git add .
```

Commit:

```bash
git commit -m "message"
```

Push:

```bash
git push
```

Pull latest changes:

```bash
git pull
```

---

# 2. Docker

## Check Docker

```bash
docker --version
```

Check Docker service:

```bash
sudo systemctl status docker
```

Start Docker:

```bash
sudo systemctl start docker
```

Enable Docker at startup:

```bash
sudo systemctl enable docker
```

## Check containers

Running containers:

```bash
sudo docker ps
```

All containers:

```bash
sudo docker ps -a
```

## Start an existing container

If the container already exists:

```bash
sudo docker start <container_name>
```

Example:

```bash
sudo docker start jenkins
```

Check:

```bash
sudo docker ps
```

## Stop a container

```bash
sudo docker stop <container_name>
```

## Restart a container

```bash
sudo docker restart <container_name>
```

## View logs

```bash
sudo docker logs <container_name>
```

Live logs:

```bash
sudo docker logs -f <container_name>
```

## Remove a container

```bash
sudo docker rm <container_name>
```

Force remove:

```bash
sudo docker rm -f <container_name>
```

## Docker images

List images:

```bash
sudo docker images
```

Pull an image:

```bash
sudo docker pull <image>
```

Example:

```bash
sudo docker pull jenkins/jenkins:lts
```

---

# 3. Kubernetes

## Check kubectl

```bash
kubectl version --client
```

## Check Minikube

```bash
minikube version
```

Check status:

```bash
minikube status
```

## Start Minikube

```bash
minikube start
```

Check status again:

```bash
minikube status
```

Expected:

```text
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

## Check Kubernetes nodes

```bash
kubectl get nodes
```

## Check pods

```bash
kubectl get pods
```

Check pods in all namespaces:

```bash
kubectl get pods -A
```

## Check services

```bash
kubectl get svc
```

## Check deployments

```bash
kubectl get deployments
```

## Apply a YAML file

```bash
kubectl apply -f deployment.yaml
```

## Delete a YAML deployment

```bash
kubectl delete -f deployment.yaml
```

## Describe a resource

```bash
kubectl describe pod <pod-name>
```

## Check pod logs

```bash
kubectl logs <pod-name>
```

## Stop Minikube

```bash
minikube stop
```

Start it again:

```bash
minikube start
```

---

# 4. Terraform

## Check Terraform

```bash
terraform version
```

## Go to the Terraform project

Example:

```bash
cd ~/terraform/floci-lab
```

## Initialize Terraform

Run this first when starting a new Terraform project:

```bash
terraform init
```

## Check configuration

```bash
terraform validate
```

## Format Terraform files

```bash
terraform fmt
```

## See what Terraform will create

```bash
terraform plan
```

## Create the infrastructure

```bash
terraform apply
```

Confirm with:

```text
yes
```

## Destroy the infrastructure

```bash
terraform destroy
```

Confirm with:

```text
yes
```

## Check Terraform state

```bash
terraform show
```

---

# 5. Floci

Floci is used as a local AWS-compatible environment for the Terraform lab.

## Check Floci containers

```bash
sudo docker ps
```

The main Floci services should be running.

Example:

```text
floci
floci-ui
```

## Floci endpoints

AWS-compatible API:

```text
http://localhost:4566
```

Floci UI:

```text
http://localhost:4500
```

## If Floci is stopped

Start the existing containers:

```bash
sudo docker start floci
sudo docker start floci-ui
```

Check:

```bash
sudo docker ps
```

---

# 6. AWS CLI

## Check AWS CLI

```bash
aws --version
```

## Configure AWS CLI

```bash
aws configure
```

For a local Floci environment, the endpoint can be specified when running AWS commands.

Example:

```bash
aws s3 ls --endpoint-url http://localhost:4566
```

---

# 7. Jenkins

## Check Jenkins container

```bash
sudo docker ps -a
```

Look for:

```text
jenkins
```

Example:

```text
cb5685eccef7   jenkins/jenkins:lts   ...   Exited (143)   ...   jenkins
```

`Exited (143)` means the container was stopped. We don't need to create a new Jenkins container.

## Start Jenkins

```bash
sudo docker start jenkins
```

Check:

```bash
sudo docker ps
```

Jenkins should show:

```text
Up ...
```

## Open Jenkins

Open in the browser:

```text
http://localhost:8080
```

## Check Jenkins logs

```bash
sudo docker logs jenkins
```

Live logs:

```bash
sudo docker logs -f jenkins
```

## Restart Jenkins

```bash
sudo docker restart jenkins
```

## Stop Jenkins

```bash
sudo docker stop jenkins
```

---

# 8. Jenkins + Git

When Jenkins gets a project from GitHub, the repository URL is configured in the Jenkins job.

Example repository:

```text
https://github.com/<username>/<repository>.git
```

Check the repository locally:

```bash
git status
```

Commit changes:

```bash
git add .
git commit -m "update Jenkins pipeline"
git push
```

Then Jenkins can build the updated code.

---

# 9. Jenkins Pipeline

A Jenkins pipeline can be defined in a file called:

```text
Jenkinsfile
```

Basic structure:

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }

        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
    }
}
```

The `Jenkinsfile` is normally stored inside the GitHub repository.

---

# 10. Jenkins Shared Library

If the Jenkinsfile uses:

```groovy
@Library('jenkins-shared-lib')
```

Jenkins must have a Shared Library configured with exactly that name.

If the library is not configured, Jenkins can show:

```text
Could not find any definition of libraries [jenkins-shared-lib]
```

Check:

```text
Jenkins
→ Manage Jenkins
→ System
→ Global Pipeline Libraries
```

Add the shared library there.

---

# 11. Useful Daily Startup Order

When starting the lab from scratch, use this order.

## Step 1: Linux

```bash
free -h
df -h
ip a
```

## Step 2: Docker

```bash
sudo systemctl status docker
sudo docker ps
```

If Docker is stopped:

```bash
sudo systemctl start docker
```

## Step 3: Floci

```bash
sudo docker ps
```

Start Floci if needed:

```bash
sudo docker start floci
sudo docker start floci-ui
```

## Step 4: Kubernetes

```bash
minikube status
```

If it is stopped:

```bash
minikube start
```

Then:

```bash
kubectl get nodes
```

## Step 5: Terraform

Go to the project:

```bash
cd ~/terraform/floci-lab
```

Then:

```bash
terraform init
terraform validate
terraform plan
```

Apply only when you want to create/update the infrastructure:

```bash
terraform apply
```

## Step 6: Jenkins

Check:

```bash
sudo docker ps -a
```

Start Jenkins:

```bash
sudo docker start jenkins
```

Check:

```bash
sudo docker ps
```

Open:

```text
http://localhost:8080
```

---

# 12. Quick Health Check

Use these commands to quickly check the whole environment:

```bash
free -h
```

```bash
sudo systemctl status docker
```

```bash
sudo docker ps
```

```bash
minikube status
```

```bash
kubectl get nodes
```

```bash
terraform version
```

```bash
sudo docker ps | grep jenkins
```

If everything is working, you should have:

```text
Docker        → Running
Floci         → Running
Minikube      → Running
Kubernetes    → Node Ready
Terraform     → Available
Jenkins       → Container Up
```

---

# 13. Troubleshooting

## Docker container is stopped

Check:

```bash
sudo docker ps -a
```

Start it:

```bash
sudo docker start <container_name>
```

Check logs:

```bash
sudo docker logs <container_name>
```

---

## Jenkins is stopped

```bash
sudo docker start jenkins
```

Then:

```bash
sudo docker ps
```

If it stops again:

```bash
sudo docker logs jenkins
```

---

## Minikube is not running

```bash
minikube status
```

Start:

```bash
minikube start
```

Then:

```bash
kubectl get nodes
```

---

## Kubernetes cannot connect

Check:

```bash
minikube status
```

Then:

```bash
kubectl config current-context
```

For Minikube:

```bash
kubectl config use-context minikube
```

Then:

```bash
kubectl get nodes
```

---

## Terraform initialization fails

Check internet connection:

```bash
ping -c 4 google.com
```

Then retry:

```bash
terraform init
```

If the provider download fails because of network/IPv6 problems, check the network before changing the Terraform configuration.

---

# 14. Main Commands Cheat Sheet

| Tool       | Check                      | Start                         | Status              |
| ---------- | -------------------------- | ----------------------------- | ------------------- |
| Linux      | `lsb_release -a`           | —                             | `free -h`           |
| Docker     | `docker --version`         | `sudo systemctl start docker` | `sudo docker ps`    |
| Container  | —                          | `sudo docker start NAME`      | `sudo docker ps`    |
| Minikube   | `minikube version`         | `minikube start`              | `minikube status`   |
| Kubernetes | `kubectl version --client` | —                             | `kubectl get nodes` |
| Terraform  | `terraform version`        | `terraform init`              | `terraform plan`    |
| Jenkins    | —                          | `sudo docker start jenkins`   | `sudo docker ps`    |
| Floci      | —                          | `sudo docker start floci`     | `sudo docker ps`    |

---

# 15. Important Paths

Terraform lab:

```text
~/terraform/floci-lab
```

Floci:

```text
~/floci
```

Projects:

```text
~/Projects_
```

NTI:

```text
~/Nti
```

Jenkins:

```text
http://localhost:8080
```

Floci API:

```text
http://localhost:4566
```

Floci UI:

```text
http://localhost:4500
```
