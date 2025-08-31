# 🚀 OrchestrateX Quick Start Guide

## Easy Startup for Tomorrow

### Option 1: One-Click Startup (Recommended)
```
Double-click: start_full_system.bat
```
This will automatically start:
1. MongoDB Docker (Port 27019)
2. Backend API (Port 8002) 
3. Frontend UI (Port 5176+)
4. Open MongoDB Express (Port 8081)

### Option 2: Manual Startup
If you prefer to start components individually:

1. **Start MongoDB:**
   ```
   start_mongodb.bat
   ```

2. **Start Backend API:**
   ```
   venv\Scripts\python.exe working_api.py
   ```

3. **Start Frontend:**
   ```
   cd "FRONTEND\CHAT BOT UI\ORCHACHATBOT\project"
   npm run dev
   ```

## 🌐 System URLs

- **Frontend Chat Interface:** http://localhost:5176 (or next available port)
- **Backend API:** http://localhost:8002  
- **MongoDB Express:** http://localhost:8081 (admin/admin)

## 📊 MongoDB Collections

Your data is stored in database `orchestratex`:
- **prompts** - User messages from the UI
- **model_responses** - AI model responses (GLM-4.5, GPT-OSS, Llama-4-Maverick, Kimi-K2, TNG-DeepSeek-R1T2)

## 🔧 Key Configuration

- **MongoDB Port:** 27019 (updated for your network)
- **API Port:** 8002
- **Frontend Port:** Auto-assigned starting from 5176
- **MongoDB Express:** 8081

## ✅ Verification Checklist

After startup, verify:
1. ✅ MongoDB Express opens automatically
2. ✅ API terminal shows "MongoDB Docker connected successfully!"
3. ✅ Frontend terminal shows the port number
4. ✅ Send a test message in UI
5. ✅ Check MongoDB Express for stored data

## 🛠️ Troubleshooting

- **If MongoDB fails:** Check if Docker Desktop is running
- **If API fails:** Check if port 8002 is available
- **If Frontend fails:** Check if Node.js/npm is installed
- **If storage fails:** Check MongoDB Express for connection

---
**Note:** All ports have been configured for your network setup. The system should start smoothly tomorrow! 🎯
