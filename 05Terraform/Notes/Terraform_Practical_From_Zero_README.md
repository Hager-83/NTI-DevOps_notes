# Terraform From Zero to a Modular AWS Infrastructure

> A practical, instructor-style guide for learning Terraform by building a real infrastructure project step by step with a local AWS-compatible emulator.

---

## 1. What We Are Going to Build

In this course, we will learn Terraform by actually building infrastructure instead of starting with a large final configuration.

Our final architecture will contain:

- One VPC
- Two public subnets
- Two private subnets
- One Internet Gateway
- Public and private route tables
- Two public EC2 instances
- Security groups
- One public Application Load Balancer
- One target group
- One HTTP listener
- Two EC2 instances attached to the target group
- Terraform variables
- Terraform outputs
- Terraform state
- Terraform workspaces
- Terraform modules

We will first build the infrastructure as a simple Terraform configuration.

After we understand how every resource works, we will refactor the configuration into modules.

The important idea is:

> **Do not start by copying the final project. Build it one small piece at a time and understand every piece before moving on.**

---

# 2. What Is Terraform?

Terraform is an Infrastructure as Code (IaC) tool.

Instead of manually creating infrastructure through a cloud provider's web console, we describe the desired infrastructure in configuration files.

For example, instead of manually clicking through an AWS console to create a VPC, we can describe the VPC in Terraform:

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
```

Terraform reads this configuration and communicates with the infrastructure provider to create the requested resource.

The configuration becomes a reproducible description of the infrastructure.

---

# 3. What Is Infrastructure as Code?

Infrastructure as Code means managing infrastructure using code and configuration files.

Without IaC, someone might:

1. Open the AWS Console.
2. Create a VPC.
3. Create subnets.
4. Create route tables.
5. Create security groups.
6. Create EC2 instances.
7. Configure a load balancer.

The problem is that this process is manual and difficult to reproduce consistently.

With Terraform, the infrastructure is described as code.

For example:

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
```

The same configuration can be used again.

This gives us:

- Reproducibility
- Version control
- Automation
- Consistency
- Easier collaboration
- A clear record of infrastructure configuration

---

# 4. How Terraform Works

The basic Terraform workflow is:

```text
Write configuration
       ↓
terraform init
       ↓
terraform validate
       ↓
terraform plan
       ↓
terraform apply
       ↓
Terraform creates or changes infrastructure
```

Later, when the infrastructure is no longer needed:

```text
terraform destroy
```

---

# 5. Why Are We Using Floci?

Normally, Terraform can communicate with real AWS.

For example:

```text
Terraform
   |
   v
AWS API
   |
   v
VPC / EC2 / ALB / ...
```

For this training project, we do not want to create real AWS resources and generate real AWS costs.

Therefore, we use **Floci**, a local AWS-compatible emulator.

The architecture becomes:

```text
Terraform
    |
    | AWS API requests
    v
Floci
    |
    v
Local simulated AWS resources
```

Floci exposes an AWS-compatible API locally.

Our Terraform AWS provider is configured to send requests to:

```text
http://localhost:4566
```

instead of the real AWS endpoint.

This allows us to practice Terraform using local infrastructure.

---

# 6. Verify the Environment

Before writing Terraform, make sure the local AWS emulator is running.

Check Docker:

```bash
docker ps
```

The Floci container should be running.

The API is expected to be available on:

```text
http://localhost:4566
```

We can also verify the AWS CLI configuration:

```bash
aws configure list
```

For this local environment, the credentials are dummy credentials:

```text
Access key: test
Secret key: test
Region: us-east-1
```

These credentials are used by the local emulator and are not real AWS credentials.

---

# 7. Create the Terraform Project

Create a project directory:

```bash
mkdir terraform
cd terraform
```

Open the directory in VS Code:

```bash
code .
```

We will write Terraform code in VS Code.

Commands such as `terraform init` and `terraform plan` will be executed in the VS Code terminal.

---

# 8. How to Learn Terraform Resources from the Documentation

A major goal of this project is not simply to memorize Terraform syntax.

You should learn how to find the syntax yourself.

Terraform providers contain documentation for resources and data sources.

For AWS, we use the Terraform AWS Provider documentation.

