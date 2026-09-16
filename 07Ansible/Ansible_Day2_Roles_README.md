# Ansible Day 2 — Roles

## 1. What are Ansible Roles?

Ansible Roles help us separate one large playbook into multiple files and folders.

Instead of keeping everything in one playbook, we organize reusable parts into a role:

```text
Role
├── defaults
├── vars
├── tasks
├── templates
├── handlers
└── files
```

This makes the project easier to reuse and maintain.

---

## 2. Create a Role

```bash
ansible-galaxy role init role_name
```

Example:

```bash
ansible-galaxy role init install_frontend
```

Ansible creates the role directory with the required subdirectories.

---

## 3. Role Structure

```text
├── install_frontend/
│   ├── defaults/
│   │   └── main.yml
│   ├── files/
│   ├── handlers/
│   │   └── main.yml
│   ├── meta/
│   │   └── main.yml
│   ├── README.md
│   ├── tasks/
│   │   └── main.yml
│   ├── templates/
│   │   ├── index.html.j2
│   │   └── nginx.conf.j2
│   ├── tests/
│   │   ├── inventory
│   │   └── test.yml
│   └── vars/
│       └── main.yml
├── inventory
└── playbook.yaml
```

### Important directories

| Directory | Purpose |
|---|---|
| `defaults/` | Default variables |
| `vars/` | Role variables |
| `tasks/` | Main tasks of the role |
| `templates/` | Jinja2 template files |
| `handlers/` | Handlers triggered by `notify` |
| `files/` | Static files |
| `meta/` | Role metadata/dependencies |
| `tests/` | Role testing files |

### Variable Priority

For the variables we studied:

```text
defaults
   ↓
vars / playbook / task variables
   ↓
extra variables (-e)
```

`defaults` has the lowest priority, so it is easy to override.

---

## 4. Add Code to the Role

After creating the role:

```bash
ansible-galaxy role init install_frontend
```

Open the role directory and add your code to the correct locations:

```text
tasks/       → tasks
templates/   → Jinja2 templates
handlers/    → handlers
defaults/    → default variables
vars/        → role variables
files/       → static files
```

---

## 5. Use the Role in the Playbook

The role is called from the main playbook outside the role directory.

```yaml
- name: Configure frontend
  hosts: web
  become: true

  roles:
    - install_frontend
```

### Flow

```text
playbook.yaml
      ↓
install_frontend role
      ↓
tasks + templates + handlers + variables
      ↓
Configured server
```

---

## 6. Run the Project

Check mode:

```bash
ansible-playbook playbook.yaml --check
```

Run:

```bash
ansible-playbook playbook.yaml
```

---

# Lab 1 — Nginx Using a Role

## Goal

Convert yesterday's Nginx lab into an Ansible Role.

Instead of manually doing:

```text
Install Nginx
      ↓
Create website directory
      ↓
Create Nginx configuration
      ↓
Enable website
      ↓
Remove default website
      ↓
Add domain to /etc/hosts
      ↓
Create HTML page
      ↓
Test Nginx
      ↓
Restart Nginx
      ↓
Enable Nginx at startup
```

we let Ansible automate the process.

### Suggested structure

```text
ansible-nginx-role/
│
├── inventory
├── playbook.yaml
│
└── install_frontend/
    ├── defaults/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── tasks/
    │   └── main.yml
    ├── templates/
    │   ├── index.html.j2
    │   └── nginx.conf.j2
    └── vars/
        └── main.yml
```

### Main idea

```text
Nginx installation        → tasks/main.yml
Nginx configuration       → templates/nginx.conf.j2
HTML page                 → templates/index.html.j2
Restart/reload action     → handlers/main.yml
Default variables         → defaults/main.yml
```

Then the main `playbook.yaml` calls the role.

---

# Lab 2 — Connect to an EC2 Machine

## 1. Generate an SSH Key

On your local machine:

```bash
ssh-keygen
```

