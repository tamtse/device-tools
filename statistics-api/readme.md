
  ```markdown
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

  cd statistics-api
  docker build -t statistic-api:1.0.0 .
  docker run -p 8000:8000 -d statistic-api:1.0.0

  Then open http://localhost:8000/docs to see the Swagger documentation.

```
  ### How to deploy on Kubernetes

  Kubernetes deployment for the Statistics API

  #### Prerequisites

  - Kubernetes
  - kubectl configured
  - Access to namespace `device-platform`
  - PostgreSQL deployed and running
  - Device Registration API deployed and running

  **Required images:**
  - `feugana1g/statistic-api:1.0.0` (public on Docker Hub)
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

  kubectl apply -f ../kubernetes/statistic-api-configMap.yml

  ---
  Step 3: Deploy dependencies

  Deploy PostgreSQL (if not already deployed):

  # Create persistent volume claim
  kubectl apply -f ../kubernetes/postgres-pvc.yml

  # Deploy PostgreSQL
  kubectl apply -f ../kubernetes/postgres-deploy.yml
  kubectl apply -f ../kubernetes/postgres-service.yml
  kubectl apply -f ../kubernetes/postgres-networkPolicy.yml

  Deploy Device Registration API (if not already deployed):

  kubectl apply -f ../kubernetes/device-registration-api-configMap.yml
  kubectl apply -f ../kubernetes/device-registration-api-deploy.yml
  kubectl apply -f ../kubernetes/device-registration-api-service.yml
  kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-ingress.yml
  kubectl apply -f ../kubernetes/device-registration-api-networkPolicy-egress.yml

  ---
  Step 4: Deploy the Statistics API

  Deploy the API application:

  kubectl apply -f ../kubernetes/statistic-api-deploy.yml

  Deploy the LoadBalancer service:

  kubectl apply -f ../kubernetes/statistic-api-service-lb.yml

  Apply network policies:

  kubectl apply -f ../kubernetes/statistic-api-networkPolicy-ingress.yml
  kubectl apply -f ../kubernetes/statistic-api-networkPolicy-egress.yml
  kubectl apply -f ../kubernetes/hors-ligne-networkPolicy.yml

  ---
  Step 5: Verify the installation

  Check that pods are running:

  kubectl get pods -n device-platform -l app=statistic-api

  Check the LoadBalancer service:

  kubectl get svc -n device-platform statistic-api


  ---
  Step 6: Access the API

  Get the external IP:

  kubectl get svc statistic-api -n device-platform -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

  Test the health endpoint:

  EXTERNAL_IP=$(kubectl get svc statistic-api -n device-platform -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
  curl http://$EXTERNAL_IP/health

  Expected output:
  {"status":"healthy"}

  Access the Swagger documentation:

  open http://$EXTERNAL_IP/docs

  Or use port-forward for local testing:

  kubectl port-forward -n device-platform svc/statistic-api 8000:80

  Then open: http://localhost:8000/docs