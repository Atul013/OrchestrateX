# 🌐 FRONTEND TO FIRESTORE INTEGRATION GUIDE

## 🎯 Current Setup

### **Frontend Configuration**
- **Landing Page**: https://orchestratex.me (points to chat.orchestratex.me)
- **Chat Interface**: https://chat.orchestratex.me 
- **API Endpoint**: https://api.orchestratex.me

### **Backend Configuration**  
- **Local Firestore**: http://localhost:8002 ✅ WORKING
- **Cloud Deployment**: Needs to be deployed to https://api.orchestratex.me

---

## 🔧 INTEGRATION STEPS

### 1. **Update Cloud Deployment**
Replace the old backend with our new Firestore version:

```bash
# Deploy Firestore backend to Cloud Run
gcloud run deploy orchestratex-api \
  --image gcr.io/orchestratex-app/orchestratex:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8002
```

### 2. **Frontend API Flow** 
```
User enters prompt on chat.orchestratex.me
          ↓
Sends POST to https://api.orchestratex.me/chat  
          ↓
Our Firestore backend processes request
          ↓
Stores prompt in Google Cloud Firestore
          ↓
Returns AI response to frontend
```

### 3. **API Endpoints**
- `POST /chat` - Store user prompts & get AI responses
- `GET /health` - Health check
- `GET /models` - Available AI models

---

## 🚀 DEPLOYMENT COMMANDS

### **Option A: Manual Deployment**
```bash
# 1. Install Google Cloud CLI
# 2. Authenticate
gcloud auth login

# 3. Build and deploy
docker build -f Dockerfile.firestore -t gcr.io/orchestratex-app/orchestratex:latest .
docker push gcr.io/orchestratex-app/orchestratex:latest
gcloud run deploy orchestratex-api --image gcr.io/orchestratex-app/orchestratex:latest --region us-central1
```

### **Option B: Using Deployment Script**
```bash
# Run the deployment script
./deploy-to-cloud.bat
```

---

## ✅ VERIFICATION

After deployment, test:
1. **Health Check**: https://api.orchestratex.me/health
2. **Chat Endpoint**: POST to https://api.orchestratex.me/chat
3. **Frontend Integration**: Enter prompt on chat.orchestratex.me

---

## 📊 EXPECTED DATA FLOW

```
User Input: "Create a landing page"
         ↓
Frontend: chat.orchestratex.me
         ↓  
API: https://api.orchestratex.me/chat
         ↓
Backend: Express.js + Firestore
         ↓
Database: Google Cloud Firestore
         ↓
Response: AI-generated content
         ↓
Frontend: Display to user
```

**Result**: Every prompt from orchestratex.me gets stored in Firestore! 🎉