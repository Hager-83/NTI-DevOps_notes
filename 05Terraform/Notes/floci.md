# Installing Floci

This guide explains how to install and run **Floci** using Docker.

## Prerequisites

Ensure the following software is installed:

- Docker 20.10+
- Docker Compose (or `docker compose`)

Verify the installation:

```bash
docker --version
docker compose version
```

---

## Create a Docker Compose File

Create a file named `docker-compose.yml` with the following content:

```yaml
services:
  floci:
    image: floci/floci:latest
    container_name: floci
    privileged: true
    ports:
      - "4566:4566"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock

  floci-ui:
    image: floci/floci-ui:latest
    container_name: floci-ui
    ports:
      - "4500:4500"
    depends_on:
      - floci
```

---

## Start Floci

Run:

```bash
docker compose up -d
```

Verify that both containers are running:

```bash
docker ps
```

Expected output:

```text
CONTAINER ID   IMAGE                  STATUS
xxxxxxxxxxxx   floci/floci:latest     Up ...
xxxxxxxxxxxx   floci/floci-ui:latest  Up ...
```

---

## Open the Floci UI

Open your browser and navigate to:

```
http://localhost:4500
```

---

## Configure AWS CLI

Configure the AWS CLI with dummy credentials:

```bash
aws configure
```

Use the following values:

```text
AWS Access Key ID: test
AWS Secret Access Key: test
Default region: us-east-1
Default output format: json
```

Alternatively, set environment variables:

```bash
export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
```

---

## Test the Installation

Run:

```bash
aws ec2 describe-vpcs \
  --endpoint-url http://localhost:4566
```

If Floci is running correctly, the command will return a JSON response.

---

## Configure Terraform

Example provider configuration:

```hcl
provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true

  endpoints {
    ec2 = "http://localhost:4566"
  }
}
```

---

## Troubleshooting

### Check running containers

```bash
docker ps -a
```

### Start existing containers

```bash
docker start floci
docker start floci-ui
```

### View Floci logs

```bash
docker logs floci
```

### View Floci UI logs

```bash
docker logs floci-ui
```

### Stop Floci

```bash
docker compose down
```

---

## Useful Commands

```bash
# Start Floci
docker compose up -d

# Stop Floci
docker compose down

# Restart Floci
docker compose restart

# View logs
docker logs floci

# Verify EC2 API
aws ec2 describe-vpcs \
  --endpoint-url http://localhost:4566

# List Docker containers
docker ps
```


----------------------------------------------

```
Start Floci
docker compose up -d

docker ps

floci
floci-ui

```