When we need a VPC, search the Terraform Registry for:

```text
aws_vpc
```

When we need a subnet:

```text
aws_subnet
```

For an EC2 instance:

```text
aws_instance
```

For an Application Load Balancer:

```text
aws_lb
```

For a target group:

```text
aws_lb_target_group
```

The general workflow is:

```text
What infrastructure do I need?
        ↓
Find the Terraform resource
        ↓
Read the example
        ↓
Read the arguments
        ↓
Write the smallest configuration
        ↓
terraform validate
        ↓
terraform plan
        ↓
terraform apply
        ↓
Verify the result
```

This is much more useful than memorizing complete Terraform files.

---

# 9. First Step: Configure the AWS Provider

Before Terraform can create AWS resources, Terraform needs to know which provider it should use.

Create:

```text
main.tf
```

Start with the provider:

```hcl
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region     = "us-east-1"
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true

  endpoints {
    ec2                  = "http://localhost:4566"
    elasticloadbalancing = "http://localhost:4566"
  }
}
```

## What does this mean?

The `terraform` block declares the provider.

```hcl
source = "hashicorp/aws"
```

means that we are using the AWS provider published by HashiCorp.

The provider block configures that provider.

```hcl
region = "us-east-1"
```

sets the AWS region used by our local environment.

These are dummy credentials:

```hcl
access_key = "test"
secret_key = "test"
```

The endpoint configuration is important for our local environment:

```hcl
endpoints {
  ec2                  = "http://localhost:4566"
  elasticloadbalancing = "http://localhost:4566"
}
```

It tells Terraform to send the supported AWS API requests to Floci instead of real AWS.

---

# 10. Initialize Terraform

Now run:

```bash
terraform init
```

Terraform downloads the required provider and prepares the working directory.

You should see that the AWS provider has been initialized.

---

# 11. Validate the Configuration

Run:

```bash
terraform validate
```

Terraform checks whether the configuration is syntactically and structurally valid.

Validation does not create infrastructure.

Think of it as:

```text
Is my Terraform configuration written correctly?
```

---

# 12. Build the First Resource: A VPC

Now we need a VPC.

Do not start with subnets, EC2, or ALB.

First create only the VPC.

Search the Terraform AWS Provider documentation for:

```text
aws_vpc
```

Look at the example and the required arguments.

