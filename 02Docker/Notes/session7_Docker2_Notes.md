# Session 7 – Docker Day 2 Notes

## 1. Image from an Existing Container

`docker commit` saves the current state of a container as a new image.

```bash
docker commit CONTAINER_ID IMAGE_NAME:TAG
```

**Example:**
```bash
docker commit app1 myapp:v1
```

> Usually, **Dockerfile + `docker build`** is preferred because it is repeatable and documented.

---

## 2. Dockerfile

A **Dockerfile** is a text file containing instructions used to build an image.

### Example

```dockerfile
FROM php:7.4-apache

WORKDIR /var/www/html

COPY . .

RUN apt-get update && apt-get install -y package_name

CMD ["apache2-foreground"]
```

### Important

- `FROM` → base image.
- `WORKDIR` → working directory for following instructions.
- `COPY . .` → copy the build context into the current `WORKDIR`.
- `RUN` → runs during **image build**.
- `CMD` → default command when a container starts.

> `php:7.4-apache` is an old PHP version. For a real project, use a currently supported version when possible.

---

## 3. Build the Image

```bash
docker build -t IMAGE_NAME:TAG .
```

**Example:**
```bash
docker build -t myapp:v1 .
```

- `-t` → name/tag the image.
- `.` → build context (current directory).

Check images:

```bash
docker images
```

Or:

```bash
docker image ls
```

### Useful

```bash
docker build --no-cache -t myapp:v1 .
```

`--no-cache` → build without using the previous build cache.

---

## 4. Run the Image

```bash
docker run -d --name CONTAINER_NAME -p HOST_PORT:CONTAINER_PORT IMAGE_NAME:TAG
```

**Example:**
```bash
docker run -d --name web -p 8080:80 myapp:v1
```

- `-d` → detached/background mode.
- `--name` → give the container a name.
- `-p` → map host port to container port.

---

## 5. Execute Commands Inside a Container

The container must be **running**.

```bash
docker exec -it CONTAINER_ID_OR_NAME bash
```

If `bash` is not available:

```bash
docker exec -it CONTAINER_ID_OR_NAME sh
```

Run one command:

```bash
docker exec CONTAINER_ID_OR_NAME ls /app
```

---

# 6. Docker Hub – Login

```bash
docker login -u USERNAME
```

Docker Hub can use a **Personal Access Token (PAT)** instead of your password.

---

# 7. Tag → Push → Pull

Docker Hub image names normally follow:

```text
USERNAME/REPOSITORY:TAG
```

### Tag an existing image

```bash
docker tag IMAGE_NAME:OLD_TAG USERNAME/REPOSITORY:NEW_TAG
```

**Example:**
```bash
docker tag myapp:v1 hager/myapp:v1
```

The new tag is another reference to the same image.

Check:

```bash
docker images
```

### Push

```bash
docker push USERNAME/REPOSITORY:TAG
```

**Example:**
```bash
docker push hager/myapp:v1
```

### Pull

```bash
docker pull USERNAME/REPOSITORY:TAG
```

**Example:**
```bash
docker pull hager/myapp:v1
```

---

# 8. Dockerfile Instructions ⭐

| Instruction | What it does | Example |
|---|---|---|
| `FROM` | Selects base image | `FROM ubuntu:24.04` |
| `RUN` | Executes during build | `RUN apt-get update` |
| `CMD` | Default container command | `CMD ["python3","app.py"]` |
| `ENTRYPOINT` | Main executable | `ENTRYPOINT ["python3"]` |
| `ENV` | Sets runtime environment variable | `ENV APP_ENV=prod` |
| `ARG` | Build-time variable | `ARG VERSION=1.0` |
| `COPY` | Copies files | `COPY . /app` |
| `ADD` | Adds files; has extra features | `ADD app.tar /app` |
| `WORKDIR` | Sets working directory | `WORKDIR /app` |
| `USER` | Sets user | `USER appuser` |
| `EXPOSE` | Documents intended container port | `EXPOSE 80` |

### Important: `EXPOSE`

```dockerfile
EXPOSE 80
```

`EXPOSE` **does not publish the port**.

You still need:

```bash
docker run -p 8080:80 IMAGE_NAME
```

---

# 9. COPY vs ADD

### COPY

Use `COPY` for normal file/directory copying.

```dockerfile
COPY . /app
COPY package.json /app/
```

