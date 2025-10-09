# Manual Deployment Steps for OrchestrateX

## Before You Start

1. **Create a Google Cloud Project**:
   - Go to https://console.cloud.google.com/projectcreate
   - Create a new project with a unique ID (e.g., `orchestratex-2024-yourname`)
   - Enable billing for the project

2. **Set up permissions**:
   - Make sure you have `Cloud Run Admin` and `Cloud Build Editor` roles

## Quick Commands

```powershell
# 1. Set your project (replace with your actual project ID)
gcloud config set project YOUR-PROJECT-ID

# 2. Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com domains.googleapis.com

# 3. Deploy using Cloud Build
gcloud builds submit --config cloudbuild-production.yaml

# 4. Set environment variables
.\setup-environment.ps1 -ProjectId YOUR-PROJECT-ID

# 5. Set up domain (optional)
.\setup-domain.ps1 -ProjectId YOUR-PROJECT-ID
```

## Alternative: Direct Deploy

If Cloud Build doesn't work, try direct deployment:

```powershell
# Build locally and deploy
gcloud run deploy orchestratex `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --port 8080 `
  --memory 1Gi `
  --cpu 1

# Then set environment variables
.\setup-environment.ps1 -ProjectId YOUR-PROJECT-ID
```

## Test Deployment

```powershell
# Get service URL
$url = gcloud run services describe orchestratex --region=us-central1 --format="value(status.url)"

# Test health endpoint
curl "$url/health"

# Test chat endpoint (POST)
curl -X POST "$url/chat" -H "Content-Type: application/json" -d '{"prompt":"Hello"}'
```

## Troubleshooting

### Permission Denied Errors
- Go to https://console.cloud.google.com/iam-admin/iam
- Add Cloud Run Admin role to your account

### Billing Issues
- Go to https://console.cloud.google.com/billing
- Link a billing account to your project

### Project Not Found
- Use `gcloud projects list` to see available projects
- Use the PROJECT ID (not name) in commands

### Domain Issues
- Verify domain at https://console.cloud.google.com/apis/credentials/domainverification
- Add DNS TXT record as instructed