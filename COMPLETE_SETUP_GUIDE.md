# Complete OrchestrateX Google Cloud Setup Guide
# Domain Verification, Permissions, and Landing Page Integration

## 🎯 Step 1: Google Cloud Project Setup

### 1.1 Create or Select Project
```powershell
# Create a new project (recommended)
gcloud projects create orchestratex-prod-2025 --name="OrchestrateX Production"

# Or list existing projects
gcloud projects list

# Set the project
gcloud config set project orchestratex-prod-2025
```

### 1.2 Enable Billing
1. Go to: https://console.cloud.google.com/billing
2. Link a billing account to your project
3. **This is REQUIRED for Cloud Run**

## 🔐 Step 2: Set Up Permissions

### 2.1 Add Required Roles to Your Account
```powershell
# Get your current account
$ACCOUNT = gcloud config get-value account

# Set your project ID
$PROJECT_ID = "orchestratex-prod-2025"

# Add required roles
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$ACCOUNT" --role="roles/owner"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$ACCOUNT" --role="roles/cloudbuild.builds.editor"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$ACCOUNT" --role="roles/run.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="user:$ACCOUNT" --role="roles/storage.admin"
```

### 2.2 Enable Required Services
```powershell
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable domains.googleapis.com
gcloud services enable dns.googleapis.com
gcloud services enable certificatemanager.googleapis.com
```

## 🌐 Step 3: Domain Verification (orchestratex.me)

### 3.1 Add Domain to Google Cloud
1. **Go to Domain Verification Console:**
   https://console.cloud.google.com/apis/credentials/domainverification

2. **Click "Add Domain"**
3. **Enter:** `orchestratex.me`
4. **Select verification method:** DNS TXT record (recommended)

### 3.2 Add DNS TXT Record
You'll get a TXT record like this:
```
Type: TXT
Name: @ (or orchestratex.me)
Value: google-site-verification=ABC123XYZ...
```

**Add this to your domain registrar:**
- If using Cloudflare: DNS → Records → Add Record
- If using GoDaddy: DNS Management → Add TXT Record
- If using Namecheap: Advanced DNS → Add TXT Record

### 3.3 Verify Domain
```powershell
# Check verification status
gcloud domains list-user-verified-domains

# Or check in console: https://console.cloud.google.com/apis/credentials/domainverification
```

**⏰ Wait time:** 5 minutes to 24 hours for verification

## 🚀 Step 4: Deploy OrchestrateX API

### 4.1 Run Deployment Script
```powershell
# Use your verified project ID
.\deploy-orchestratex.ps1
# Enter: orchestratex-prod-2025
```

### 4.2 Set Environment Variables
```powershell
.\setup-environment.ps1 -ProjectId orchestratex-prod-2025
```

### 4.3 Test API Deployment
```powershell
.\test-deployment.ps1 -ProjectId orchestratex-prod-2025
```

## 🌐 Step 5: Domain Mapping Setup

### 5.1 Create Domain Mapping (After Domain is Verified)
```powershell
# Create the mapping
gcloud run domain-mappings create --domain orchestratex.me --service orchestratex --region us-central1

# Get DNS records
gcloud run domain-mappings describe orchestratex.me --region us-central1 --format="table(status.resourceRecords[].name,status.resourceRecords[].type,status.resourceRecords[].rrdata)"
```

### 5.2 Configure DNS Records at Your Registrar
You'll get records like:
```
Type: A
Name: @ (or orchestratex.me)
Value: 216.239.32.21

Type: A  
Name: @ (or orchestratex.me)
Value: 216.239.34.21

Type: A
Name: @ (or orchestratex.me) 
Value: 216.239.36.21

Type: A
Name: @ (or orchestratex.me)
Value: 216.239.38.21

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:32::15

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:34::15

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:36::15

Type: AAAA
Name: @ (or orchestratex.me)
Value: 2001:4860:4802:38::15
```

**Add ALL these records to your domain registrar**

## 🏠 Step 6: Landing Page Setup

### 6.1 Deploy Landing Page to Firebase Hosting

First, let's check your landing page structure:
```powershell
# Check if you have a landing page
Get-ChildItem landingapge/
Get-ChildItem FRONTEND/
```

### 6.2 Set up Firebase Hosting
```powershell
# Install Firebase CLI (if not installed)
npm install -g firebase-tools

# Login to Firebase
firebase login

# Initialize Firebase in your project
firebase init hosting
```

**Firebase Setup Prompts:**
- Select existing project: `orchestratex-prod-2025`
- Public directory: `landingapge` (or wherever your landing page is)
- Single-page app: `No`
- Overwrite index.html: `No`

