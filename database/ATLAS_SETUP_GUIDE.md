# MongoDB Atlas Configuration Guide for OrchestrateX

## Setup Steps

### 1. Create MongoDB Atlas Account
- Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Sign up or log in with your account
- Create a new project called "OrchestrateX"

### 2. Create Database Cluster
- Click "Build a Database"
- Choose "M0 Sandbox" (Free tier)
- **Select Google Cloud Platform as provider**
- Choose region closest to your users (e.g., us-central1 to match Cloud Run)
- Name your cluster: `orchestratex-cluster`

### 3. Configure Database Access
- Username: `orchestratex_user`
- Password: [Generate strong password]
- Add IP address: `0.0.0.0/0` (Allow access from anywhere for Cloud Run)

### 4. Connection String Format
```
mongodb+srv://orchestratex_user:<password>@orchestratex-cluster.xxxxx.mongodb.net/orchestratex?retryWrites=true&w=majority
```

## Environment Variables to Update

Add these to your Cloud Run environment variables:

```bash
MONGODB_CONNECTION_STRING=mongodb+srv://orchestratex_user:<password>@orchestratex-cluster.xxxxx.mongodb.net/orchestratex?retryWrites=true&w=majority
DATABASE_NAME=orchestratex
```

## Cost Information

- **Free Tier (M0)**: 
  - 512 MB storage
  - Shared CPU
  - No charges
  
- **Paid Tier (M2)**:
  - 2 GB storage
  - ~$9/month
  - Better performance

## Security Features

- Network access control
- Database user authentication
- SSL/TLS encryption
- VPC peering (paid tiers)
- Private endpoints (paid tiers)

## Performance Benefits

- Automatic scaling
- Built-in monitoring
- Automated backups
- Global clusters
- Read replicas