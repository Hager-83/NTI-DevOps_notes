# Ansible – Beginner Revision

## 0. Requirements / Before Starting

Before learning Ansible, you should have a basic understanding of:

- Linux commands
- Files and directories
- Users and permissions
- `sudo`
- Basic YAML syntax
- Basic SSH concept
- Basic networking

### Important idea

```text
Python
SSH
```

Ansible connects to target machines using SSH and executes tasks through Python/modules.

---

## 1. What is Ansible?

**Ansible** is an automation tool used to automate tasks on one or more machines.

Instead of manually doing:

```bash
sudo apt update
sudo apt install nginx
sudo systemctl start nginx
```

we can define these tasks in an Ansible Playbook and let Ansible execute them automatically.

---

## 2. Why Use Ansible?

Ansible can be used for:

- Server configuration
- Installing packages
- Starting and stopping services
- Managing users
- Managing files
- Application deployment
- Repeating the same configuration on multiple machines

```text
Manual work
    ↓
Write tasks once
    ↓
Ansible
    ↓
Apply tasks to multiple machines
```

---

## 3. IaC and CMS

### IaC – Infrastructure as Code

Managing infrastructure using configuration/code instead of doing everything manually.

Terraform is mainly used for **Infrastructure Provisioning**.

Ansible is mainly used for **Configuration Management and Automation**.

### CMS – Configuration Management System

Managing the configuration of machines.

Example:

```text
Install nginx
Create user
Copy configuration file
Start nginx
Enable nginx
```

---

## 4. Terraform vs Ansible

| Terraform | Ansible |
|---|---|
| Mainly Infrastructure Provisioning | Mainly Configuration Management |
| Creates infrastructure | Configures existing machines |
| Uses providers | Uses modules |
| Commonly manages cloud resources | Commonly manages servers/software |

Example:

```text
Terraform
   ↓
Create infrastructure
   ↓
Ansible
   ↓
Configure the machines
```

---

## 5. How Ansible Connects

```text
Ansible Controller
       |
       | SSH
       ↓
Target Machine
```

The target machine generally needs Python for Ansible modules to execute.

For local execution:

```text
connection = local
```

---

## 6. Ansible Building Blocks

```text
Inventory
Playbook
Module
Role
```

### Inventory

Defines the machines/hosts Ansible will manage.

```ini
[web]
localhost ansible_connection=local
```

### Playbook

A YAML file containing the tasks Ansible should execute.

### Module

Performs a specific operation.

### Role

A structured way to organize reusable Ansible automation.

---

## 7. Install Ansible on Ubuntu

```bash
sudo apt update
sudo apt install software-properties-common
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt install ansible
```

Check:

```bash
ansible --version
```

---

## 8. `ansible.cfg`

Example:

```ini
[defaults]
inventory = ./inventory
forks = 10
retries = 3
```

---

## 9. Inventory

Example:

```ini
[web]
localhost ansible_connection=local
```

Test it:

```bash
ansible -i inventory web -m ping
```

Meaning:

```text
-i inventory → use inventory file
web           → use web group
-m ping       → use ping module
```

---

## 10. Use a Specific Configuration File

```bash
export ANSIBLE_CONFIG=.ansible/ansible.cfg
```

Check:

```bash
ansible --version
```

---

## 11. Variable Precedence

If the same variable is defined in different locations, Ansible uses precedence to decide which value is used.

For this revision:

```text
Config
   ↓
Playbook / Task
   ↓
Extra Variables
```

**Higher precedence overrides lower precedence.**

Example:

```text
Config        → env=dev
Playbook      → env=stg
Extra (-e)    → env=prod

Final value   → prod
```

Run with an extra variable:

```bash
ansible-playbook playbook.yml -e "env=prod"
```

`-e` means **extra variables**.

---

## 12. First Playbook

```yaml
- name: test
  hosts: localhost
  become: true

  tasks:
    - name: install package
      package:
        name: nginx
        state: present
```

### Main parts

```text
name      → play/task name
hosts     → target host/group
become    → elevated privileges
tasks     → list of operations
module    → performs the operation
```

---

## 13. Start and Enable Nginx

```yaml
- name: start and enable nginx
  service:
    name: nginx
    state: started
    enabled: true
```

Complete example:

```yaml
- name: test
  hosts: localhost
  become: true

  tasks:

    - name: install package
      package:
        name: nginx
        state: present

    - name: start and enable nginx
      service:
        name: nginx
        state: started
        enabled: true
```

---

## 14. Modules

Examples:

```text
package
service
copy
file
command
shell
user
```

Get module documentation:

