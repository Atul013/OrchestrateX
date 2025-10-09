# GitHub Continuous Deployment Setup for OrchestrateX

## Step 1: Prepare Your Repository

### 1.1 Ensure Required Files are in GitHub
Make sure these files are in your GitHub repository:
```
├── working_api.py
├── rate_limit_handler.py  
├── api_key_rotation.py
├── requirements-production.txt
├── Dockerfile.production
├── cloudbuild-production.yaml
└── .gcloudignore
```

### 1.2 Push Latest Changes
```bash
git add .
git commit -m "Add Cloud Run deployment configuration"
git push origin main
```

## Step 2: Connect GitHub to Cloud Run

### 2.1 In Cloud Run Console
1. Go to: https://console.cloud.google.com/run
2. Click "Create Service"
3. Select "Continuously deploy from a repository"
4. Click "Set up with Cloud Build"

### 2.2 Connect Repository
1. Select "GitHub" as source
2. Click "Connect New Repository"
3. Authenticate with GitHub
4. Select repository: `Atul013/OrchestrateX`
5. Select branch: `main`

### 2.3 Build Configuration
**Build Type:** Dockerfile
**Source location:** `/Dockerfile.production`

### 2.4 Service Configuration
```
Service name: orchestratex
Region: us-central1
CPU allocation: CPU is only allocated during request processing
Ingress: Allow all traffic
Authentication: Allow unauthenticated invocations
```

### 2.5 Advanced Settings
```
Container port: 8080
Memory: 1 GiB
CPU: 1
Maximum number of instances: 10
Minimum number of instances: 0
Request timeout: 300 seconds
```

## Step 3: Environment Variables

After deployment, set environment variables:
```powershell
# Get your project ID
$PROJECT_ID = "your-project-id"

# Set environment variables from cloud-env-vars.yaml
.\setup-environment.ps1 -ProjectId $PROJECT_ID
```

## Step 4: Domain Mapping

```powershell
# Set up custom domain
.\step4-setup-domain-mapping.ps1
```

## Step 5: Automatic Deployments

Now every time you push to GitHub:
1. Code changes are detected
2. Cloud Build automatically builds new image
3. Cloud Run deploys the new version
4. Zero downtime deployment

## Benefits of GitHub Integration

✅ **Automatic CI/CD**: Push to deploy
✅ **Version History**: Easy rollbacks
✅ **Collaboration**: Team-friendly
✅ **Build Logs**: Debug build issues
✅ **Security**: No local credentials needed
✅ **Scalability**: Handles traffic spikes

## Alternative: Quick Container Deploy

If you want to deploy immediately without GitHub setup:
```powershell
# Use the container image option with our pre-built setup
.\deploy-direct.ps1
```

This will build and deploy directly from your local files.