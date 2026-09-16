# CI/CD with Jenkins — Session Notes


![alt text](<Pasted image.png>)

## 1. CI/CD Without Automation

Without CI/CD, when there is a change in the project, we may need to repeat the same steps manually:

1. Clone the code.
2. Build the project.
3. Test the project.
4. Push the image to a registry.
5. Deploy the application.

The problem is that the same steps have to be repeated whenever there is a change.

CI/CD automates this process.

---

# 2. CI vs CD

## Continuous Integration (CI)

CI focuses on integrating changes and making sure the project is still working.

Typical CI steps:

```text
Clone Code
    ↓
Build
    ↓
Test
```

## Continuous Delivery (CD)

After the CI steps succeed, the application can be prepared for delivery.

Example:

```text
Build
  ↓
Test
  ↓
Push Image to Registry
  ↓
Deploy
```

### Continuous Deployment

Continuous Deployment means that the deployment happens automatically after the pipeline succeeds.

```text
Continuous Deployment
        ↓
    Automatic
```

### Continuous Delivery

Continuous Delivery requires an external/manual approval before starting the deployment.

This can be useful for critical projects where deployment should not happen automatically.

```text
Continuous Delivery
        ↓
External Approval
        ↓
Deployment
```

---

# 3. CI/CD Tools

There are many tools that can be used to implement CI/CD.

Examples:

* GitHub Actions
* Jenkins

In this session, we focus on **Jenkins**.

---

# 4. Why Jenkins?

Jenkins is:

* An open-source automation tool.
* Used to automate CI/CD pipelines.
* Extensible through many plugins.
* Java-based.

Jenkins can automate tasks such as:

```text
Build
Test
Push
Deploy
```

Instead of doing these steps manually, Jenkins can execute them automatically.

---

# 5. Jenkins Architecture

Jenkins can work with a **Controller** and **Agents**.

The Jenkins Controller manages the jobs and decides where they should run.

```text
              Jenkins Controller
        ┌──────────────────────────┐
        │ Jobs                     │
        │ Users                    │
        │ Plugins                  │
        │ Nodes                    │
        │ Global Configuration     │
        └────────────┬─────────────┘
                     │
          ┌──────────┴──────────┐
          │                     │
       Static Agent        Dynamic Agent
          │                     │
      Linux Server        Docker / Kubernetes
```

The Controller assigns tasks to agents.

---

# 6. Jenkins Agents

An agent is a machine or environment where Jenkins runs the actual task.

The agent must have the tools required by the project.

For example:

```text
Project requires Python
        ↓
Agent should have Python
```

Jenkins can use different types of agents.

---

## Static Agent

A static agent is available all the time.

```text
Static Agent
     ↓
Works all the time
```

It can be useful for critical projects where we need:

* High speed
* Low latency
* A continuously available environment

### Advantage

```text
Static → Faster
```

### Disadvantage

The server is running even when it is not executing a task, so it can cost more.

---

## Dynamic Agent

A dynamic agent is created when it is needed and can be terminated after finishing the task.

```text
Task starts
    ↓
Create Agent
    ↓
Run Task
    ↓
Task finishes
    ↓
Terminate Agent
```

This helps reduce cost.

```text
Dynamic → Cheaper
```

Dynamic agents can be created using environments such as:

* Docker
* Kubernetes
* EC2

---

# 7. Agent Tools and Versions

Different projects may require different versions of tools.

For example:

```text
Project A → Python 3.10
Project B → Python 3.12
```

Instead of installing everything on the same machine, we can use different agents/environments with the required tools.

Jenkins can also use images/templates to create the required environment.

---

# 8. Jenkins Agent Communication

The Jenkins Controller needs to communicate with its agents.

For a static Linux agent, communication can be established using:

```text
SSH (22)
```

Jenkins can also communicate with dynamic agents using cloud APIs.

Example:

```text
Jenkins Controller
       ↓
   Cloud API
       ↓
Docker / Kubernetes / EC2
       ↓
Dynamic Agent
```

### Important

The Controller must have Jenkins installed.

A static agent does not necessarily need to have Jenkins installed as a full Jenkins server.

---

# 9. Static Agent vs Dynamic Agent

| Static Agent                           | Dynamic Agent                   |
| -------------------------------------- | ------------------------------- |
| Always available                       | Created when needed             |
| Faster                                 | Cheaper                         |
| Runs continuously                      | Terminated after the task       |
| Good for critical/high-speed workloads | Good for reducing resource cost |

