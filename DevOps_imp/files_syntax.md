# DevOps Files Syntax & Writing Guide

This README contains the basic syntax, structure, and steps for writing common DevOps files.

Covered topics:

1. Dockerfile
2. Docker Compose YAML
3. Kubernetes YAML files
4. Terraform files
5. Jenkinsfile
6. GitHub Actions YAML
7. Common syntax rules

---

# 1. Dockerfile

A `Dockerfile` contains instructions used to build a Docker image.

## Basic structure

```dockerfile
FROM <base-image>

WORKDIR <directory>

COPY <source> <destination>

RUN <command>

EXPOSE <port>

CMD ["command"]
```

## Example

```dockerfile
FROM python:3.12

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

## Common Dockerfile instructions

### FROM

Defines the base image.

```dockerfile
FROM python:3.12
```

Example:

```dockerfile
FROM ubuntu:24.04
```

---

### WORKDIR

Sets the working directory inside the container.

```dockerfile
WORKDIR /app
```

After this:

```dockerfile
RUN pwd
```

will run inside:

```text
/app
```

---

### COPY

Copies files from the build context into the image.

```dockerfile
COPY app.py /app/
```

Common form:

```dockerfile
COPY <source> <destination>
```

Example:

```dockerfile
COPY . .
```

This copies the current project into the current `WORKDIR`.

---

### RUN

Runs a command while building the image.

```dockerfile
RUN apt update
```

Example:

```dockerfile
RUN pip install -r requirements.txt
```

---

### EXPOSE

Documents the port used by the application.

```dockerfile
EXPOSE 8080
```

Important:

`EXPOSE` does not publish the port to the host.

Publishing is done when running the container:

```bash
docker run -p 8080:8080 image-name
```

---

### CMD

Defines the default command when the container starts.

```dockerfile
CMD ["python", "app.py"]
```

Another example:

```dockerfile
CMD ["nginx", "-g", "daemon off;"]
```

---

## Dockerfile writing steps

### Step 1

Create the file:

```bash
touch Dockerfile
```

### Step 2

Write the basic structure:

```dockerfile
FROM ...

WORKDIR ...

COPY ...

RUN ...

EXPOSE ...

CMD [...]
```

### Step 3

Build the image:

```bash
docker build -t my-app .
```

### Step 4

Check the image:

```bash
docker images
```

### Step 5

Run it:

```bash
docker run -p 8080:8080 my-app
```

---

# 2. Docker Compose YAML

Docker Compose uses YAML files, normally:

```text
compose.yaml
```

or:

```text
docker-compose.yml
```

## Basic structure

```yaml
services:

  app:
    image: <image>
    ports:
      - "<host-port>:<container-port>"

  database:
    image: <database-image>
```

## Example

```yaml
services:

  app:
    build: .
    ports:
      - "8080:8080"

  db:
    image: postgres:16
    environment:
      POSTGRES_PASSWORD: password
```

## Important YAML syntax

Indentation matters.

Correct:

```yaml
services:
  app:
    image: nginx
```

Incorrect:

```yaml
services:
app:
image: nginx
```

Use spaces, not tabs.

---

## Common Compose fields

### image

Use an existing image:

```yaml
image: nginx:latest
```

### build

Build an image using a Dockerfile:

```yaml
build: .
```

### ports

Map host → container:

```yaml
ports:
  - "8080:80"
```

Meaning:

```text
localhost:8080 → container:80
```

### environment

Set environment variables:

```yaml
environment:
  APP_ENV: production
  DEBUG: "false"
```

### volumes

Mount storage:

```yaml
volumes:
  - ./data:/app/data
```

### depends_on

Define startup dependency:

```yaml
depends_on:
  - db
```

---

## Compose commands

Start:

```bash
docker compose up
```

Start in background:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

Check containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs
```

---

# 3. Kubernetes YAML

Kubernetes resources are commonly written as YAML files.

Examples:

```text
deployment.yaml
service.yaml
configmap.yaml
secret.yaml
```

---

# 3.1 Deployment

## Basic structure

```yaml
apiVersion: apps/v1

kind: Deployment

metadata:
  name: my-app

spec:

  replicas: 2

  selector:
    matchLabels:
      app: my-app

  template:

    metadata:
      labels:
        app: my-app

    spec:

      containers:

        - name: my-app
          image: my-image:latest

          ports:
            - containerPort: 8080
```

## Important sections

### apiVersion

Defines the Kubernetes API version.

```yaml
apiVersion: apps/v1
```

### kind

Defines the resource type.

```yaml
kind: Deployment
```

### metadata

Contains information about the resource.

```yaml
metadata:
  name: my-app
```

### spec

Defines the desired state.

