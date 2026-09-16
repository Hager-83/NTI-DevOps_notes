# Session 6 — Docker

## 1. What is Docker?

**Docker** is a containerization platform used to package and run applications with their dependencies in an **isolated environment**.

### Container vs Virtual Machine

- **VM:** Each VM has its own Guest OS + applications and usually needs a **hypervisor**.
- **Container:** Containers share the **host OS kernel** and contain only what the application needs.
- Containers are therefore usually **lighter and faster** than VMs.

```text
Virtual Machines                 Containers
-----------------                -----------------
App 1       App 2                App 1       App 2
Guest OS    Guest OS             Container   Container
-----------------                -----------------
Hypervisor                       Docker Engine
Host OS                          Host OS
Host Hardware                    Host Hardware
```

---

## 2. Docker Architecture

Docker mainly works through:

```text
Docker CLI (Client)
       |
       | request
       v
Docker Daemon
       |
       +---- Container 1
       +---- Container 2
       +---- Container 3
```

- **Docker Client / CLI:** where we type commands such as `docker run`.
- **Docker Daemon:** receives requests and manages images, containers, networks and volumes.
- **Container:** the running environment for the application.

---

## 3. Image vs Container

### Docker Image

An **image** is a read-only blueprint/template containing the application, dependencies and required environment.

One image can be used to create **multiple containers**.

```text
Image
  |
  +---- Container 1
  +---- Container 2
  +---- Container 3
```

### Container

A **container** is a running instance of an image.

```text
docker run IMAGE
       ↓
   Container
```

A container has its own isolated environment and process space.

---

## 4. Registry

A **registry** stores Docker images.

Example flow:

```text
Registry → docker pull → Local Image → docker run → Container
```

```bash
docker pull IMAGE_NAME
```
Download an image from a registry.

```bash
docker run IMAGE_NAME
```
Create and start a container from an image.

---

# 5. Basic Docker Commands

### Check Docker

```bash
docker ps
```
Show **running containers only**.

```bash
docker ps -a
```
Show **all containers**, including stopped ones.

```bash
docker images
```
List images available locally.

```bash
docker run hello-world
```
Test Docker by downloading/using `hello-world` and running a container.

For a new terminal after Docker group changes:

```bash
newgrp docker
```
Refresh the current shell so the new Docker-group membership is applied.

---

# 6. Create and Run Containers

```bash
docker run IMAGE_NAME
```
Create and start a container using the default/latest tag.

```bash
docker run IMAGE_NAME:TAG
```
Run a specific image version.

Example:

```bash
docker run nginx
docker run nginx:1.27
```

### Run in the Background

```bash
docker run -d IMAGE_NAME
```

`-d` = **detached mode**.

The container runs in the background instead of keeping the terminal attached to it.

Similar idea:

```bash
sleep 100 &
```

---

# 7. Stop and Start Containers

```bash
docker stop CONTAINER_ID
```
Stop a running container.

```bash
docker start CONTAINER_ID
```
Start a stopped container again.

Check the result:

```bash
docker ps
docker ps -a
```

Every container has an **ID** and can also have a **name**.

---

# 8. Remove Containers and Images

```bash
docker rm CONTAINER_ID
```
Remove a stopped container.

```bash
docker rmi IMAGE_NAME
```
Remove an image.

```bash
docker rmi IMAGE_NAME:TAG
```
Remove a specific tagged version.

### Important

You normally cannot remove an image while containers based on it still exist/use it.

Typical order:

```text
Stop container
      ↓
Remove container
      ↓
Remove image
```

---

# 9. Execute Commands Inside a Container

The container must be **running**.

```bash
docker exec CONTAINER_ID cat /etc/...
```
Execute a command inside a running container.

```bash
docker exec -it CONTAINER_ID bash
```
Open an interactive terminal inside the container.

- `-i` → interactive
- `-t` → terminal

If `bash` is not available, some small images use:

```bash
docker exec -it CONTAINER_ID sh
```

---

# 10. Port Mapping

Containers have their own network space, so a service running inside the container may need to be exposed to the host.

```bash
docker run -d -p 8080:80 nginx
```

Format:

```text
-p HOST_PORT:CONTAINER_PORT
```

Here:

```text
Host                 Container
8080  ------------>  80
```

- `8080` = port on your machine
- `80` = port used by the application inside the container

Then open:

```text
http://localhost:8080
```

The container port depends on the application/image and should be known from the application's configuration/documentation.

---

# 11. Logs

```bash
docker logs CONTAINER_ID
```

Show the output/logs of a container.