---

# 10. Agent Capacity

A server has a limited capacity.

Jenkins uses the available capacity to run tasks.

For example, if an agent has a limited number of executors, only a limited number of tasks can run at the same time.

```text
Agent
 ├── Task 1
 ├── Task 2
 └── Task 3
```

If all available executors are busy, new tasks remain pending until an executor becomes available.

```text
Running Tasks
      ↓
All Executors Busy
      ↓
New Task → Pending
      ↓
Executor Available
      ↓
Task Starts
```

---

# 11. Jenkins on Docker

Jenkins can run inside a Docker container.

The basic idea is:

```text
Host
└── Docker Engine
      └── Jenkins Container
            ├── Jenkins
            ├── Docker Client
            └── Required tools
```

Jenkins can then use Docker to run tasks in containers.

---

# 12. Docker-in-Docker Concept

When Jenkins needs to work with Docker, the Jenkins environment needs access to the Docker engine.

The general idea discussed in the session is:

```text
Host
│
└── Docker Engine
      │
      └── Jenkins Container
            │
            └── Docker Client
                  │
                  ↓
              Docker Engine
```

The important point is that the Jenkins environment needs access to Docker so it can perform Docker-related tasks.

---

# 13. Jenkins Setup

Basic setup flow:

1. Run/install Jenkins.
2. Open Jenkins through the configured port.
3. Install the required plugins.
4. Create a Jenkins user/account.
5. Configure the required credentials.
6. Create a pipeline.

Jenkins can be extended by installing plugins.

For example, plugins can provide integration with other tools.

---

# 14. Jenkins Pipeline

A pipeline defines the steps Jenkins should execute.

A pipeline can contain multiple stages.

Example:

```text
Pipeline
   │
   ├── Build
   │
   ├── Test
   │
   ├── Push
   │
   └── Deploy
```

The pipeline can be created from Jenkins.

---

# 15. Creating a Pipeline

Basic flow:

```text
New Item
   ↓
Add Name
   ↓
Select Pipeline
   ↓
Configure Pipeline
   ↓
Add Commands
   ↓
Build
```

The Pipeline is used to describe what Jenkins should do.

---

# 16. Pipeline Stages

A pipeline can be divided into stages.

Example:

```groovy
pipeline {
    stages {
        stage('Hello') {
            steps {
                echo 'Hello World'
            }
        }

        stage('Build') {
            steps {
                // build commands
            }
        }
    }
}
```

Stages make the pipeline easier to understand.

For example:

```text
Stage 1 → Build
Stage 2 → Test
Stage 3 → Push
Stage 4 → Deploy
```

---

# 17. `sh` vs `sh ''' ... '''`

For Linux commands, Jenkins can use the `sh` step.

### Single command

```groovy
sh 'pwd'
```

### Multiple commands

```groovy
sh '''
    pwd
    ls
    echo "Hello"
'''
```

The multiple-line form is useful when we need to execute several shell commands.

---

# 18. Pipeline Console Output

Jenkins provides **Console Output** for each pipeline run.

It shows the details of the execution, including:

* Commands
* Logs
* Errors
* Success/failure information
* Other execution details

Example:

```text
Build
  ↓
Console Output
  ↓
Check what happened during the run
```

This is useful for debugging failed pipelines.

---

# 19. Jenkinsfile

A pipeline can be stored in a file called:

```text
Jenkinsfile
```

The Jenkinsfile contains the pipeline definition.

The file should be stored in the project repository.

Example project:

```text
project/
├── Jenkinsfile
├── source files
└── other project files
```

The Jenkins pipeline can then use the Jenkinsfile from the GitHub repository.

---

# 20. Jenkinsfile and GitHub

Jenkins can connect to a GitHub repository and use the Jenkinsfile stored there.

Basic flow:

```text
GitHub Repository
       ↓
   Jenkinsfile
       ↓
     Jenkins
       ↓
     Pipeline
       ↓
      Build
```

The repository URL is configured in Jenkins.

The source control type in the pipeline configuration is:

```text
Git
```

---

# 21. Private GitHub Repository

If the GitHub repository is private, Jenkins needs permission to access it.

We can configure GitHub credentials in Jenkins.

Basic idea:

```text
GitHub Private Repository
          ↑
          │
      Credentials
          │
        Jenkins
```

---

# 22. GitHub Personal Access Token

A Personal Access Token (PAT) can be used to authenticate Jenkins with GitHub.

