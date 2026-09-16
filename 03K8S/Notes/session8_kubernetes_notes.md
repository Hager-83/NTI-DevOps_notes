#Kubernetes: Pods, Deployments, ReplicaSets & Scaling

## 1. Run a Pod

Create a Pod directly:

```bash
kubectl run pod_name --image=image
```

Example:

```bash
kubectl run nginx --image=nginx
```

Check Pods:

```bash
kubectl get pods
```

Delete a Pod:

```bash
kubectl delete pod nginx
```

---

## 2. Deployment

A Deployment is a higher-level object used to manage Pods and their desired state.

Create a Deployment:

```bash
kubectl create deployment dep1 --image=nginx
```

Check Deployments:

```bash
kubectl get deploy
```

Check ReplicaSets:

```bash
kubectl get rs
```

Check Pods:

```bash
kubectl get pods
```

### Relationship

```text
Deployment
     ↓
ReplicaSet
     ↓
Pod
```

- **Deployment** → manages the desired state and replica count.
- **ReplicaSet** → makes sure the desired number of Pods are running.
- **Pod** → runs the container(s).

---

## 3. Desired State

Kubernetes works with a **desired state**.

For example, if we request:

```text
replicas = 3
```

we want 3 Pods to be running.

```text
Deployment
     ↓
ReplicaSet
     ↓
3 Pods
```

If one Pod is deleted, the ReplicaSet works to create another Pod so the desired number is maintained.

### Important idea

We normally request changes through the **Deployment**, not directly through the ReplicaSet or Pod.

```text
Deployment → ReplicaSet → Pod
```

---

## 4. One Replica = One Pod

When:

```text
replicas = 1
```

the desired state is:

```text
1 Replica → 1 Pod
```

When:

```text
replicas = 3
```

the desired state is:

```text
3 Replicas → 3 Pods
```

---

## 5. Scaling

When we need to increase or decrease the number of Pods, we scale the **Deployment**.

### Syntax

```bash
kubectl scale deployment dep_name --replicas=num_of_replicas
```

### Example

```bash
kubectl scale deployment dep1 --replicas=3
```

Watch the ReplicaSet:

```bash
kubectl get rs -w
```

Check Pods:

```bash
kubectl get pods
```

### Scaling flow

```text
Scale Deployment
      ↓
Deployment changes desired state
      ↓
ReplicaSet works to match it
      ↓
Number of Pods changes
```

---

## 6. Namespaces

Namespaces can be used to separate Kubernetes resources.

Create namespaces:

```bash
kubectl create namespace dev
kubectl create namespace test
```

Create a Deployment inside the `test` namespace:

```bash
kubectl create deployment dep2 --image=nginx -n test
```

Check the Deployment:

```bash
kubectl get deployment -n test
```

The `-n` option specifies the namespace.

---

## 7. Describe a Deployment

To see detailed information:

```bash
kubectl describe deployment dep1
```

---

## 8. Delete a Deployment

```bash
kubectl delete deployment dep1
```

---

# Lab 3 — Deployment, ReplicaSet, Pods & Namespace

## Goal

Practice creating Deployments, checking ReplicaSets and Pods, scaling the Deployment, and using namespaces.

### Step 1 — Create a namespace

```bash
kubectl create namespace dev
```

### Step 2 — Create a Deployment

```bash
kubectl create deployment dep2 --image=nginx -n dev
```

### Step 3 — Check the Deployment

```bash
kubectl get deployment -n dev
```

### Step 4 — Check the ReplicaSet

```bash
kubectl get rs -n dev
```

### Step 5 — Check the Pods

```bash
kubectl get pods -n dev
```

### Step 6 — Scale the Deployment

```bash
kubectl scale deployment dep2 --replicas=3 -n dev
```

### Step 7 — Check the Pods again

```bash
kubectl get pods -n dev
```

Expected relationship:

```text
Deployment dep2
      ↓
ReplicaSet
      ↓
3 Pods
```

---

# 9. Command Practice

Basic workflow:

```bash
kubectl run nginx --image=nginx

kubectl get pods

kubectl delete pod nginx

kubectl create deployment dep1 --image=nginx

kubectl get deploy

kubectl get rs

kubectl get pods
```

Scale:

```bash
kubectl scale deployment dep1 --replicas=3
```

Watch:

```bash
kubectl get rs -w
```

Describe:

```bash
kubectl describe deployment dep1
```

Delete:

```bash
kubectl delete deployment dep1
```

History:

```bash
history
```

---

# 10. Important Concepts

### Pod

Runs the container(s).

```text
Pod → Container(s)
```

### ReplicaSet

Ensures that the desired number of Pods are running.

```text
ReplicaSet → Pods
```

### Deployment

Manages the desired state and controls the ReplicaSet.

```text
Deployment → ReplicaSet → Pods
```

### Scaling

When we need more or fewer Pods:

```text
Scale the Deployment
```

### Desired State

The requested number of replicas represents the desired state.

```text
Desired state = requested number of replicas
```

---

# 11. Quick Revision

```bash
# Create a Pod
kubectl run nginx --image=nginx

# List Pods
kubectl get pods

# Delete a Pod
kubectl delete pod nginx

# Create a Deployment
kubectl create deployment dep1 --image=nginx

# List Deployments
kubectl get deploy

# List ReplicaSets
kubectl get rs

# Describe a Deployment
kubectl describe deployment dep1

# Scale a Deployment
kubectl scale deployment dep1 --replicas=3

# Watch ReplicaSets
kubectl get rs -w

# Create a namespace
kubectl create namespace dev

# Create a Deployment in a namespace
kubectl create deployment dep2 --image=nginx -n dev

# Get a Deployment in a namespace
kubectl get deployment -n dev

# Delete a Deployment
kubectl delete deployment dep1
```

---

# 12. Final Flow

```text
Create Pod
    ↓
kubectl run
    ↓
Pod


Create Deployment
    ↓
Deployment
    ↓
ReplicaSet
    ↓
Pod


Need more Pods?
    ↓
Scale Deployment
    ↓
Change replicas
    ↓
ReplicaSet creates/removes Pods
    ↓
Desired state is reached
```