Check the public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

Copy the public key.

## 2. Create the EC2 Instance

In the lab environment:

```text
Key Pairs
   ↓
Import Key Pair
   ↓
Add your public key
   ↓
Create Key
```

Then:

```text
Instances
   ↓
Create / Launch Instance
   ↓
Give it a name
   ↓
Choose Ubuntu
   ↓
Select your imported key pair
```

Allow the required:

```text
SSH
HTTP
HTTPS
```

Then launch the instance.

## 3. Connect to the Machine

```bash
ssh ubuntu@PUBLIC_IP
```

Or specify the key:

```bash
ssh -i ~/.ssh/id_ed25519 ubuntu@PUBLIC_IP
```

## 4. Configure the Ansible SSH Key

In `ansible.cfg`:

```ini
[defaults]
private_key_file = /home/yourname/.ssh/id_ed25519
```

This tells Ansible which private key to use for SSH connections.

## 5. Configure the Inventory

```ini
[web]
web-server1 ansible_host=PUBLIC_IP ansible_user=ubuntu
```

Test the connection:

```bash
ansible -i inventory web -m ping
```

Expected result:

```text
web-server1 | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

## 6. Run the Project

```bash
ansible-playbook playbook.yaml
```

---

# Lab 3 — MariaDB Role

## Goal

Create an Ansible Role that automatically configures MariaDB.

Tasks:

1. Install MariaDB using `package`
2. Enable MariaDB
3. Start MariaDB
4. Create a folder under `/opt/<mariadb>/`
5. Deploy the configuration
6. Deploy `initd.sql`
7. Restart MariaDB
8. Create a new database
9. Create a new user
10. Give the user all required permissions on the database
11. Use `initd.sql` to initialize the database

## Suggested Structure

```text
ansible-mariadb/
│
├── inventory
├── playbook.yaml
│
└── mariadb/
    ├── defaults/
    │   └── main.yml
    ├── handlers/
    │   └── main.yml
    ├── tasks/
    │   └── main.yml
    ├── templates/
    │   └── mariadb.conf.j2
    ├── files/
    │   └── initd.sql
    └── vars/
        └── main.yml
```

### Role Flow

```text
playbook.yaml
      ↓
mariadb role
      ↓
Install MariaDB
      ↓
Enable + Start
      ↓
Create directories
      ↓
Deploy config + initd.sql
      ↓
Restart MariaDB
      ↓
Create DB
      ↓
Create User
      ↓
Grant Permissions
      ↓
Initialize DB
```

---

# Important Commands

### Create a role

```bash
ansible-galaxy role init role_name
```

### Check Ansible version

```bash
ansible --version
```

### Test connection

```bash
ansible -i inventory web -m ping
```

### Check a playbook

```bash
ansible-playbook playbook.yaml --check
```

### Run a playbook

```bash
ansible-playbook playbook.yaml
```

### Check module documentation

```bash
ansible-doc ansible.builtin.package
```

### Generate SSH key

```bash
ssh-keygen
```

### Show public key

```bash
cat ~/.ssh/id_ed25519.pub
```

### SSH to EC2

```bash
ssh ubuntu@PUBLIC_IP
```

---

# Quick Revision

```text
                    Ansible Role
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
   defaults/          vars/            tasks/
  variables         variables           tasks
       │                 │                 │
       └─────────────────┼─────────────────┘
                         ↓
                    templates/
                    Jinja2 files
                         │
                         ↓
                    handlers/
                  notify → action
```

### Main Workflow

```text
Create Role
    ↓
Add Tasks / Variables / Templates / Handlers
    ↓
Call Role from playbook.yaml
    ↓
Test with --check
    ↓
Run ansible-playbook
```

### Most Important Commands

```bash
ansible-galaxy role init install_frontend

ansible -i inventory web -m ping

ansible-playbook playbook.yaml --check

ansible-playbook playbook.yaml
```