The smallest useful configuration is:

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
```

---

# 13. Understand the VPC Resource

The first line:

```hcl
resource "aws_vpc" "main" {
```

contains two important names.

The first is the Terraform resource type:

```text
aws_vpc
```

The second is our local Terraform name:

```text
main
```

Together they identify the resource inside Terraform:

```text
aws_vpc.main
```

The CIDR block defines the network range:

```hcl
cidr_block = "10.0.0.0/16"
```

At this stage, do not add anything that we do not need yet.

---

# 14. Plan the VPC

Run:

```bash
terraform plan
```

Terraform compares:

```text
Configuration
      +
Current Terraform state
      ↓
Proposed changes
```

You should see Terraform planning to create one VPC.

Nothing is created by `terraform plan`.

---

# 15. Apply the VPC

Run:

```bash
terraform apply
```

Terraform will show the planned change and ask for confirmation.

Enter:

```text
yes
```

Terraform now creates the VPC through Floci.

---

# 16. Why Did Terraform Create the VPC?

Terraform is not simply executing the file line by line.

Terraform builds a model of the desired infrastructure.

The configuration says:

```text
I want a VPC.
```

Terraform checks its state and the provider.

If the VPC does not exist in the current Terraform state, Terraform plans to create it.

This is the foundation of Terraform's declarative approach.

We describe **what we want**, rather than writing a sequence of imperative commands explaining exactly how to create it.

---

# 17. Terraform State

After applying the VPC, Terraform creates a state file:

```text
terraform.tfstate
```

The state records information about infrastructure managed by Terraform.

Conceptually:

```text
Terraform configuration
        |
        v
Terraform state
        |
        v
Real/emulated infrastructure
```

Terraform uses the state to understand what it manages and what changes are required.

For example, if we run:

```bash
terraform plan
```

again without changing the configuration, Terraform should normally report that there are no changes to make.

---

# 18. Add DNS Support to the VPC

Once the basic VPC works, we can improve the configuration.

Update the VPC:

```hcl
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
}
```

These settings enable DNS functionality for the VPC.

Run:

```bash
terraform validate
```

Then:

```bash
terraform plan
```

Then:

```bash
terraform apply
```

The important learning pattern is:

> Change one thing, validate it, plan it, apply it, and understand the result.

---

# 19. Add Public Subnets

A VPC alone is not enough.

We need subnets inside the VPC.

Search the Terraform documentation for:

```text
aws_subnet
```

A subnet needs information such as:

- VPC ID
- CIDR block
- Availability Zone

Our first public subnet can be:

```hcl
resource "aws_subnet" "public_1" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
}
```

Notice this:

```hcl
vpc_id = aws_vpc.main.id
```

We did not manually type the VPC ID.

Terraform knows the ID of the VPC it created.

This is one of the most important Terraform concepts:

> Resources can reference other resources directly.

---

# 20. Add the Second Public Subnet

We need two public subnets for the final architecture.

```hcl
resource "aws_subnet" "public_2" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
}
```

Now our network contains:

```text
VPC
├── Public Subnet 1
└── Public Subnet 2
```

Run:

```bash
terraform validate
terraform plan
terraform apply
```

---

# 21. Add Private Subnets

The final architecture also needs two private subnets.

```hcl
resource "aws_subnet" "private_1" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "us-east-1a"
}
```

And:

```hcl
resource "aws_subnet" "private_2" {
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "us-east-1b"
}
```

At this point:

```text
VPC
│
├── Public Subnet 1
├── Public Subnet 2
├── Private Subnet 1
└── Private Subnet 2
```

---

# 22. Internet Gateway

Public subnets need a path to the internet.

Search the Terraform documentation for:

```text
aws_internet_gateway
```

Create:

```hcl
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
}
```

The Internet Gateway is attached to the VPC.

But creating an Internet Gateway alone does not automatically make a subnet public.

We still need routing.

---

# 23. Public Route Table

Search for:

```text
aws_route_table
```

Create:

```hcl
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
}
```

Now add a default route:

```hcl
resource "aws_route" "public_internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.main.id
}
```

The important part is:

```text
0.0.0.0/0
```

This represents the default route.

Traffic that does not match a more specific route can use this route.

---

# 24. Associate Public Subnets with the Public Route Table

Creating a route table does not automatically attach it to the subnets.

We need route table associations.

```hcl
resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.public_1.id
  route_table_id = aws_route_table.public.id
}
```

And:

```hcl
resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.public_2.id
  route_table_id = aws_route_table.public.id
}
```

Now the public path is conceptually:

```text
Public Subnet
      |
      v
Public Route Table
      |
      v
0.0.0.0/0
      |
      v
Internet Gateway
```

---

# 25. Private Route Table

Private subnets also need a route table.

```hcl
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id
}
```

Associate both private subnets with it.

```hcl
resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.private_1.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.private_2.id
  route_table_id = aws_route_table.private.id
}
```

For this training environment, we do not add a NAT Gateway.

Therefore, the private route table does not contain an internet route.

---

# 26. Introduce Variables

Hard-coding values works for a small experiment, but it becomes inconvenient when the configuration grows.

Instead of:

```hcl
cidr_block = "10.0.0.0/16"
```

we can create a variable.

Create:

```text
variables.tf
```

Add:

```hcl
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}
```

Then use:

```hcl
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
}
```

The value can be supplied from a `.tfvars` file.

---

# 27. tfvars Files

Create:

```text
dev.tfvars
```

Example:

```hcl
vpc_cidr = "172.17.0.0/16"
```

Then:

```bash
terraform plan -var-file="dev.tfvars"
```

This separates:

```text
Infrastructure definition
```

from:

```text
Environment-specific values
```

That becomes especially useful when we introduce workspaces and multiple environments.

---

# 28. Workspaces

Terraform workspaces allow the same configuration to maintain separate state.

For example:

```text
dev
prod
```

Each workspace has its own Terraform state.

Conceptually:

```text
Same Terraform configuration
          |
     ┌────┴────┐
     v         v
    dev       prod
   state      state