```bash
ansible-doc ansible.builtin.package
```

Example:

```bash
ansible-doc ansible.builtin.service
```

---

## 15. Run the Playbook

### Check Mode

```bash
ansible-playbook playbook.yml --check
```

Use it to check what Ansible would do before applying changes where check mode is supported.

### Run

```bash
ansible-playbook playbook.yml
```

---

## 16. YAML Basics

Ansible Playbooks use YAML.

Indentation matters:

```yaml
- name: test
  hosts: localhost
  tasks:
    - name: install nginx
      package:
        name: nginx
        state: present
```

Use spaces instead of tabs.

Key/value:

```yaml
name: nginx
state: present
```

Lists:

```yaml
tasks:
  - name: task 1
  - name: task 2
```

---

## 17. Sudoers

For administrative privileges in the Playbook:

```yaml
become: true
```

A sudoers rule used in the lab can be:

```text
user ALL=(ALL:ALL) NOPASSWD: ALL
```

This gives broad sudo privileges, so use it intentionally in a controlled lab.

---

## 18. Conditions

A task can run only when a condition is true.

```yaml
- name: install nginx
  package:
    name: nginx
    state: present
  when: ansible_os_family == "Debian"
```

Flow:

```text
Task
 ↓
Condition
 ↓
True  → Run
False → Skip
```

---

## 19. Filters

Filters modify/process values.

Syntax:

```text
variable | filter
```

Example:

```yaml
{{ name | upper }}
```

---

## 20. Tasks

A **task** is one operation.

```yaml
tasks:

  - name: install nginx
    package:
      name: nginx
      state: present

  - name: start nginx
    service:
      name: nginx
      state: started
```

---

## 21. Handlers

A **handler** is triggered by another task using `notify`.

```yaml
tasks:

  - name: copy nginx config
    copy:
      src: nginx.conf
      dest: /etc/nginx/nginx.conf
    notify: restart nginx

handlers:

  - name: restart nginx
    service:
      name: nginx
      state: restarted
```

Flow:

```text
Task changes something
        ↓
      notify
        ↓
     Handler
```

---

## 22. Template

Ansible can use templates to create configuration files dynamically.

Template files commonly use `.j2`.

`template.j2`:

```jinja2
environment={{ env }}
```

Playbook:

```yaml
- name: create config file
  template:
    src: template.j2
    dest: /tmp/temp-out.yaml
```

If:

```yaml
vars:
  env: dev
```

The generated `temp-out.yaml` contains:

```text
environment=dev
```

Flow:

```text
template.j2
     ↓
Ansible + variables
     ↓
temp-out.yaml
```

---

## 23. YAML Checker

Validate YAML syntax before running the Playbook.

```text
YAML
 ↓
Validate
 ↓
Run Playbook
```

---

## 24. Simple Project Structure

```text
ansible-project/
│
├── ansible.cfg
├── inventory
└── playbook.yml
```

`ansible.cfg`:

```ini
[defaults]
inventory = ./inventory
forks = 10
retries = 3
```

`inventory`:

```ini
[web]
localhost ansible_connection=local
```

`playbook.yml`:

```yaml
- name: test
  hosts: localhost
  become: true

  tasks:
    - name: install nginx
      package:
        name: nginx
        state: present

    - name: start and enable nginx
      service:
        name: nginx
        state: started
        enabled: true
```

---

## 25. Run the Project

```bash
ansible --version
```

```bash
ansible -i inventory web -m ping
```

```bash
ansible-playbook playbook.yml --check
```

```bash
ansible-playbook playbook.yml
```

---

# Quick Revision

```text
Ansible
  ↓
Automation + Configuration Management

Building blocks
  ↓
Inventory
Playbook
Module
Role

Inventory
  ↓
Target hosts

Playbook
  ↓
Tasks

Module
  ↓
Operation

Task
  ↓
One operation

Handler
  ↓
notify → Handler

Template
  ↓
template.j2 → temp-out.yaml
```

### Most Important Commands

```bash
ansible --version

ansible -i inventory web -m ping

ansible-doc ansible.builtin.package

ansible-playbook playbook.yml --check

ansible-playbook playbook.yml

ansible-playbook playbook.yml -e "env=prod"
```

---

# 26. Ansible Labs

These labs practice the main Ansible concepts from this revision: **Playbooks, Modules, Services, Templates, Variables, and Handlers**.

## Lab 1 — Install Nginx

### Goal
Install Nginx using Ansible.

### Playbook

```yaml
- name: Install Nginx
  hosts: localhost
  become: true

  tasks:
    - name: Install nginx
      package:
        name: nginx
        state: present
```

