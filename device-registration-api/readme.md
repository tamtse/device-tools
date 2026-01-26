## Device Registration API

  Internal API responsible for registering user device types.

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

  Expected output:
  INFO:     Will watch for changes in these directories: ['xxxx']
  INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
  INFO:     Started reloader process [40886] using WatchFiles
  INFO:     Started server process [40888]
  INFO:     Waiting for application startup.
  INFO:     Application startup complete.

  Then open http://localhost:8000/docs to see the Swagger documentation.

  ---
  How to run with Docker

  Make sure to have Docker installed locally:

  cd device-registration-api
  docker build -t device-registration-api:1.0.0 .
  docker run -p 8000:8000 -d device-registration-api:1.0.0

  Then open http://localhost:8000/docs to see the Swagger documentation.

  ---
  
### How to deploy on Kubernetes

  Kubernetes deployment for the Device Registration API (internal service).

  #### Prerequisites

  - Kubernetes
  - kubectl configured
  - Access to namespace `device-platform`
  - PostgreSQL deployed and running

  **Required images:**
  - `feugana1g/device-registration-api:1.0.0-20260121` (public on Docker Hub)
  - `postgres:16` (for database dependency)

  ---

  #### Installation steps

  ##### Step 1: Create the namespace (if not already created)

  ```bash
  kubectl apply -f ../kubernetes/namespace.yml

  Expected output:
  namespace/device-platform created

  ---
  Step 2: Create secrets and configuration

  Create the PostgreSQL secret (contains database credentials):

  kubectl apply -f ../kubernetes/postgres-secrets.yml

  Create the API configuration:

  kubectl apply -f ../kubernetes/device-registration-api-configMap.yml

  Important: Verify the DATABASE_URL in the ConfigMap matches your PostgreSQL credentials:
  DATABASE_URL: postgresql://user:password@postgres:5432/devices

  Expected output:
  secret/postgres-secret created
  configmap/device-registration-config created

  ---
  Step 3: Deploy PostgreSQL (dependency)

  If PostgreSQL is not already deployed:

  # Create persistent volume claim
  kubectl apply -f ../kubernetes/postgres-pvc.yml

  # Deploy PostgreSQL
  kubectl apply -f ../kubernetes/postgres-deploy.yml
  kubectl apply -f ../kubernetes/postgres-service.yml
  kubectl apply -f ../kubernetes/postgres-networkPolicy.yml

  Wait for PostgreSQL to be ready:

  kubectl wait --for=condition=ready pod -l app=postgres -n device-platform --timeout=120s

  Expected output:
  pod/postgres-xxxxx-yyyyy condition met

  ---
  Step 4: Deploy the Device Registration API

  Deploy the API application:

  kubectl apply -f ../kubernetes/device-registration-api-deploy.yml

  Deploy the service:

  kubectl apply -f ../kubernetes/device-registration-api-service.yml

  Apply network policies:

  kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-ingress.yml
  kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-egress.yml
  kubectl apply -f ../kubernetes/hors-ligne-networkPolicy.yml

  Expected output:
  deployment.apps/device-registration-api created
  service/device-registration-api created
  networkpolicy.networking.k8s.io/allow-device-registration-from-statistic created
  networkpolicy.networking.k8s.io/allow-device-registration-egress created
  networkpolicy.networking.k8s.io/default-deny-all created

  ---
  Step 5: Verify the installation

  Check that pods are running:

  kubectl get pods -n device-platform -l app=device-registration-api

  Expected output:
  NAME                                      READY   STATUS    RESTARTS   AGE
  device-registration-api-xxxxx-aaaaa       1/1     Running   0          45s
  device-registration-api-xxxxx-bbbbb       1/1     Running   0          45s
  device-registration-api-xxxxx-ccccc       1/1     Running   0          45s

  Check the service:

  kubectl get svc -n device-platform device-registration-api

  Expected output:
  NAME                      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
  device-registration-api   ClusterIP   10.105.10.109   <none>        8000/TCP   60s

  Verify health status:

  kubectl port-forward -n device-platform svc/device-registration-api 8001:8000

  In another terminal:
  curl http://localhost:8001/health

  Expected output:
  {"status":"healthy"}

  Check the Swagger documentation:
  open http://localhost:8001/docs