```

Create a development workspace:

```bash
terraform workspace new dev
```

Select it with:

```bash
terraform workspace select dev
```

Check the current workspace:

```bash
terraform workspace show
```

Create production:

```bash
terraform workspace new prod
```

Then select it:

```bash
terraform workspace select prod
```

For this project, we use only:

```text
dev
prod
```

---

# 29. Why Use Workspaces?

Imagine that the same infrastructure configuration should exist in:

```text
Development
Production
```

We do not want the development state and production state mixed together.

Workspaces provide separate state contexts.

However, workspaces do not automatically create different infrastructure values.

We still need environment-specific variables.

For example:

```text
dev.tfvars
prod.tfvars
```

The workspace and variable file solve different problems.

---

# 30. Add EC2 Instances

Once the network is ready, we can create EC2 instances.

Search the Terraform documentation for:

```text
aws_instance
```

The basic resource looks like:

```hcl
resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public_1.id
}
```

The important arguments are:

```text
ami
instance_type
subnet_id
```

For the local emulator, use an AMI that actually exists in the emulator.

Example:

```hcl
ami_id = "ami-0abcdef1234567890"
```

Do not assume that a real AWS AMI ID from an assignment exists in a local emulator.

Always verify the available AMIs when working with an emulator.

---

# 31. Create Two EC2 Instances

Our final public architecture requires two public EC2 instances.

Instead of duplicating the complete resource, we can use `count`.

```hcl
resource "aws_instance" "web" {
  count = 2

  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.public_subnet_ids[count.index]

  vpc_security_group_ids = [aws_security_group.ec2.id]
}
```

The idea is:

```text
count = 2
```

creates two instances.

The subnet expression:

```hcl
var.public_subnet_ids[count.index]
```

allows the instances to be placed in different public subnets.

---

# 32. Security Groups

The EC2 instances need controlled network access.

Search:

```text
aws_security_group
```

The load balancer should be allowed to send HTTP traffic to the EC2 instances.

Conceptually:

```text
Internet
   |
   v
ALB Security Group
   |
   | HTTP :80
   v
EC2 Security Group
```

The EC2 security group can contain:

```hcl
ingress {
  from_port       = 80
  to_port         = 80
  protocol        = "tcp"
  security_groups = [aws_security_group.alb.id]
}
```

This allows HTTP traffic from the ALB security group.

---

# 33. Application Load Balancer

Now we can build the final front end.

Search the Terraform documentation for:

```text
aws_lb
```

The ALB needs:

- Name
- Load balancer type
- Internal/public setting
- Security group
- Subnets

Example:

```hcl
resource "aws_lb" "public" {
  name               = "public-alb"
  internal           = false
  load_balancer_type = "application"

  security_groups = [aws_security_group.alb.id]
  subnets         = aws_subnet.public[*].id
}
```

`internal = false` means the load balancer is internet-facing.

---

# 34. Target Group

The ALB needs somewhere to send traffic.

Search:

```text
aws_lb_target_group
```

Create:

```hcl
resource "aws_lb_target_group" "public" {
  name     = "public-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id

  health_check {
    path     = "/"
    protocol = "HTTP"
    matcher  = "200"
  }
}
```

The target group contains the backend targets.

The health check tells the load balancer how to determine whether a target is healthy.

---

# 35. Listener

The ALB needs a listener.

Search:

```text
aws_lb_listener
```

Create:

```hcl
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.public.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.public.arn
  }
}
```

The traffic flow becomes:

```text
Client
  |
  | HTTP :80
  v
Public ALB
  |
  v
HTTP Listener
  |
  v
Target Group
  |
  ├── EC2 #1
  └── EC2 #2
