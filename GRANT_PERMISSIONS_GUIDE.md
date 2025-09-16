# How to Grant Firestore Permissions to sahilkhk001@gmail.com

## Method 1: Using Google Cloud Console (Web Interface) - EASIEST

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Select your project**: `orchestratex-app` (or whatever your project is called)
3. **Navigate to IAM & Admin** → **IAM**
4. **Click "GRANT ACCESS"**
5. **Add the user**:
   - **New principals**: `sahilkhk001@gmail.com`
   - **Role**: Select one of these roles:
     - `Cloud Datastore Owner` (full database access)
     - `Firebase Admin` (full Firebase access)
     - `Editor` (project-wide edit access)
6. **Click "SAVE"**

## Method 2: Using Google Cloud CLI (Once installed)

### Install Google Cloud CLI first:
Download from: https://cloud.google.com/sdk/docs/install-windows

### Then run these commands:

```bash
# Authenticate
gcloud auth login

# Set your project
gcloud config set project orchestratex-app

# Grant Datastore Owner permissions
gcloud projects add-iam-policy-binding orchestratex-app \
    --member="user:sahilkhk001@gmail.com" \
    --role="roles/datastore.owner"

# OR grant Firebase Admin permissions (more comprehensive)
gcloud projects add-iam-policy-binding orchestratex-app \
    --member="user:sahilkhk001@gmail.com" \
    --role="roles/firebase.admin"

# Verify the permissions were added
gcloud projects get-iam-policy orchestratex-app \
    --filter="bindings.members:user:sahilkhk001@gmail.com"
```

## Method 3: Enable Firestore if not already enabled

```bash
# Enable Firestore API
gcloud services enable firestore.googleapis.com

# Create Firestore database (if needed)
gcloud firestore databases create --region=us-central1
```

## Recommended Roles for OrchestrateX Development:

1. **For Database Access**: `roles/datastore.owner`
2. **For Full Firebase Access**: `roles/firebase.admin` 
3. **For Project Management**: `roles/editor`

## Quick Test Commands (for sahilkhk001@gmail.com to verify access):

```bash
# Test Firestore access
gcloud firestore collections list

# Test project access
gcloud projects describe orchestratex-app
```

---

**EASIEST OPTION**: Use the Google Cloud Console web interface (Method 1) - it's point and click!