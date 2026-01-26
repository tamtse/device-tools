## Statistics API

Public-facing API responsible for providing device statistics.

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
pip install -r statistics-api/requirements.txt

# Run the api
cd statistics-api
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
cd statistics-api
docker build -t statistics-api:1.0.0 .
docker run -p 8000:8000 -d statistics-api:1.0.0
```

Then open http://localhost:8000/docs to see the Swagger documentation.

---

### How to deploy on Kubernetes

Kubernetes deployment for the Statistics API (public-facing service).

#### Prerequisites

- Kubernetes 1.24+
- kubectl configured
- Access to namespace `device-platform`
- PostgreSQL deployed and running
- Device Registration API deployed and running

**Required images:**
- `feugana1g/statistics-api:1.0.0` (public on Docker Hub)
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
kubectl apply -f ../kubernetes/statistic-api-configMap.yml
```

**Important:** Verify the configuration in the ConfigMap:
```yaml
DATABASE_URL: postgresql://user:password@postgres:5432/devices
DEVICE_REGISTRATION_API_URL: http://device-registration-api:8000
REQUEST_TIMEOUT_SECONDS: "5"
LOG_LEVEL: INFO
```

Expected output:
```
secret/postgres-secret created
configmap/statistic-api-config created
```

---

##### Step 3: Deploy dependencies

Deploy PostgreSQL (if not already deployed):

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

Deploy Device Registration API (if not already deployed):

```bash
kubectl apply -f ../kubernetes/device-registration-api-configMap.yml
kubectl apply -f ../kubernetes/device-registration-api-deploy.yml
kubectl apply -f ../kubernetes/device-registration-api-service.yml
kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-ingress.yml
kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-egress.yml
```

Wait for Device Registration API to be ready:

```bash
kubectl wait --for=condition=ready pod -l app=device-registration-api -n device-platform --timeout=120s
```

---

##### Step 4: Deploy the Statistics API

Deploy the API application:

```bash
kubectl apply -f ../kubernetes/statistic-api-deploy.yml
```

Deploy the LoadBalancer service:

```bash
kubectl apply -f ../kubernetes/statistic-api-service-lb.yml
```

Apply network policies:

```bash
kubectl apply -f ../kubernetes/statistic-api-networkPolicy-ingress.yml
kubectl apply -f ../kubernetes/statistic-api-networkPolicy-egress.yml
kubectl apply -f ../kubernetes/hors-ligne-networkPolicy.yml
```

Expected output:
```
deployment.apps/statistic-api created
service/statistic-api created
networkpolicy.networking.k8s.io/allow-statistic-api-ingress created
networkpolicy.networking.k8s.io/allow-statistic-egress created
networkpolicy.networking.k8s.io/default-deny-all created
```

---

##### Step 5: Verify the installation

Check that pods are running:

```bash
kubectl get pods -n device-platform -l app=statistic-api
```

Expected output:
```
NAME                             READY   STATUS    RESTARTS   AGE
statistic-api-xxxxx-aaaaa        1/1     Running   0          45s
statistic-api-xxxxx-bbbbb        1/1     Running   0          45s
statistic-api-xxxxx-ccccc        1/1     Running   0          45s
```

Check the LoadBalancer service:

```bash
kubectl get svc -n device-platform statistic-api
```

Expected output:
```
NAME            TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)        AGE
statistic-api   LoadBalancer   10.108.59.90    35.x.x.x        80:30123/TCP   60s
```

**Note:** It may take a few minutes for the `EXTERNAL-IP` to be assigned. You'll see `<pending>` initially.

---

##### Step 6: Access the API

Get the external IP:

```bash
kubectl get svc statistic-api -n device-platform -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

Test the health endpoint:

```bash
EXTERNAL_IP=$(kubectl get svc statistic-api -n device-platform -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl http://$EXTERNAL_IP/health
```

Expected output:
```json
{"status":"healthy"}
```

Access the Swagger documentation:

```bash
open http://$EXTERNAL_IP/docs
```

Or use port-forward for local testing:

```bash
kubectl port-forward -n device-platform svc/statistic-api 8000:80
```

Then open: http://localhost:8000/docs

---

#### Configuration

The API is configured via the ConfigMap `statistic-api-config`:

```yaml
LOG_LEVEL: INFO
REQUEST_TIMEOUT_SECONDS: "5"
DATABASE_URL: postgresql://user:password@postgres:5432/devices
DEVICE_REGISTRATION_API_URL: http://device-registration-api:8000
```

To update configuration:

```bash
kubectl edit configmap statistic-api-config -n device-platform
```

Then restart the pods:

```bash
kubectl rollout restart deployment/statistic-api -n device-platform
```

---

#### Scaling

Scale horizontally:

```bash
kubectl scale deployment/statistic-api --replicas=5 -n device-platform
```

Enable autoscaling:

```bash
kubectl autoscale deployment statistic-api \
  --cpu-percent=70 \
  --min=3 \
  --max=10 \
  -n device-platform
```

View autoscaler status:

```bash
kubectl get hpa -n device-platform
```

---

#### Monitoring

The service exposes Prometheus metrics annotations:

```yaml
annotations:
  prometheus.io/scrape: "true"
  prometheus.io/port: "8000"
  prometheus.io/path: "/metrics"
```

If Prometheus is installed in your cluster, metrics will be automatically scraped.

View current metrics (if /metrics endpoint exists):

```bash
EXTERNAL_IP=$(kubectl get svc statistic-api -n device-platform -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
curl http://$EXTERNAL_IP/metrics
```

---

#### Troubleshooting

View logs:

```bash
kubectl logs -n device-platform -l app=statistic-api --tail=50 -f
```

Describe pod issues:

```bash
kubectl describe pod -n device-platform -l app=statistic-api
```

**Common issues:**

**Pods stuck in CrashLoopBackOff:**
- Check DATABASE_URL is correct
- Verify PostgreSQL is running and accessible
- Verify Device Registration API is running
- Check logs for connection errors

**Connection to Device Registration API fails:**
- Verify device-registration-api service is running
- Check network policies allow egress
- Test DNS: `kubectl exec -it <pod-name> -n device-platform -- nslookup device-registration-api`

**LoadBalancer stuck in Pending:**
- Check if your cluster supports LoadBalancer services
- On local clusters (minikube, kind), use `kubectl port-forward` instead
- Consider using an Ingress controller

**Connection to Postgres fails:**
- Verify network policies allow egress to postgres
- Check DATABASE_URL credentials match postgres-secret

---

#### Updating the image

Update to a new version:

```bash
kubectl set image deployment/statistic-api \
  api=feugana1g/statistics-api:1.0.1 \
  -n device-platform
```

Monitor the rollout:

```bash
kubectl rollout status deployment/statistic-api -n device-platform
```

Rollback if needed:

```bash
kubectl rollout undo deployment/statistic-api -n device-platform
```

View rollout history:

```bash
kubectl rollout history deployment/statistic-api -n device-platform
```

---

#### Cleanup

Remove the API (keep dependencies):

```bash
kubectl delete deployment statistic-api -n device-platform
kubectl delete service statistic-api -n device-platform
kubectl delete networkpolicy allow-statistic-api-ingress -n device-platform
kubectl delete networkpolicy allow-statistic-egress -n device-platform
kubectl delete configmap statistic-api-config -n device-platform
```

Remove everything including database and device-registration-api:

```bash
kubectl delete namespace device-platform
```

**Warning:** This will delete all data permanently.

---

#### Security notes

- The API is publicly accessible via LoadBalancer
- Network policies restrict traffic to:
  - Ingress: from anywhere (0.0.0.0/0) on port 8000
  - Egress: to device-registration-api, postgres, and DNS only
- All containers run as non-root user (UID 1000)
- Read-only root filesystem with writable /tmp volume
- All capabilities dropped

**For production:**
- Consider replacing LoadBalancer with an Ingress + TLS
- Implement authentication/authorization
- Use secrets management (Sealed Secrets, Vault)
- Enable rate limiting