```

---

# 36. Attach EC2 Instances to the Target Group

The target group still needs targets.

Search:

```text
aws_lb_target_group_attachment
```

Example:

```hcl
resource "aws_lb_target_group_attachment" "public" {
  count = length(aws_instance.web)

  target_group_arn = aws_lb_target_group.public.arn
  target_id        = aws_instance.web[count.index].id
  port             = 80
}
```

Now the two EC2 instances become targets of the ALB.

---

# 37. Outputs

Sometimes we need useful information after Terraform finishes.

For example, we want the ALB DNS name.

Create:

```text
outputs.tf
```

Add:

```hcl
output "alb_dns_name" {
  description = "DNS name of the public ALB"
  value       = aws_lb.public.dns_name
}
```

After applying:

```bash
terraform output
```

Terraform displays the output.

Outputs are useful when another resource, module, person, or system needs information from our infrastructure.

---

# 38. Why Do We Need Modules?

At this point, our Terraform configuration works, but the configuration can become large.

We can organize related resources into modules.

Instead of keeping everything in one root configuration:

```text
VPC
Subnets
Route Tables
EC2
Security Groups
ALB
```

we can separate responsibilities:

```text
modules/
├── vpc/
├── ec2/
└── alb/
```

A module is a reusable Terraform configuration.

Think of it as a component with:

```text
Inputs
   ↓
Module
   ↓
Outputs
```

---

# 39. VPC Module

Create:

```text
modules/vpc/
```

The VPC module contains resources related to networking:

```text
modules/vpc/
├── vpc.tf
├── subnets.tf
├── igw.tf
├── public-rw.tf
├── private-rw.tf
├── variables.tf
└── outputs.tf
```

The module receives values such as:

```text
VPC CIDR
Public subnet CIDRs
Private subnet CIDRs
Availability Zones
Tags
```

---

# 40. Module Variables

Inside:

```text
modules/vpc/variables.tf
```

define:

```hcl
variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "public_subnet_cidr" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
}

variable "private_subnet_cidr" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
}

variable "azs" {
  description = "Availability zones for the subnets"
  type        = list(string)
}

variable "tags" {
  description = "Tags for VPC resources"
  type        = map(string)
  default     = {}
}
```

These variables are the module's inputs.

---

# 41. Module Outputs

The root configuration needs to know the IDs created inside the module.

Inside:

```text
modules/vpc/outputs.tf
```

we expose:

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "public_subnet_ids" {
  value = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  value = aws_subnet.private[*].id
}
```

Now the root module can access:

```hcl
module.vpc.vpc_id
```

and:

```hcl
module.vpc.public_subnet_ids
```

This is the connection between modules.

---

# 42. EC2 Module

Create:

```text
modules/ec2/
```

Structure:

```text
modules/ec2/
├── ec2.tf
├── variables.tf
└── outputs.tf
```

The EC2 module should not need to know how the VPC was created.

It only needs the information required to create EC2 instances.

For example:

```text
AMI
Instance type
Subnet IDs
Instance count
Security group ID
Tags
```

This is an important module design principle:

> A module should receive what it needs through inputs rather than depending on unrelated resources directly.

---

# 43. EC2 Module Resource

The module resource can be:

```hcl
resource "aws_instance" "this" {
  count = var.instance_count

  ami           = var.ami_id
  instance_type = var.instance_type

  subnet_id = var.subnet_ids[count.index]

  vpc_security_group_ids = [var.security_group_id]

  tags = merge(var.tags, {
    Name = "ec2-${count.index + 1}"
  })
}
```

The module does not decide which VPC to use directly.

It receives subnet IDs.

Because a subnet belongs to a VPC, the instance is automatically created in the correct VPC.

---

# 44. EC2 Module Output

Create:

```hcl
output "instance_ids" {
  value = aws_instance.this[*].id
}
```

The root configuration can now use:

```hcl
module.ec2.instance_ids
```

This will be useful when connecting the EC2 instances to the ALB target group.

---

# 45. ALB Module

Create:

```text
modules/alb/
```

Structure:

```text
modules/alb/
├── alb.tf
├── variables.tf
└── outputs.tf
```

The ALB module receives:

```text
VPC ID
Public subnet IDs
ALB security group ID
EC2 instance IDs
Tags
```

It creates:

```text
ALB
Target Group
Listener
Target Attachments
```

---

# 46. ALB Module Resource

The ALB resource:

```hcl
resource "aws_lb" "public" {
  name               = "public-alb"
  internal           = false
  load_balancer_type = "application"

  security_groups = [var.security_group_id]
  subnets         = var.subnet_ids
}
```

The target group:

```hcl
resource "aws_lb_target_group" "public" {
  name     = "public-tg"
  port     = 80
  protocol = "HTTP"
  vpc_id   = var.vpc_id

  health_check {
    path     = "/"
    protocol = "HTTP"
    matcher  = "200"
  }
}
```

The listener:

```hcl
resource "aws_lb_listener" "http" {
  load_balancer_arn = aws_lb.public.arn
  port              = 80
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.public.arn
  }
}
```

The attachments:

```hcl
resource "aws_lb_target_group_attachment" "public" {
  count = length(var.target_instance_ids)

  target_group_arn = aws_lb_target_group.public.arn
  target_id        = var.target_instance_ids[count.index]
  port             = 80
}
```

---

# 47. Connect the Modules

Now the root configuration becomes the place where the modules are connected.

VPC:

```hcl
module "vpc" {
  source = "./modules/vpc"

  vpc_cidr            = var.vpc_cidr
  public_subnet_cidr  = var.public_subnet_cidr
  private_subnet_cidr = var.private_subnet_cidr
  azs                 = var.azs
  tags                = var.tags
}
```

EC2 receives subnet IDs from the VPC module:

```hcl
module "ec2" {
  source = "./modules/ec2"

  ami_id            = var.ami_id
  instance_type     = var.instance_type
  instance_count    = var.instance_count
  subnet_ids        = module.vpc.public_subnet_ids
  security_group_id = aws_security_group.ec2.id

  tags = var.tags
}
```

The ALB receives both network and EC2 information:

```hcl
module "alb" {
  source = "./modules/alb"

  vpc_id              = module.vpc.vpc_id
  subnet_ids          = module.vpc.public_subnet_ids
  security_group_id   = aws_security_group.alb.id
  target_instance_ids = module.ec2.instance_ids

  tags = var.tags
}
```

This is the important dependency chain:

```text
VPC Module
    |
    ├── VPC ID
    └── Public Subnet IDs
            |
            v
        EC2 Module
            |
            └── Instance IDs
                    |
                    v
                ALB Module
```

Terraform understands these dependencies from the references.

---

# 48. Final Project Structure

The final project is organized as:

```text
terraform/
├── main.tf
├── variables.tf
├── outputs.tf
├── dev.tfvars
├── prod.tfvars
│
└── modules/
    ├── vpc/
    │   ├── vpc.tf
    │   ├── subnets.tf
    │   ├── igw.tf
    │   ├── public-rw.tf
    │   ├── private-rw.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    ├── ec2/
    │   ├── ec2.tf
    │   ├── variables.tf
    │   └── outputs.tf
    │
    └── alb/
        ├── alb.tf
        ├── variables.tf
        └── outputs.tf
```

---

# 49. Final Architecture

The final infrastructure looks like:

```text
                         Internet
                            |
                            v
                    +---------------+
                    | Public ALB    |
                    | HTTP :80      |
                    +-------+-------+
                            |
                     Target Group
                       /       \
                      /         \
                     v           v
             +-----------+   +-----------+
             | Public EC2|   | Public EC2|
             | Instance 1|   | Instance 2|
             +-----------+   +-----------+
                    |             |
              Public Subnet 1  Public Subnet 2
                    \             /
                     \           /
                      +---------+
                      |   VPC   |
                      +---------+
                      /         \
                     /           \
          Private Subnet 1   Private Subnet 2
```

The VPC contains:

```text
VPC
├── Public Subnet 1
│   └── EC2 Instance 1
│
├── Public Subnet 2
│   └── EC2 Instance 2
│
├── Private Subnet 1
└── Private Subnet 2
```

The public networking path is:

```text
Internet
    |
    v
Internet Gateway
    |
    v
Public Route Table
    |
    v
Public Subnets
```

---

# 50. The Terraform Workflow We Followed

The complete learning process is:

```text
1. Understand Terraform
        ↓
2. Understand IaC
        ↓
3. Understand Floci
        ↓
4. Configure the AWS provider
        ↓
5. terraform init
        ↓
6. Create a VPC
        ↓
7. terraform validate
        ↓
8. terraform plan
        ↓
9. terraform apply
        ↓
10. Add subnets
        ↓
11. Add Internet Gateway
        ↓
12. Add route tables
        ↓
13. Add route associations
        ↓
14. Introduce variables
        ↓
15. Introduce outputs
        ↓
16. Understand state
        ↓
17. Understand workspaces
        ↓
18. Create EC2 instances
        ↓
19. Create security groups
        ↓
20. Create ALB
        ↓
21. Create target group
        ↓
22. Create listener
        ↓
23. Attach EC2 instances
        ↓
24. Refactor into modules
        ↓
25. Connect module inputs/outputs
        ↓
26. Plan and apply the final architecture
```

---

# 51. Important Terraform Commands

## Initialize

```bash
terraform init
```

Downloads providers and initializes the working directory.

## Format

```bash
terraform fmt
```

Formats Terraform files.

## Validate

```bash
terraform validate
```

Checks Terraform configuration syntax and structure.

## Plan

```bash
terraform plan
```

Shows the changes Terraform intends to make.

With an environment file:

```bash
terraform plan -var-file="prod.tfvars"
```

## Apply

```bash
terraform apply
```

Creates or changes infrastructure.

With an environment file:

```bash
terraform apply -var-file="prod.tfvars"
```

## Show Current Workspace

```bash
terraform workspace show
```

## List Workspaces

```bash
terraform workspace list
```

## Select a Workspace

```bash
terraform workspace select prod
```

## Show Outputs

```bash
terraform output
```

## Destroy

```bash
terraform destroy
```

With a specific variable file:

```bash
terraform destroy -var-file="prod.tfvars"
```

---

# 52. The Most Important Learning Habit

When you need to create a new Terraform resource, do not immediately search for a complete project.

Use this process:

```text
I need a resource
       ↓
Search Terraform Registry
       ↓
Find the resource
       ↓
Read the example
       ↓
Read the arguments
       ↓
Identify required arguments
       ↓
Write the smallest configuration
       ↓
Validate
       ↓
Plan
       ↓
Apply
       ↓
Verify
       ↓
Only then add more configuration
```

For example:

```text
"I need an ALB"
        ↓
Search: aws_lb
        ↓
Read the documentation
        ↓
Identify:
  name
  internal
  load_balancer_type
  security_groups
  subnets
        ↓
Write the resource
        ↓
Validate
        ↓
Plan
        ↓
Apply
```

This is how you become able to build Terraform infrastructure independently.

---

# 53. Final Mental Model

Terraform can be understood using five main ideas.

### Provider

Terraform needs a provider to communicate with an infrastructure platform.

```text
Terraform → AWS Provider → Floci
```

### Resource

A resource describes something we want to create.

```hcl
resource "aws_vpc" "main" {
  ...
}
```

### Variable

A variable makes configuration reusable.

```hcl
var.vpc_cidr
```

### State

State allows Terraform to keep track of the infrastructure it manages.

```text
Configuration ↔ State ↔ Infrastructure
```

### Module

A module packages related Terraform resources into a reusable component.

```text
Inputs → Module → Outputs
```

Together:

```text
                 Terraform
                     |
             +-------+-------+
             |               |
          Provider         State
             |
           Floci
             |
      Infrastructure
             |
     +-------+-------+
     |       |       |
    VPC     EC2     ALB
     |
  Modules
```

---

# 54. What You Should Be Able to Do After This Project

After completing the project, you should be able to:

- Explain Infrastructure as Code.
- Explain what Terraform does.
- Explain the Terraform workflow.
- Configure the AWS provider.
- Work with a local AWS-compatible emulator.
- Find resources in the Terraform documentation.
- Read Terraform resource examples.
- Understand resource arguments.
- Create VPC networking.
- Create subnets.
- Configure an Internet Gateway.
- Configure route tables.
- Use variables.
- Use `.tfvars` files.
- Understand Terraform state.
- Use Terraform workspaces.
- Create EC2 instances.
- Configure security groups.
- Create an Application Load Balancer.
- Create target groups and listeners.
- Attach instances to a target group.
- Create Terraform modules.
- Pass variables into modules.
- Expose outputs from modules.
- Connect modules together.
- Build and maintain a modular Terraform project.

The goal is not to memorize this project.

The goal is to understand **how to build the project yourself from the Terraform documentation.**