### ADD

`ADD` can also handle some extra features, such as local tar archives.

```dockerfile
ADD app.tar /app/
```

**Rule:** Prefer `COPY` unless you specifically need an `ADD` feature.

---

## Dockerfile Without CMD or ENTRYPOINT

A Dockerfile **does not have to contain** `CMD` or `ENTRYPOINT`.

Example:

```dockerfile
FROM ubuntu

RUN apt-get update && apt-get install -y nginx
```

Build it normally:

```bash
docker build -t myimage .
```

You can provide a command when starting the container:

```bash
docker run -it myimage bash
```

Here, `bash` becomes the command started in the container.

### Why can the container exit?

A container stays alive while its **main process (PID 1)** is running.

If there is no suitable default command or entrypoint, Docker may have no long-running process to keep the container alive. If the main process finishes immediately, the container stops.

For example:

```bash
docker run myimage
```

may start and then exit.

But:

```bash
docker run -it myimage bash
```

keeps the container running while the interactive `bash` process is running.

⭐ **Remember:**

- `CMD` and `ENTRYPOINT` are **optional**.
- A container needs a running **main process (PID 1)** to stay alive.
- You can provide the command at runtime if the image does not define a suitable default.

---

# 10. CMD vs ENTRYPOINT ⭐⭐⭐

### CMD

Provides the **default command/arguments**.

```dockerfile
CMD ["echo", "Hello"]
```

Run:

```bash
docker run myimage
```

Output:

```text
Hello
```

You can replace the CMD:

```bash
docker run myimage Hi
```

---

### ENTRYPOINT

Defines the main executable.

```dockerfile
ENTRYPOINT ["echo"]
```

Then:

```bash
docker run myimage Hello
```

means approximately:

```text
echo Hello
```

To replace the entrypoint:

```bash
docker run --entrypoint sleep myimage 5
```

### Use them together

```dockerfile
ENTRYPOINT ["echo"]
CMD ["Hello, World!"]
```

```bash
docker run myimage
```

→ `echo Hello, World!`

```bash
docker run myimage Hager
```

→ `echo Hager`

**Remember:**

```text
ENTRYPOINT → main executable
CMD        → default arguments
```

> In practice, the **exec form** (`["command", "arg"]`) is usually preferred.

---

# 11. PID 1

The process started as the container's main process normally becomes **PID 1**.

It is **not always the CMD itself**. It depends on the final command/entrypoint that Docker starts.

Check:

```bash
docker exec CONTAINER_ID ps aux
```

Or inside the container:

```bash
ps aux
```

---

# 12. Layered Architecture

Docker images are built from layers.

Filesystem-changing instructions such as:

```dockerfile
RUN
COPY
ADD
```

normally create filesystem layers.

Instructions such as:

```dockerfile
CMD
ENTRYPOINT
ENV
ARG
EXPOSE
WORKDIR
USER
```

mainly add image metadata/configuration rather than filesystem layers.

### Why layers?

- **Caching** → unchanged build steps can be reused.
- **Faster builds** → only affected steps need rebuilding.
- **Image sharing** → layers can be reused between images.

### Order matters ⭐

Example:

```dockerfile
COPY . .
RUN apt-get update
```

If the copied files change, the cache for later steps may be invalidated.

A better pattern is often:

```dockerfile
COPY package.json .
RUN install_dependencies
COPY . .
```

So dependency installation can remain cached when only application code changes.

View layers:

```bash
docker history IMAGE_NAME
```

---

# 13. Intermediate Containers

During `docker build`, Docker creates temporary build containers/stages to execute build instructions.

For example:

```dockerfile
RUN apt-get update
RUN apt-get install -y curl
```

Docker executes these steps during the build and stores the resulting image data/layers.

Temporary build containers are not your final application container.

---

# 14. ENV vs ARG ⭐⭐⭐

## ENV

Available in the resulting image/container environment.

```dockerfile
ENV NAME=Ali
```

Check inside the container:

```bash
echo $NAME
```

---

## ARG

Available during **build time**.

```dockerfile
ARG NAME=Ali
RUN echo $NAME
```

Build:

```bash
docker build --build-arg NAME=Hager -t myapp .
```

### Important difference

```text
ARG → build time
ENV → runtime environment
```

### Why `RUN export` is not enough

```dockerfile
RUN export NAME=Ali
```

