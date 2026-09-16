# Session 9 – Kubernetes Notes

## 1. YAML Files

### Why do we use YAML?
- **Declarative configuration**: describe the desired state of the application.
- **Easy to scale and reproduce**: the same file can be applied again.
- Keeps the application's configuration in one place.
- Easy to version and keep as **history** in Git.

### Basic YAML structure

```yaml
apiVersion: v1
kind: Pod

metadata:
  name: pod1
  namespace: lab1
  labels:
    app: nginx
    env: web

spec:
  containers:
    - name: nginx
      image: nginx:latest
```

### Main parts

| Part | Purpose |
|---|---|
| `apiVersion` | API version/group used by the object |
| `kind` | Type of object: `Pod`, `Deployment`, `Service`, ... |
| `metadata` | Name, namespace, labels, etc. |
| `spec` | Desired configuration of the object |

> **Important:** `kind` values are case-sensitive → use `Pod`, `Deployment`, `Service`.

---

## 2. Create a Namespace

```bash
kubectl create namespace lab1
```

---

## 3. Create a Pod from YAML

Apply the file:

```bash
kubectl apply -f pod.yaml
```

Get pods in a namespace:

```bash
kubectl get pods -n lab1
```

Get all pods in all namespaces:

```bash
kubectl get pods -A
```

Show pod labels:

```bash
kubectl get pods -n lab1 --show-labels
```

---

# 4. Deployment

### Architecture

```text
Deployment
    ↓
ReplicaSet
    ↓
Pods
    ↓
Containers
    ↓
Image
```

A Deployment manages ReplicaSets and keeps the required number of Pods running.

### Deployment YAML

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: dep1
  namespace: lab1

spec:
  replicas: 3

  selector:
    matchLabels:
      app: nginx

  template:
    metadata:
      labels:
        app: nginx

    spec:
      containers:
        - name: nginx
          image: nginx:latest
          ports:
            - containerPort: 80

          resources:
            requests:
              cpu: "250m"
              memory: "128Mi"
            limits:
              cpu: "500m"
              memory: "256Mi"
```

### Important

**The Deployment selector must match the labels in the Pod template.**

```yaml
selector:
  matchLabels:
    app: nginx

template:
  metadata:
    labels:
      app: nginx
```

The selector tells the Deployment **which Pods it manages**.

### Generate a Deployment YAML template

```bash
kubectl create deployment dep2 \
  --image=nginx \
  --namespace=lab1 \
  --dry-run=client -o yaml > dep2.yaml
```

Then edit it:

```bash
vim dep2.yaml
```

---

# 5. Services

A **Service** provides a stable way to access Pods.

The Pod/Application network is different from the network used by the PC/Node, so the Service provides the connection between the client and the application.

### Important terms

- `selector` → selects the Pods using their labels.
- `port` → the Service port.
- `targetPort` → the port of the application inside the Pod.
- `nodePort` → the port opened on the Node when using `NodePort`.

**Remember the flow:**

```text
Client → Service → targetPort → Pod/Application
```

### Service → Pod

```text
Client
   ↓
Service
   ↓
Pod / Application
```

The Service acts as the bridge between clients and the selected Pods.

---

## 6. Service Types

### ClusterIP
- Default Service type.
- Used for **internal cluster communication**.
- Not directly exposed outside the cluster.

```yaml
type: ClusterIP
```

### NodePort
- Exposes the Service through a port on the Node.
- Useful for accessing the application from outside the cluster.

```yaml
type: NodePort
```

### LoadBalancer
- Provides an external load balancer when supported by the environment/cloud provider.
- Common for externally accessible applications.

```yaml
type: LoadBalancer
```

---

## 7. NodePort Service YAML

```yaml
apiVersion: v1
kind: Service

metadata:
  name: nginx-service
  namespace: lab1

spec:
  selector:
    app: nginx

  ports:
    - port: 80
      targetPort: 80
      nodePort: 30080

  type: NodePort
```

### Port flow

```text
Client
  ↓
NodeIP:30080
  ↓
Service port:80
  ↓
Pod targetPort:80
  ↓
NGINX
```

> `targetPort` should match the port where the application is listening inside the Pod.

---

## 8. Apply & Check the Service

```bash
kubectl apply -f service.yaml
kubectl apply -f dep.yaml
```

List Services:

```bash
kubectl get svc
```

For Minikube:

```bash
minikube service nginx-service
```

Example:

```text
NAME            TYPE       CLUSTER-IP    PORT(S)
nginx-service   NodePort   10.x.x.x      80:30080/TCP
```

---

# 9. Lab 2 – Useful Commands

Create namespace:

```bash
kubectl create namespace dev
```

Apply YAML:

```bash
kubectl apply -f lab2.yaml
```

Check Pods:

```bash
kubectl get pods -n dev
```

Enter a running container:

```bash
kubectl exec -it <pod-name> -n dev -- /bin/bash
```

Example:

```bash
kubectl exec -it dep2-6b9c86f68c-86znq -n dev -- /bin/bash
```

> `kubectl exec` runs a command **inside a container**.

---

# 10. Lab 3 – Generate Deployment YAML

```bash
kubectl create namespace test
```

Generate the YAML without creating the Deployment yet:

```bash
kubectl create deployment dep3 \
  --image=nginx \
  --namespace=test \
  --dry-run=client -o yaml > lab3.yaml
