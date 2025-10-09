# OrchestrateX Google Cloud Deployment Guide

This guide will help you deploy OrchestrateX to Google Cloud with the orchestratex.me domain using minimal changes to your existing files.

## Prerequisites

1. **Google Cloud Account** with billing enabled
2. **Google Cloud SDK** installed on your machine
3. **Domain ownership** of orchestratex.me
4. **Project with required APIs enabled**

## Quick Deployment Steps

### 1. Initialize Google Cloud Project

```powershell
# Authenticate with Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create your-project-id --name="OrchestrateX"

# Set the project
gcloud config set project your-project-id

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

### 2. Deploy to Cloud Run

Run the automated deployment script:

```powershell
.\deploy-orchestratex.ps1
```

This script will:
- ✅ Check Google Cloud SDK installation
- ✅ Enable required APIs (Cloud Build, Cloud Run, Domains)
- ✅ Create optimized production files
- ✅ Build and deploy to Cloud Run
- ✅ Set environment variables
- ✅ Configure domain mapping (optional)

### 3. Manual Steps (if needed)

If you prefer manual deployment:

```powershell
# Set your project ID
$PROJECT_ID = "your-project-id"
gcloud config set project $PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable domains.googleapis.com

# Deploy using Cloud Build
gcloud builds submit --config cloudbuild-production.yaml

# Set environment variables
.\setup-environment.ps1 -ProjectId $PROJECT_ID

# Setup domain (after verification)
.\setup-domain.ps1 -ProjectId $PROJECT_ID
```

## Domain Setup

### 1. Verify Domain Ownership

1. Go to [Domain Verification](https://console.cloud.google.com/apis/credentials/domainverification)
2. Click "Add Domain" and enter `orchestratex.me`
3. Add the provided DNS TXT record to your domain registrar
4. Wait for verification (can take up to 24 hours)

### 2. Configure DNS Records

After domain mapping is created, configure these DNS records at your domain registrar:

```
Type: A
Name: @ (or orchestratex.me)
Value: [IP provided by gcloud]

Type: AAAA
Name: @ (or orchestratex.me)  
Value: [IPv6 provided by gcloud]

Type: CNAME
Name: www
Value: orchestratex.me
```

## Files Created/Modified

### New Files:
- `requirements-production.txt` - Optimized dependencies for Cloud Run
- `Dockerfile.production` - Production-ready Docker configuration
- `cloudbuild-production.yaml` - Cloud Build configuration
- `deploy-orchestratex.ps1` - Automated deployment script
- `setup-environment.ps1` - Environment variables setup
- `setup-domain.ps1` - Domain mapping setup

### Modified Files:
- `.gcloudignore` - Updated to exclude unnecessary files

### Unchanged Files:
- `working_api.py` - Already Cloud Run compatible
- `cloud-env-vars.yaml` - Your API keys and configuration
- Core application logic - No changes needed

## Environment Variables

Your API keys from `cloud-env-vars.yaml` will be automatically set as environment variables in Cloud Run:

- `PROVIDER_GLM45_API_KEY`
- `PROVIDER_GPTOSS_API_KEY`
- `PROVIDER_LLAMA3_API_KEY`
- `PROVIDER_KIMI_API_KEY`
- `PROVIDER_QWEN3_API_KEY`
- `PROVIDER_FALCON_API_KEY`
- All backup keys and model configurations

## Monitoring and Logs

```powershell
# View logs
gcloud run services logs read orchestratex --region=us-central1

# Monitor service
gcloud run services describe orchestratex --region=us-central1

# Test health endpoint
curl https://orchestratex.me/health
```

## URLs

After deployment, your application will be available at:

- **Cloud Run URL**: `https://orchestratex-[hash]-uc.a.run.app`
- **Custom Domain**: `https://orchestratex.me` (after DNS propagation)

## Troubleshooting

### Common Issues:

1. **Domain verification fails**
   - Ensure TXT record is correctly added to DNS
   - Wait for DNS propagation (up to 24 hours)

2. **Environment variables not set**
   - Run: `.\setup-environment.ps1 -ProjectId your-project-id`

3. **Service fails to start**
   - Check logs: `gcloud run services logs read orchestratex --region=us-central1`
   - Verify environment variables are set

4. **Domain mapping fails**
   - Ensure domain is verified first
   - Check IAM permissions

### Support Commands:

```powershell
# Check service status
gcloud run services describe orchestratex --region=us-central1

# Update service
gcloud run services update orchestratex --region=us-central1

# Delete domain mapping (if needed)
gcloud run domain-mappings delete orchestratex.me --region=us-central1

# Redeploy
gcloud builds submit --config cloudbuild-production.yaml
```

## Cost Optimization

Cloud Run pricing is based on:
- **CPU**: 1 vCPU allocated
- **Memory**: 1GB allocated  
- **Requests**: Pay per request
- **Bandwidth**: Egress charges apply

With minimal traffic, monthly costs should be under $10-20.

## Security

- Service runs with default Cloud Run security
- Environment variables are securely stored
- HTTPS enforced automatically
- No persistent storage (stateless)

## Next Steps

1. Test all endpoints after deployment
2. Update any frontend applications to use the new domain
3. Set up monitoring and alerting
4. Configure backup and disaster recovery
5. Implement CI/CD pipeline for automated deployments