The variable exists only in that build step/shell. It does not automatically become an environment variable in the final container.

---

# 15. `.dockerignore`

`.dockerignore` prevents unnecessary files from being sent as the **build context**.

Useful when using:

```dockerfile
COPY . .
```

Example `.dockerignore`:

```text
.git
node_modules
*.log
.env
```

This can make builds faster and avoid copying unwanted files.

---

# 16. Multi-Stage Build ⭐⭐⭐

Use multiple stages when you need build tools/dependencies but do not need them in the final image.

### Example

```dockerfile
# Stage 1: Build
FROM node:22 AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build


# Stage 2: Final
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html
```

### Idea

```text
Stage 1
Large image
Build tools + dependencies
        ↓
     build app
        ↓
Stage 2
Small image
Only files needed to run
```

The final image does **not** automatically contain all previous stages. Only files explicitly copied with `COPY --from=...` are brought into the final stage.

---

# 17. Docker Compose

Docker Compose is used to define and manage **multiple containers/services** for one application.

Example:

```text
Frontend
   ↓
Backend
   ↓
Database
```

A Compose file can define these as separate services.

Basic command:

```bash
docker compose up
```

Run in background:

```bash
docker compose up -d
```

Stop/remove the Compose application:

```bash
docker compose down
```

> Compose does **not** mean putting frontend, backend, and database inside one container. Usually, each service runs in its own container.

---

# 18. Docker Networks

Common network modes:

### Bridge

Default network mode for normal containers.

```bash
docker run --network=bridge IMAGE_NAME
```

### Host

Container shares the host's network namespace.

```bash
docker run --network=host IMAGE_NAME
```

### None

No network connectivity.

```bash
docker run --network=none IMAGE_NAME
```

### Create your own network ⭐

```bash
docker network create mynet
```

Run containers on it:

```bash
docker run -d --name app --network=mynet myapp
docker run -d --name db --network=mynet mysql
```

User-defined bridge networks allow containers to communicate using container/service names.

List networks:

```bash
docker network ls
```

Inspect:

```bash
docker network inspect mynet
```

---

# 19. `docker cp`

Copy files between the host and a container.

### Host → Container

```bash
docker cp file.txt CONTAINER_NAME:/app/
```

### Container → Host

```bash
docker cp CONTAINER_NAME:/app/file.txt .
```

**Example:**

```bash
docker cp index.html web:/var/www/html/
```

---

# 20. Useful Inspection Commands

### Inspect an image

```bash
docker image inspect IMAGE_NAME
```

### Inspect a container

```bash
docker inspect CONTAINER_NAME
```

### See image layers

```bash
docker history IMAGE_NAME
```

### See running containers

```bash
docker ps
```

### See all containers

```bash
docker ps -a
```

---

# ⭐ Final Cheat Sheet

```text
FROM        → base image
RUN         → execute during build
COPY        → copy files
WORKDIR     → working directory
ENV         → runtime environment variable
ARG         → build-time variable
EXPOSE      → document container port
CMD         → default command/arguments
ENTRYPOINT  → main executable
USER        → user for running commands
```

```text
ARG         → build time
ENV         → runtime environment

RUN/COPY/ADD → filesystem layers

CMD         → easy to override with docker run arguments
ENTRYPOINT  → override with --entrypoint

.dockerignore → exclude unnecessary build-context files

Multi-stage → build with a large image,
              run with a small final image

Compose     → manage multiple services/containers
Network     → connect/isolate containers
```


## Best Practice — Run Containers as a Non-Root User

By default, many containers run as `root`.  
Root has full privileges inside the container, so running the application as a non-root user is safer.

### Create a user in the Dockerfile

```dockerfile
FROM ubuntu

RUN useradd -m appuser

USER appuser

CMD ["bash"]
```

- `useradd -m appuser` → creates a new user and home directory.
- `USER appuser` → makes `appuser` the default user for the following instructions and for the container at runtime.
- Now, when someone uses `docker exec` without specifying `-u`, the command runs as `appuser`, not `root`.

### Check the current user

```bash
docker exec container_name whoami
```

Example output:

```text
appuser
```

### Run a command as root only when needed

```bash
docker exec -u root container_name bash
```

`-u` (`--user`) lets you override the default container user for that command.

⭐ **Best practice:** Run applications as a non-root user whenever possible. Use `root` only for tasks that actually require elevated privileges.