```yaml
spec:
  replicas: 2
```

---

# 3.2 Kubernetes Service

A Service provides network access to Pods.

## Basic structure

```yaml
apiVersion: v1

kind: Service

metadata:
  name: my-service

spec:

  selector:
    app: my-app

  ports:
    - port: 80
      targetPort: 8080

  type: ClusterIP
```

## Common service types

### ClusterIP

Internal Kubernetes access:

```yaml
type: ClusterIP
```

### NodePort

Expose through a node port:

```yaml
type: NodePort
```

### LoadBalancer

Used with supported cloud/load-balancer environments:

```yaml
type: LoadBalancer
```

---

# 3.3 Deployment + Service

You can put multiple Kubernetes resources in one YAML file.

Separate them with:

```yaml
---
```

Example:

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: my-app

spec:
  replicas: 2

  selector:
    matchLabels:
      app: my-app

  template:
    metadata:
      labels:
        app: my-app

    spec:
      containers:
        - name: my-app
          image: my-image:latest
          ports:
            - containerPort: 8080

---
apiVersion: v1
kind: Service

metadata:
  name: my-service

spec:
  selector:
    app: my-app

  ports:
    - port: 80
      targetPort: 8080
```

---

# 3.4 Kubernetes ConfigMap

Used for non-sensitive configuration.

```yaml
apiVersion: v1

kind: ConfigMap

metadata:
  name: app-config

data:
  APP_ENV: production
  APP_PORT: "8080"
```

---

# 3.5 Kubernetes Secret

Used for sensitive values.

```yaml
apiVersion: v1

kind: Secret

metadata:
  name: app-secret

type: Opaque

stringData:
  USERNAME: admin
  PASSWORD: password
```

For real projects, don't commit real passwords into Git.

---

# Kubernetes YAML workflow

## Step 1

Create the file:

```bash
touch deployment.yaml
```

## Step 2

Write:

```yaml
apiVersion:
kind:
metadata:
spec:
```

## Step 3

Check YAML indentation.

## Step 4

Apply:

```bash
kubectl apply -f deployment.yaml
```

## Step 5

Check:

```bash
kubectl get pods
```

```bash
kubectl get deployments
```

```bash
kubectl get services
```

## Step 6

Debug:

```bash
kubectl describe pod <pod-name>
```

```bash
kubectl logs <pod-name>
```

## Step 7

Delete:

```bash
kubectl delete -f deployment.yaml
```

---

# 4. Terraform Files

Terraform configuration files normally use:

```text
.tf
```

Common files:

```text
main.tf
variables.tf
outputs.tf
providers.tf
terraform.tfvars
```

---

# 4.1 Provider

A provider tells Terraform which platform/API it will work with.

## Basic syntax

```hcl
terraform {
  required_providers {
    <provider> = {
      source  = "<source>"
      version = "<version>"
    }
  }
}

provider "<provider>" {
  ...
}
```

Example:

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
```

---

# 4.2 Resource

Resources are infrastructure objects managed by Terraform.

## Syntax

```hcl
resource "<resource_type>" "<resource_name>" {

  argument = value

}
```

Example:

```hcl
resource "aws_instance" "web" {

  ami           = "ami-123456"
  instance_type = "t2.micro"

}
```

The Terraform resource is referenced as:

```text
aws_instance.web
```

---

# 4.3 Variables

Variables make Terraform configurations reusable.

## variables.tf

```hcl
variable "instance_type" {

  description = "EC2 instance type"

  type = string

  default = "t2.micro"
}
```

Use it:

```hcl
instance_type = var.instance_type
```

---

# 4.4 terraform.tfvars

Values can be stored in:

```text
terraform.tfvars
```

Example:

```hcl
instance_type = "t2.micro"
```

Terraform automatically loads:

```text
terraform.tfvars
```

---

# 4.5 Outputs

Outputs display useful information after `terraform apply`.

```hcl
output "instance_ip" {

  value = aws_instance.web.public_ip

}
```

After applying:

```bash
terraform output
```

---

# 4.6 Terraform project structure

A simple project can look like:

```text
terraform-project/
│
├── main.tf
├── providers.tf
├── variables.tf
├── outputs.tf
└── terraform.tfvars
```

---

# Terraform workflow

## Step 1

Create the project:

```bash
mkdir terraform-project
cd terraform-project
```

## Step 2

Create files:

```bash
touch main.tf
touch providers.tf
touch variables.tf
touch outputs.tf
touch terraform.tfvars
```

## Step 3

Write Terraform configuration.

## Step 4

Initialize:

```bash
terraform init
```

## Step 5

Format:

```bash
terraform fmt
```

## Step 6

Validate:

```bash
terraform validate
```

## Step 7

Preview changes:

```bash
terraform plan
```

## Step 8

Apply:

```bash
terraform apply
```

## Step 9

Check outputs:

```bash
terraform output
```

## Step 10

Destroy when finished:

```bash
terraform destroy
```

---

# 5. Jenkinsfile

A `Jenkinsfile` defines a Jenkins Pipeline as code.

The file is normally named exactly:

```text
Jenkinsfile
```

No extension.

---

# 5.1 Basic Jenkinsfile

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

        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}
```

---

# 5.2 Pipeline structure

The main structure is:

```groovy
pipeline {

    agent any

    stages {

        stage('Stage Name') {

            steps {
                // commands
            }
        }
    }
}
```

---

# 5.3 Agent

Defines where Jenkins runs the pipeline.

```groovy
agent any
```

This means Jenkins can use any available agent.

---

# 5.4 Stage

A stage represents one part of the pipeline.

```groovy
stage('Build') {
    steps {
        echo 'Building application'
    }
}
```

Common stages:

```text
Checkout
Build
Test
Docker Build
Docker Push
Deploy
```

---

# 5.5 Shell commands

Run Linux commands using:

```groovy
sh 'command'
```

Example:

```groovy
stage('Build') {
    steps {
        sh 'g++ main.cpp -o app'
    }
}
```

Multiple commands:

```groovy
sh '''
    echo "Building"
    g++ main.cpp -o app
    ./app
'''
```

---

# 5.6 Environment variables

```groovy
environment {
    APP_NAME = 'my-app'
}
```

Use:

```groovy
echo "${APP_NAME}"
```

---

# 5.7 Post actions

Run actions after the pipeline.

```groovy
post {

    success {
        echo 'Build successful'
    }

    failure {
        echo 'Build failed'
    }

    always {
        echo 'Pipeline finished'
    }
}
```

---

# 5.8 Jenkinsfile with Build and Test

```groovy
pipeline {

    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'g++ main.cpp -o app'
            }
        }

        stage('Test') {
            steps {
                sh './app'
            }
        }
    }

    post {

        success {
            echo 'Pipeline completed successfully'
        }

        failure {
            echo 'Pipeline failed'
        }
    }
}
```

---

# Jenkinsfile workflow

## Step 1

Create the file:

```bash
touch Jenkinsfile
```

## Step 2

Write:

```groovy
pipeline {
    agent any

    stages {
        ...
    }
}
```

## Step 3

Add stages:

```groovy
stage('Build') {
    steps {
        ...
    }
}
```

## Step 4

Add Linux commands:

```groovy
sh 'command'
```

## Step 5

Commit to Git:

```bash
git add Jenkinsfile
git commit -m "add Jenkins pipeline"
git push
```

## Step 6

Create/configure the Jenkins job.

For a Pipeline from Git:

```text
Jenkins
→ New Item
→ Pipeline
→ Pipeline Definition
→ Pipeline script from SCM
→ Git
→ Repository URL
→ Script Path: Jenkinsfile
```

## Step 7

Run:

```text
Build Now
```

## Step 8

Check:

```text
Console Output
```

---

# 6. GitHub Actions YAML

GitHub Actions workflows use YAML.

File location:

```text
.github/workflows/
```

Example:

```text
.github/
└── workflows/
    └── ci.yml
```

## Basic structure

```yaml
name: CI

on:
  push:

  pull_request:

jobs:

  build:
    runs-on: ubuntu-latest

    steps:

      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Build
        run: echo "Building"

      - name: Test
        run: echo "Testing"
```

---

# GitHub Actions sections

### name

Workflow name:

```yaml
name: CI
```

### on

Defines when the workflow runs:

```yaml
on:
  push:
  pull_request:
```

### jobs

Defines the jobs:

```yaml
jobs:
  build:
```

### runs-on

Defines the runner:

```yaml
runs-on: ubuntu-latest
```

### steps

Defines commands/actions:

```yaml
steps:
  - name: Checkout
    uses: actions/checkout@v4
```

or:

```yaml
- name: Build
  run: g++ main.cpp -o app
```

---

# 7. YAML Syntax Rules

YAML is indentation-sensitive.

## Correct

```yaml
server:
  name: web
  port: 8080
```

## Incorrect

```yaml
server:
name: web
port: 8080
```

Use spaces.

Avoid tabs.

---

# Lists

YAML lists use:

```yaml
items:
  - item1
  - item2
  - item3
```

Example:

```yaml
ports:
  - 80
  - 443