```

Apply it:

```bash
kubectl apply -f lab3.yaml
```

Check Pods:

```bash
kubectl get pods -n test
```

Show labels:

```bash
kubectl get pods -n test --show-labels
```

Add a label as a column:

```bash
kubectl get pods -n test -L app
```

> `-L <label-key>` displays the value of that label as an extra column.

---

# 11. Quick Practice

### Create + apply

```bash
kubectl create namespace lab1
kubectl apply -f pod.yaml
kubectl get pods -n lab1
```

### Deployment

```bash
kubectl apply -f deployment.yaml
kubectl get pods -n lab1
kubectl get deployment -n lab1
```

### Service

```bash
kubectl apply -f service.yaml
kubectl get svc -n lab1
```

### Enter a container

```bash
kubectl exec -it <pod-name> -n lab1 -- /bin/bash
```

---

## ⭐ Remember

- **YAML** → keeps the configuration of the Kubernetes object.
- `apiVersion` → which API version the object uses.
- `kind` → object type (`Pod`, `Deployment`, `Service`).
- `metadata` → name, namespace, labels.
- `spec` → the required configuration.
- **Deployment → ReplicaSet → Pods → Containers → Image**
- **Selector + labels must match** for the Deployment/Service to select the correct Pods.
- `port` → Service port.
- `targetPort` → Pod/application port.
- `nodePort` → Node access port.
- **ClusterIP** → internal traffic.
- **NodePort** → access through the Node.
- **LoadBalancer** → external access/load balancing.


# 12. Containers

A **Container** is the environment that runs the application inside a Pod.

```text
Deployment
    ↓
ReplicaSet
    ↓
Pod
    ↓
Container
    ↓
Application / Process
```

### Container types you should remember

#### 1. App / Main Container
The normal container that runs the main application.

```yaml
containers:
  - name: nginx
    image: nginx:latest
```

#### 2. Init Container
Runs **before** the main containers start and must finish successfully first.

Useful for:
- Preparing files/configuration.
- Waiting for another service.
- Running initialization tasks.

```yaml
initContainers:
  - name: init
    image: busybox
    command: ["sh", "-c", "echo Initializing..."]
```

**Remember:** `initContainers` → run first → finish → main container starts.

#### 3. Sidecar Container
An additional container in the **same Pod** that supports the main application.

Examples:
- Logging
- Monitoring
- Proxy/helper processes

```yaml
spec:
  containers:
    - name: app
      image: myapp
    - name: sidecar
      image: helper
```

**Remember:** same Pod → containers share the Pod's network and can communicate using `localhost`.

> **Easy memory:**  
> **Main container** = runs the app  
> **Init container** = prepares things first  
> **Sidecar** = helps the app while it runs

### Container vs Pod

- **Container** → runs a process/application.
- **Pod** → the smallest Kubernetes unit and can contain **one or more containers**.
- Containers in the same Pod share networking and can share storage volumes.

### Important YAML difference

For a Pod/Deployment:

```yaml
spec:
  containers:
    - name: nginx
      image: nginx:latest
```

For a Deployment, `containers` is inside the Pod template:

```yaml
spec:
  template:
    spec:
      containers:
        - name: nginx
          image: nginx:latest
```



# 12. Taints & Tolerations

### Taint
A **taint** is placed on a **Node** to prevent Pods from being scheduled on it unless they tolerate the taint.

```bash
kubectl taint nodes <node-name> key=value:NoSchedule
```

Example:

```bash
kubectl taint nodes node1 app=backend:NoSchedule
```

### Toleration
A **toleration** is added to a **Pod** so it can be scheduled on a Node that has a matching taint.

```yaml
spec:
  tolerations:
    - key: "app"
      operator: "Equal"
      value: "backend"
      effect: "NoSchedule"
```

### Easy to remember

```text
Taint       → Node says: "Don't schedule here"
Toleration  → Pod says: "I am allowed to run here"
```

> **Important:** A toleration does **not** force the Pod to run on that Node. It only allows it to be scheduled there.

### Remove a taint

```bash
kubectl taint nodes <node-name> key=value:NoSchedule-
```