Basic flow:

```text
GitHub
  ↓
Developer Settings
  ↓
Personal Access Tokens
  ↓
Create Token
  ↓
Select Required Permissions
  ↓
Use Token in Jenkins Credentials
```

The token should be treated as a secret.

It should not be written directly inside the Jenkinsfile.

---

# 23. Jenkins Credentials

Credentials can be added from Jenkins and then selected by the pipeline/job.

The general idea is:

```text
Jenkins
  ↓
Credentials
  ↓
Add GitHub Credential
  ↓
Use Credential in Pipeline
```

For private repositories, Jenkins uses the configured credential to access the repository.

---

# 24. Pipeline Script from GitHub

Instead of writing the pipeline directly inside Jenkins, we can tell Jenkins to get the pipeline definition from GitHub.

The important parts are:

```text
Repository URL
      ↓
Git
      ↓
Jenkinsfile
```

The Jenkinsfile contains the pipeline stages and commands.

---

# 25. Post Actions

A pipeline can execute actions after a pipeline or stage finishes.

This is useful for tasks such as cleanup or reporting.

Example:

```groovy
post {
    always {
        echo 'Pipeline finished'
    }

    success {
        echo 'Success'
    }

    failure {
        echo 'Failure'
    }
}
```

### `always`

Runs whether the pipeline succeeds or fails.

```text
always → runs every time
```

### `success`

Runs when the pipeline succeeds.

```text
success → successful pipeline
```

### `failure`

Runs when the pipeline fails.

```text
failure → failed pipeline
```

---

# 26. Post Actions Example

One use case is cleaning temporary files after the pipeline finishes.

```groovy
post {
    always {
        // cleanup temporary files
    }
}
```

This means the cleanup step will run regardless of whether the pipeline succeeds or fails.

---

# 27. Complete CI/CD Flow

The main idea of the session can be summarized as:

```text
Developer Changes Code
          ↓
       GitHub
          ↓
        Jenkins
          ↓
       Pipeline
          ↓
       Build
          ↓
        Test
          ↓
   Push Image / Artifact
          ↓
       Deploy
```

The goal is to automate the repeated steps instead of performing them manually every time.

---

# Lab 01 — CI/CD and Jenkins

## 01) What is CI/CD?

**CI/CD** is a practice for automating software development processes.

**CI — Continuous Integration**

Automatically:

```text
Checkout → Build → Test
```

**CD — Continuous Delivery / Deployment**

Continues the process toward releasing or deploying the application.

---

## 02) Give three CI/CD tools

Three examples:

1. **Jenkins**
2. **GitHub Actions**
3. **GitLab CI/CD**

---

## 03) What is Jenkins Pipeline?

A Jenkins Pipeline is a **set of automated steps written as code** that defines the CI/CD workflow.

Example:

```text
Checkout
   ↓
Build
   ↓
Test
   ↓
Deploy
```

---

## 04) What language is Jenkins based on?

Jenkins is primarily based on:

**Java**

---

## 05) What scripting language is Jenkins Pipeline syntax based on?

Jenkins Pipeline syntax is based on:

**Groovy**

---

## 06) What are the ways you can write Pipeline in Jenkins?

There are two main Pipeline syntax styles:

### 1. Declarative Pipeline

```groovy
pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Build'
            }
        }
    }
}
```

### 2. Scripted Pipeline

```groovy
node {
    stage('Build') {
        echo 'Build'
    }
}
```

A Pipeline can also be stored as a **Jenkinsfile** in the Git repository.

---

# 07) Create Freestyle Project with Hello World

### Step 1

Open Jenkins.

Create:

```text
New Item
```

### Step 2

Enter a project name:

```text
hello-world
```

Select:

```text
Freestyle project
```

### Step 3

Go to:

```text
Build Steps
```

Choose:

```text
Execute shell
```

Add:

```bash
echo "Hello World"
```

### Step 4

Click:

```text
Save
```

Then:

```text
Build Now
```

### Step 5

Open the build and check:

```text
Console Output
```

Expected output:

```text
Hello World
```

---

# 08) Create Jenkins Pipeline for Your Repo Using Jenkinsfile

Create a file in the repository named exactly:

```text
Jenkinsfile
```

Example:

```groovy
pipeline {
    agent any

    stages {
        stage('Hello 1') {
            steps {
                echo 'Hello from Stage 1'
            }
        }

        stage('Hello 2') {
            steps {
                echo 'Hello from Stage 2'
            }
        }
    }
}
```