### 6.3 Configure firebase.json for Multiple Sites
```json
{
  "hosting": [
    {
      "target": "main",
      "public": "landingapge",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
      "rewrites": [
        {
          "source": "/api/**",
          "destination": "https://orchestratex.me/api/**"
        }
      ]
    },
    {
      "target": "chat",
      "public": "chatbot-frontend/dist",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
      "rewrites": [
        {
          "source": "/**",
          "destination": "/index.html"
        }
      ]
    }
  ]
}
```

### 6.4 Deploy Landing Page
```powershell
# Deploy to Firebase
firebase deploy --only hosting:main

# This gives you: https://orchestratex-prod-2025.web.app
```

## 🔗 Step 7: Complete Domain Setup

### 7.1 Configure Subdomains
Add these DNS records to your registrar:

```
# Main landing page
Type: CNAME
Name: www
Value: orchestratex-prod-2025.web.app

# API (already configured above)
Type: A 
Name: api
Value: [Cloud Run IPs from step 5.2]

# Chat application
Type: CNAME
Name: chat
Value: orchestratex-prod-2025.web.app
```

### 7.2 Update Firebase Hosting for Custom Domain
```powershell
# Add custom domain to Firebase
firebase hosting:sites:create orchestratex-main
firebase target:apply hosting main orchestratex-main

# Connect custom domain
firebase hosting:channel:deploy live --only hosting:main
```

Then in Firebase Console:
1. Go to: https://console.firebase.google.com/project/orchestratex-prod-2025/hosting
2. Click "Add custom domain"
3. Enter: `www.orchestratex.me`
4. Follow the verification steps

## 🔧 Step 8: Update Application URLs

### 8.1 Update CORS in working_api.py
```python
CORS(app, origins=[
    'https://orchestratex.me',
    'https://www.orchestratex.me', 
    'https://chat.orchestratex.me',
    'https://api.orchestratex.me',
    'http://localhost:3000',
    'http://localhost:5173'
], methods=['GET', 'POST', 'OPTIONS'], allow_headers=['Content-Type', 'Authorization'])
```

### 8.2 Update Frontend Configuration
In your chatbot frontend, update API endpoints:
```javascript
const API_BASE_URL = 'https://orchestratex.me';
// or 'https://api.orchestratex.me' if using subdomain
```

### 8.3 Redeploy with Updates
```powershell
# Redeploy API with updated CORS
gcloud run deploy orchestratex --source . --dockerfile Dockerfile.production --region us-central1

# Redeploy frontend
firebase deploy --only hosting
```

## 🧪 Step 9: Testing Everything

### 9.1 Test API Endpoints
```powershell
# Test health endpoint
curl https://orchestratex.me/health

# Test chat endpoint  
curl -X POST https://orchestratex.me/chat -H "Content-Type: application/json" -d '{"message":"Hello"}'
```

### 9.2 Test Landing Page
- Visit: https://orchestratex.me
- Visit: https://www.orchestratex.me  
- Check: All links work
- Check: API calls from frontend work

### 9.3 Test Chat Application
- Visit: https://chat.orchestratex.me
- Test: Send a message
- Check: API responses work

## 📊 Step 10: Final Configuration

### 10.1 SSL Certificate (Automatic)
- Cloud Run: Automatic HTTPS
- Firebase Hosting: Automatic HTTPS
- Domain mapping: Automatic certificate provisioning

### 10.2 DNS Propagation Check
```powershell
# Check DNS propagation
nslookup orchestratex.me
nslookup www.orchestratex.me
nslookup chat.orchestratex.me
```

**Use online tools:**
- https://whatsmydns.net
- https://dnschecker.org

## 🎉 Final URL Structure

After complete setup:

```
https://orchestratex.me          → Landing page (Firebase)
https://www.orchestratex.me      → Landing page (Firebase)  
https://chat.orchestratex.me     → Chat application (Firebase)
https://api.orchestratex.me      → API endpoints (Cloud Run)
```

**Or simplified version:**
```
https://orchestratex.me          → Landing page (Firebase)
https://orchestratex.me/api      → API endpoints (proxied to Cloud Run)
https://orchestratex.me/chat     → Chat application (Firebase)
```

## 🛠️ Troubleshooting Commands

```powershell
# Check domain verification
gcloud domains list-user-verified-domains

# Check Cloud Run service
gcloud run services describe orchestratex --region us-central1

# Check domain mapping
gcloud run domain-mappings describe orchestratex.me --region us-central1

# View logs
gcloud run services logs read orchestratex --region us-central1

# Check Firebase hosting
firebase hosting:sites:list

# Test DNS
nslookup orchestratex.me 8.8.8.8
```

## ⏱️ Timeline Expectations

- **Project setup:** 5 minutes
- **Domain verification:** 5 minutes - 24 hours  
- **API deployment:** 10-15 minutes
- **Domain mapping:** 5 minutes
- **DNS propagation:** 5 minutes - 4 hours
- **SSL certificate:** 5-15 minutes

**Total time:** 30 minutes - 24 hours (depending on domain verification)

Ready to start? Begin with Step 1! 🚀