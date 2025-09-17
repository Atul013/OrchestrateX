#!/usr/bin/env python3
"""
Deploy OrchestrateX to Google Cloud Run
"""

import subprocess
import os
import json

def create_deployment_files():
    """Create necessary deployment files"""
    
    # 1. Create Dockerfile optimized for Cloud Run
    dockerfile_content = """FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Expose the port
EXPOSE 8080

# Run the application
CMD ["python", "working_api.py"]
"""
    
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)
    
    # 2. Create Cloud Run specific requirements.txt
    requirements_content = """flask==2.3.3
flask-cors==4.0.0
google-cloud-firestore==2.21.0
firebase-admin==7.1.0
requests==2.32.5
"""
    
    with open("requirements.txt", "w") as f:
        f.write(requirements_content)
    
    # 3. Create Cloud Run service YAML
    cloudrun_yaml = """apiVersion: serving.knative.dev/v1
kind: Service
metadata:
  name: orchestratex-api
  annotations:
    run.googleapis.com/ingress: all
spec:
  template:
    metadata:
      annotations:
        run.googleapis.com/cpu-throttling: "false"
        run.googleapis.com/memory: "512Mi"
        run.googleapis.com/max-scale: "10"
    spec:
      containerConcurrency: 80
      containers:
      - image: gcr.io/PROJECT_ID/orchestratex-api
        ports:
        - containerPort: 8080
        env:
        - name: PORT
          value: "8080"
        resources:
          limits:
            cpu: "1"
            memory: "512Mi"
"""
    
    with open("cloudrun.yaml", "w") as f:
        f.write(cloudrun_yaml)
    
    # 4. Create .dockerignore
    dockerignore_content = """__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.env
.venv
pip-log.txt
.git
.gitignore
README.md
Dockerfile
.dockerignore
temp_storage/
*.log
"""
    
    with open(".dockerignore", "w") as f:
        f.write(dockerignore_content)
    
    print("✅ Deployment files created!")

def deploy_to_cloud_run():
    """Deploy to Google Cloud Run"""
    
    print("🚀 Deploying to Google Cloud Run...")
    
    # Step 1: Build and push container
    print("📦 Building container...")
    subprocess.run([
        "gcloud", "builds", "submit", 
        "--tag", "gcr.io/PROJECT_ID/orchestratex-api"
    ])
    
    # Step 2: Deploy to Cloud Run
    print("🌐 Deploying to Cloud Run...")
    subprocess.run([
        "gcloud", "run", "deploy", "orchestratex-api",
        "--image", "gcr.io/PROJECT_ID/orchestratex-api",
        "--platform", "managed",
        "--region", "us-central1",
        "--allow-unauthenticated",
        "--port", "8080",
        "--memory", "512Mi",
        "--cpu", "1",
        "--max-instances", "10"
    ])

def main():
    print("🚀 OrchestrateX Cloud Deployment Setup")
    print("=" * 50)
    
    # Check if gcloud is installed
    try:
        result = subprocess.run(["gcloud", "version"], capture_output=True, text=True)
        print("✅ Google Cloud SDK is installed")
    except FileNotFoundError:
        print("❌ Google Cloud SDK not found!")
        print("   Install from: https://cloud.google.com/sdk/docs/install")
        return
    
    # Create deployment files
    create_deployment_files()
    
    print("\n📋 Next Steps:")
    print("1. Set your project ID:")
    print("   gcloud config set project YOUR_PROJECT_ID")
    print("2. Enable required APIs:")
    print("   gcloud services enable run.googleapis.com")
    print("   gcloud services enable cloudbuild.googleapis.com")
    print("3. Deploy:")
    print("   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/orchestratex-api")
    print("   gcloud run deploy orchestratex-api --image gcr.io/YOUR_PROJECT_ID/orchestratex-api --platform managed --region us-central1 --allow-unauthenticated")
    
    print("\n💰 Estimated Monthly Cost:")
    print("   • Free tier: 2 million requests/month")
    print("   • After free tier: ~$0.40 per million requests")
    print("   • Container storage: ~$0.10/month")
    print("   • Firestore: Free for your usage level")

if __name__ == "__main__":
    main()