Repository:

```text
my-project/
├── Jenkinsfile
└── project files
```

Push it to GitHub:

```bash
git add Jenkinsfile
git commit -m "Add Jenkins pipeline"
git push
```

In Jenkins:

```text
New Item
   ↓
Pipeline
   ↓
Pipeline Definition
   ↓
Pipeline script from SCM
   ↓
Git
   ↓
Repository URL
   ↓
Script Path: Jenkinsfile
```

Then:

```text
Save
   ↓
Build Now
```

Pipeline:

```text
Hello 1
   ↓
Hello 2
```

---

# 09) Run Scripts Inside Jenkinsfile

Instead of writing the commands directly as `echo` commands, create a shell script in the repository.

Create:

```text
hello.sh
```

Content:

```bash
#!/bin/bash

echo "Hello from shell script"
```

Make it executable:

```bash
chmod +x hello.sh
```

Now the repository contains:

```text
my-project/
├── Jenkinsfile
└── hello.sh
```

The Jenkinsfile can run the script:

```groovy
pipeline {
    agent any

    stages {
        stage('Hello 1') {
            steps {
                sh './hello.sh'
            }
        }

        stage('Hello 2') {
            steps {
                sh './hello.sh'
            }
        }
    }
}
```

Then push:

```bash
git add Jenkinsfile hello.sh
git commit -m "Run shell script from Jenkins"
git push
```

Jenkins will:

```text
Checkout repository
       ↓
Read Jenkinsfile
       ↓
Stage 1
       ↓
Run hello.sh
       ↓
Stage 2
       ↓
Run hello.sh
```

---

# 10) Repeat Task 09 with a Private Repository

For a private GitHub repository, Jenkins needs credentials to clone the repository.

## Step 1 — Create GitHub Token

Create a GitHub **Personal Access Token (PAT)** with the permissions required to access the private repository.

Do **not** put the token inside:

```text
Jenkinsfile
```

---

## Step 2 — Add Credentials to Jenkins

In Jenkins:

```text
Manage Jenkins
   ↓
Credentials
   ↓
Add Credentials
```

For HTTPS Git authentication, use:

```text
Username: your GitHub username
Password: GitHub PAT
```

Give the credential an ID, for example:

```text
github-private-repo
```

---

## Step 3 — Jenkins Pipeline

Use the private repository URL in the Pipeline SCM configuration.

```text
Pipeline
   ↓
Pipeline Definition
   ↓
Pipeline script from SCM
   ↓
Git
   ↓
Repository URL
   ↓
Credentials
   ↓
github-private-repo
   ↓
Script Path
   ↓
Jenkinsfile
```

Jenkins now uses the stored credentials to access the private repository.

---

## Step 4 — Jenkinsfile

The Jenkinsfile can remain simple:

```groovy
pipeline {
    agent any

    stages {
        stage('Hello 1') {
            steps {
                sh './hello.sh'
            }
        }

        stage('Hello 2') {
            steps {
                sh './hello.sh'
            }
        }
    }
}
```

The important difference is that **Jenkins authenticates during the Git checkout**.

```text
Private GitHub Repository
          ↓
      Credentials
          ↓
        Jenkins
          ↓
       Checkout
          ↓
      Jenkinsfile
          ↓
       Stage 1
          ↓
       Stage 2
```

---

# 28. Quick Revision

### CI

```text
Clone → Build → Test
```

### CD

```text
Build → Test → Push → Deploy
```

### Continuous Deployment

```text
Automatic Deployment
```

### Continuous Delivery

```text
Deployment requires approval
```

### Jenkins

```text
Open-source CI/CD automation tool
```

### Controller

```text
Manages jobs and agents
```

### Static Agent

```text
Always running
→ Faster
```

### Dynamic Agent

```text
Created when needed
→ Cheaper
```

### Jenkinsfile

```text
Pipeline definition stored in the repository
```

### Credentials

```text
Used to securely give Jenkins access to private resources
```

### Console Output

```text
Shows logs and details of a pipeline run
```

### Post

```text
Actions executed after a pipeline/stage
```

---

# Key Idea

The main purpose of Jenkins in CI/CD is to automate the repeated software delivery process:

```text
Code
 ↓
Build
 ↓
Test
 ↓
Push
 ↓
Deploy
```

Instead of repeating these steps manually after every change, Jenkins can execute them as an automated pipeline.

---