```

---

# Key-value pairs

```yaml
name: Hager
age: 23
```

---

# Strings

```yaml
name: app
```

or:

```yaml
name: "app"
```

When a value could be interpreted as another YAML type, quotes can make the intended string explicit:

```yaml
port: "8080"
```

---

# Comments

YAML comments start with:

```yaml
# This is a comment
```

Example:

```yaml
replicas: 2 # Number of Pods
```

---

# 8. File Creation Commands

## Dockerfile

```bash
touch Dockerfile
```

## Docker Compose

```bash
touch compose.yaml
```

## Kubernetes

```bash
touch deployment.yaml
touch service.yaml
```

## Terraform

```bash
touch main.tf
touch variables.tf
touch outputs.tf
```

## Jenkins

```bash
touch Jenkinsfile
```

## GitHub Actions

```bash
mkdir -p .github/workflows
touch .github/workflows/ci.yml
```

---

# 9. How to Edit the Files

Using VS Code:

```bash
code Dockerfile
```

```bash
code compose.yaml
```

```bash
code deployment.yaml
```

```bash
code main.tf
```

```bash
code Jenkinsfile
```

Open the whole project:

```bash
code .
```

---

# 10. Validation Before Running

Always check the file before applying/running it.

## Dockerfile

Build it:

```bash
docker build -t test-image .
```

If the build succeeds, the Dockerfile syntax is generally valid.

---

## Docker Compose

```bash
docker compose config
```

Then:

```bash
docker compose up
```

---

## Kubernetes YAML

```bash
kubectl apply --dry-run=client -f deployment.yaml
```

Then apply:

```bash
kubectl apply -f deployment.yaml
```

---

## Terraform

Run:

```bash
terraform fmt
terraform validate
terraform plan
```

---

## Jenkinsfile

The Jenkins server parses the Jenkinsfile when the pipeline runs.

Check the pipeline from:

```text
Jenkins
→ Job
→ Build Now
→ Console Output
```

---

# 11. General File Workflow

For most DevOps configuration files, follow this pattern:

```text
1. Create the file
        ↓
2. Write the basic structure
        ↓
3. Add configuration
        ↓
4. Check indentation/syntax
        ↓
5. Validate
        ↓
6. Run/apply
        ↓
7. Check the result
        ↓
8. Debug if necessary
        ↓
9. Commit to Git
```

---

# 12. Quick Syntax Comparison

| Technology     | File           | Main Syntax         |
| -------------- | -------------- | ------------------- |
| Docker         | `Dockerfile`   | Docker instructions |
| Docker Compose | `compose.yaml` | YAML                |
| Kubernetes     | `*.yaml`       | YAML                |
| Terraform      | `*.tf`         | HCL                 |
| Jenkins        | `Jenkinsfile`  | Groovy              |
| GitHub Actions | `*.yml`        | YAML                |

---

# 13. The Most Important Structures

## Dockerfile

```dockerfile
FROM ...

WORKDIR ...

COPY ...

RUN ...

EXPOSE ...

CMD [...]
```

## Kubernetes

```yaml
apiVersion: ...

kind: ...

metadata:
  name: ...

spec:
  ...
```

## Terraform

```hcl
resource "type" "name" {
    argument = value
}
```

## Jenkins

```groovy
pipeline {

    agent any

    stages {

        stage('Name') {

            steps {
                ...
            }
        }
    }
}
```

## GitHub Actions

```yaml
name: CI

on:
  push:

jobs:

  build:
    runs-on: ubuntu-latest

    steps:
      - name: Step
        run: command
```

---

# 14. Remember

### Dockerfile

Build:

```bash
docker build -t image-name .
```

Run:

```bash
docker run image-name
```

---

### Docker Compose

Start:

```bash
docker compose up -d
```

Stop:

```bash
docker compose down
```

---

### Kubernetes

Apply:

```bash
kubectl apply -f file.yaml
```

Check:

```bash
kubectl get pods
```

Delete:

```bash
kubectl delete -f file.yaml
```

---

### Terraform

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Destroy:

```bash
terraform destroy
```

---

### Jenkins

Create:

```text
Jenkinsfile
```

Commit:

```bash
git add Jenkinsfile
git commit -m "add Jenkinsfile"
git push
```

Then Jenkins:

```text
Pipeline → Pipeline script from SCM → Git → Jenkinsfile → Build Now
```

---

# Final Mental Model

Think about each file this way:

```text
Dockerfile
    ↓
How do I build my application image?

compose.yaml
    ↓
How do I run multiple containers together?

Kubernetes YAML
    ↓
How do I tell Kubernetes what my application should look like?

Terraform
    ↓
How do I define and manage infrastructure as code?

Jenkinsfile
    ↓
How do I automate build, test, and deployment?

GitHub Actions YAML
    ↓
How do I automate CI/CD using GitHub?
```