Save it as:

```text
lab1.yml
```

### Run

```bash
ansible-playbook lab1.yml --check
ansible-playbook lab1.yml
```

### Test

```bash
nginx -v
```

### Result

Nginx is installed on the target machine.

---

## Lab 2 — Create Nginx Configuration Using a Template

### Goal
Create an Nginx configuration file from a Jinja2 template instead of writing the final configuration directly in the Playbook.

### Step 1 — Create the template

Create:

```text
nginx.conf.j2
```

Example:

```nginx
server {
    listen 80;
    server_name {{ server_name }};

    root /var/www/html;
    index index.html;
}
```

The variable `{{ server_name }}` will be replaced by Ansible.

### Step 2 — Define the variable

In the Playbook:

```yaml
vars:
  server_name: myname.com
```

Replace `myname.com` with your own hostname.

### Step 3 — Use the template module

```yaml
- name: Create nginx configuration
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/sites-available/my-site
```

### Result

Ansible takes:

```text
nginx.conf.j2
      ↓
Ansible + variables
      ↓
/etc/nginx/sites-available/my-site
```

The generated configuration contains the real hostname instead of `{{ server_name }}`.

---

## Lab 3 — Ensure Nginx Is Running and Enabled

### Goal
Make sure Nginx:

- is running now
- starts automatically when the system boots

### Task

```yaml
- name: Ensure nginx is running and enabled
  service:
    name: nginx
    state: started
    enabled: true
```

### Result

```text
Ansible
   ↓
Nginx service
   ↓
Running + Enabled
```

You can verify it with:

```bash
systemctl status nginx
```

---

## Lab 4— Create Your Own HTML Page and Test Nginx

### Goal
Create a simple HTML page and serve it through Nginx.

### Step 1 — Create the HTML template

Create:

```text
index.html.j2
```

Example:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Ansible Lab</title>
</head>
<body>
    <h1>Hello from {{ server_name }}</h1>
    <p>Nginx is configured using Ansible.</p>
</body>
</html>
```

### Step 2 — Deploy the HTML page

Add this task:

```yaml
- name: Create HTML page
  template:
    src: index.html.j2
    dest: /var/www/html/index.html
```

### Step 3 — Run the Playbook

```bash
ansible-playbook lab.yml --check
ansible-playbook lab.yml
```

### Step 4 — Test

Open in a browser:

```text
http://myname.com
```

Or test from the terminal:

```bash
curl http://myname.com
```

### Expected Result

The browser should show something similar to:

```text
Hello from myname.com
Nginx is configured using Ansible.
```

---

# Complete Lab Flow

```text
1. Install Nginx
        ↓
2. Create nginx.conf.j2
        ↓
3. Generate Nginx configuration with template
        ↓
4. Ensure Nginx is running and enabled
        ↓
5. Add myname.com to /etc/hosts
        ↓
6. Create index.html.j2
        ↓
7. Generate /var/www/html/index.html
        ↓
8. Test with browser or curl
```

## Suggested Project Structure

```text
ansible-nginx-lab/
│
├── ansible.cfg
├── inventory
├── lab.yml
├── nginx.conf.j2
└── index.html.j2
```

## Example Complete Playbook

```yaml
- name: Configure Nginx
  hosts: localhost
  become: true

  vars:
    server_name: myname.com

  tasks:

    - name: Install nginx
      package:
        name: nginx
        state: present

    - name: Create nginx configuration
      template:
        src: nginx.conf.j2
        dest: /etc/nginx/sites-available/my-site

    - name: Add hostname to hosts file
      lineinfile:
        path: /etc/hosts
        line: "127.0.0.1 {{ server_name }}"
        state: present

    - name: Create HTML page
      template:
        src: index.html.j2
        dest: /var/www/html/index.html

    - name: Ensure nginx is running and enabled
      service:
        name: nginx
        state: started
        enabled: true
```

> **Note:** If you create a custom Nginx site configuration, make sure the configuration is actually loaded by Nginx before testing it. Validate the configuration with `nginx -t` if needed.

## Final Checks

```bash
ansible-playbook lab.yml --check
ansible-playbook lab.yml

systemctl status nginx

cat /etc/hosts

nginx -t

curl http://myname.com
```

### Final Result

```text
Ansible
   ↓
Install Nginx
   ↓
Configure Nginx with Jinja2 template
   ↓
Ensure service is running + enabled
   ↓
Configure hostname in /etc/hosts
   ↓
Deploy custom HTML page
   ↓
Test website
   ↓
http://myname.com
```
