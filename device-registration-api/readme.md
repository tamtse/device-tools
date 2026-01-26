## Device Registration API

Internal API for registering user device types.

### Tech Env
- Python 3.11
- FastAPI
- Docker

### How to run locally

Make sure to have python installed locally:

```bash
# Create virtual env
python3 -m venv .venv

# Enable virtual Env
source .venv/bin/activate

# Install dependencies
pip install -r device-registration-api/requirements.txt

# Run the api
cd device-registration-api
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Will watch for changes in these directories: ['xxxx']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [40886] using WatchFiles
INFO:     Started server process [40888]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Then open http://localhost:8000/docs to see the Swagger documentation.

---

### How to run with Docker

Make sure to have Docker installed locally:

```bash
cd device-registration-api
docker build -t device-registration-api:1.0.0 .
docker run -p 8000:8000 -d device-registration-api:1.0.0
```

Then open http://localhost:8000/docs to see the Swagger documentation.

---

### How to deploy on Kubernetes

Kubernetes deployment for the Device Registration API (internal service).

#### Prerequisites

- Kubernetes 1.24+
- kubectl configured
- Access to namespace `device-platform`
- PostgreSQL deployed and running

**Required images:**
- `feugana1g/device-registration-api:latest` (public on Docker Hub)
- `postgres:16` (for database dependency)

---

#### Installation steps

##### Step 1: Create the namespace (if not already created)

```bash
kubectl apply -f ../kubernetes/namespace.yml
```

Expected output:
```
namespace/device-platform created
```

---

##### Step 2: Create secrets and configuration

Create the PostgreSQL secret (contains database credentials):

```bash
kubectl apply -f ../kubernetes/postgres-secrets.yml
```

Create the API configuration:

```bash
kubectl apply -f ../kubernetes/device-registration-api-configMap.yml
```

**Important:** Check that the `DATABASE_URL` in the ConfigMap matches your PostgreSQL credentials:
```yaml
DATABASE_URL: postgresql://user:password@postgres:5432/devices
```

Expected output:
```
secret/postgres-secret created
configmap/device-registration-config created
```

---

##### Step 3: Deploy PostgreSQL (dependency)

If PostgreSQL is not already deployed:

```bash
# Create persistent volume claim
kubectl apply -f ../kubernetes/postgres-pvc.yml

# Deploy PostgreSQL
kubectl apply -f ../kubernetes/postgres-deploy.yml
kubectl apply -f ../kubernetes/postgres-service.yml
kubectl apply -f ../kubernetes/postgres-networkPolicy.yml
```

Wait for PostgreSQL to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=postgres -n device-platform --timeout=120s
```

Expected output:
```
pod/postgres-xxxxx-yyyyy condition met
```

---

##### Step 4: Deploy the Device Registration API

Deploy the API application:

```bash
kubectl apply -f ../kubernetes/device-registration-api-deploy.yml
```

Deploy the service:

```bash
kubectl apply -f ../kubernetes/device-registration-api-service.yml
```

Apply network policies:

```bash
kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-ingress.yml
kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-egress.yml
kubectl apply -f ../kubernetes/hors-ligne-networkPolicy.yml
```

Expected output:
```
deployment.apps/device-registration-api created
service/device-registration-api created
networkpolicy.networking.k8s.io/allow-device-registration-from-statistic created
networkpolicy.networking.k8s.io/allow-device-registration-egress created
networkpolicy.networking.k8s.io/default-deny-all created
```

---

##### Step 5: Check the installation

Check that pods are running:

```bash
kubectl get pods -n device-platform -l app=device-registration-api
```

Expected output:
```
NAME                                      READY   STATUS    RESTARTS   AGE
device-registration-api-xxxxx-aaaaa       1/1     Running   0          45s
device-registration-api-xxxxx-bbbbb       1/1     Running   0          45s
device-registration-api-xxxxx-ccccc       1/1     Running   0          45s
```

Check the service:

```bash
kubectl get svc -n device-platform device-registration-api
```

Expected output:
```
NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
device-registration-api   ClusterIP   10.105.10.109   <none>        8000/TCP   60s
```

Check health status:

```bash
kubectl port-forward -n device-platform svc/device-registration-api 8001:8000
```

In another terminal:
```bash
curl http://localhost:8001/health
```

Expected output:
```json
{"status":"healthy"}
```

Check the Swagger documentation:
```bash
open http://localhost:8001/docs
```

---

#### Configuration

The API is configured with the ConfigMap `device-registration-config`:

```yaml
LOG_LEVEL: INFO
DATABASE_URL: postgresql://user:password@postgres:5432/devices
```

To update configuration:

```bash
kubectl edit configmap device-registration-config -n device-platform
```

Then restart the pods:

```bash
kubectl rollout restart deployment/device-registration-api -n device-platform
```

---

#### Scaling

Scale horizontally:

```bash
kubectl scale deployment/device-registration-api --replicas=5 -n device-platform
```

Enable autoscaling:

```bash
kubectl autoscale deployment device-registration-api \
  --cpu-percent=70 \
  --min=3 \
  --max=10 \
  -n device-platform
```

---

#### Troubleshooting

View logs:

```bash
kubectl logs -n device-platform -l app=device-registration-api --tail=50 -f
```

Describe pod issues:

```bash
kubectl describe pod -n device-platform -l app=device-registration-api
```

**Common issues:**

**Pods stuck in CrashLoopBackOff:**
- Check DATABASE_URL is correct
- Check PostgreSQL is running and accessible
- Check logs for connection errors

**Connection to Postgres fails:**
- Check network policies allow egress to postgres
- Check DNS resolution: `kubectl exec -it <pod-name> -n device-platform -- nslookup postgres`

---

#### Updating the image

Update to a new version:

```bash
kubectl set image deployment/device-registration-api \
  device-registration-api=feugana1g/device-registration-api:1.0.1 \
  -n device-platform
```

Monitor the rollout:

```bash
kubectl rollout status deployment/device-registration-api -n device-platform
```

Rollback if needed:

```bash
kubectl rollout undo deployment/device-registration-api -n device-platform
```

---

#### Cleanup

Remove the API (keep database):

```bash
kubectl delete deployment device-registration-api -n device-platform
kubectl delete service device-registration-api -n device-platform
kubectl delete networkpolicy allow-device-registration-from-statistic -n device-platform
kubectl delete networkpolicy allow-device-registration-egress -n device-platform
kubectl delete configmap device-registration-config -n device-platform
```

Remove everything including database:

```bash
kubectl delete namespace device-platform
```

**Warning:** This will delete all data permanently.