Useful when:

- the application does not work
- the container stops
- you want to find an error
- you want to see what the application is doing

---

# 12. Inspect

```bash
docker inspect CONTAINER_ID
```

Show detailed information about a container, such as its configuration, network, mounts and other settings.

---

# 13. Environment Variables

Environment variables can be passed into a container using `-e`.

```bash
docker run --name test-env -e MY_NAME=Hager nginx
```

Format:

```bash
-e VARIABLE_NAME=VALUE
```

Example:

```bash
docker run --name app5 \
  -p 9000:80 \
  -e PASS=123 \
  -d \
  nginx
```

Inside the container, the application can read `PASS`.

---

# 14. Persistent Volumes

Containers are not the best place to keep important persistent data because the container itself can be removed.

A **Docker volume** stores data outside the container and can be reused by other containers.

### Create a Volume

```bash
docker volume create nginx-volume
```

### List Volumes

```bash
docker volume ls
```

### Inspect a Volume

```bash
docker volume inspect nginx-volume
```

### Remove a Volume

```bash
docker volume rm nginx-volume
```

### Mount a Volume

```bash
docker run -d -v nginx-volume:/app nginx
```

Format:

```bash
-v VOLUME_NAME:CONTAINER_PATH
```

Example:

```text
nginx-volume  →  /app
```

The same volume can be mounted by another container.

---

# 15. Bind Mount

We can also connect a directory/file from the host machine to a directory inside the container.

```bash
-v HOST_PATH:CONTAINER_PATH
```

Example:

```bash
docker run -d -v /home/user/app:/app nginx
```

This is useful when we want the container to access files directly from the host.

### Volume vs Bind Mount

```text
Named Volume:
docker-volume → /app

Bind Mount:
host-directory → /app
```

---

# 16. Restart Policy

A container can be configured to restart automatically when it stops/crashes.

Use the `--restart` flag with `docker run`.

Example:

```bash
docker run -d --restart unless-stopped nginx
```

The restart policy depends on the required behavior of the application.

---

# 17. Resource Isolation

Docker provides isolation using Linux features such as:

### Namespaces
Provide isolation for things such as processes and networking.

### cgroups
Control/limit resources allocated to a container, such as:

- CPU
- Memory

Example:

```text
Container
 ├── isolated environment → Namespaces
 └── resource limits      → cgroups
```

---

# 18. Useful Full Example

```bash
docker volume create nginx-volume

docker run --name app5 \
  -p 9000:80 \
  -e PASS=123 \
  -d \
  -v nginx-volume:/app \
  nginx

docker ps

docker logs app5

docker inspect app5

docker exec -it app5 bash

docker stop app5

docker start app5

docker rm app5
```

If the container is removed, the **named volume can still exist**, so its data can be reused by another container.

---

# 19. Command Flow

### Image → Container

```text
docker pull
     ↓
docker run
     ↓
docker ps
     ↓
docker exec / logs / inspect
     ↓
docker stop
     ↓
docker start
     ↓
docker rm
```

### Persistent Data

```text
docker volume create
        ↓
docker run -v
        ↓
Container uses the volume
        ↓
Container can be removed
        ↓
Volume remains
        ↓
Another container can reuse it
```

### Quick Command Reference

| Command | Purpose |
|---|---|
| `docker ps` | Running containers |
| `docker ps -a` | All containers |
| `docker images` | Local images |
| `docker pull IMAGE` | Download image |
| `docker run IMAGE` | Create + start container |
| `docker run -d IMAGE` | Run in background |
| `docker stop ID` | Stop container |
| `docker start ID` | Start container |
| `docker rm ID` | Remove container |
| `docker rmi IMAGE` | Remove image |
| `docker exec -it ID bash` | Enter container |
| `docker logs ID` | View logs |
| `docker inspect ID` | Detailed information |
| `docker volume create NAME` | Create volume |
| `docker volume ls` | List volumes |
| `docker volume inspect NAME` | Inspect volume |
| `docker volume rm NAME` | Remove volume |

-------------------
-------------------

## Docker cmds from pptx 

```
docker run image_name 

docker ps

docker ps -a 

docker stop container_id/container_name

Docker start container_id/container_name

docker rm container_id/container_name

docker images

docker rmi image_name/image_id

docker pull image_name

docker exec container_name/container_id command

docker exec -d container_name/container_id command

docker exec -it container_name/container_id command

docker logs container_nmae/container_id

-e variable_name=value 

-v host_path:container_path 

docker volume create volume_name

-v volume_name:path

--mount source=volume_name,target=path
```