# OrchestrateX Infinity Castle Theme - Deployment Guide

## Overview
The OrchestrateX Infinity Castle Theme is a special Demon Slayer-themed version of the OrchestrateX chatbot, featuring immersive UI designs inspired by the Infinity Castle from the popular anime series.

## 🎌 Features
- **Infinity Castle Theme**: Dark, mystical UI with animated effects
- **AI Model Orchestration**: Full OrchestrateX capabilities with thematic presentation
- **Responsive Design**: Works on desktop and mobile devices
- **Production Ready**: Optimized for Google Cloud Run deployment

## 🚀 Quick Deployment

### Option 1: One-Click Complete Deployment
```bash
# Run the complete deployment script
DEPLOY_INFINITY_CASTLE_COMPLETE.bat
```

This script will:
1. Deploy the application to Google Cloud Run
2. Set up custom domain mapping (optional)
3. Configure all necessary settings

### Option 2: Manual Step-by-Step Deployment

#### Step 1: Deploy to Cloud Run
```bash
deploy-infinity-castle.bat
```

#### Step 2: Set up Custom Domain (Optional)
```powershell
# Run PowerShell as Administrator
./setup-infinity-castle-domain.ps1
```

## 🌐 Access URLs

### Production URLs
- **Direct Cloud Run**: `https://orchestratex-infinity-castle-orchestratex-441819.run.app`
- **Custom Domain**: `https://castle.orchestratex.me` (after DNS setup)

### Local Development
- **Local Dev Server**: `http://localhost:5174`

## 🔧 Configuration

### Environment Variables
The application automatically detects the environment:
- **Local Development**: Uses `http://localhost:8002` for API calls
- **Production**: Uses `https://api.orchestratex.me` for API calls

### API Integration
The Infinity Castle theme connects to the same backend API as the main OrchestrateX application:
- **API Endpoint**: `https://api.orchestratex.me`
- **Chat Endpoint**: `/chat`
- **Models Endpoint**: `/models`
- **Health Check**: `/health`

## 📁 Project Structure
```
ORCHACHATBOT_INFINITY_CASTLE/project/
├── src/
│   ├── components/          # React components with Infinity Castle theme
│   ├── services/           # API integration services
│   ├── constants/          # Configuration constants
│   ├── hooks/              # Custom React hooks
│   └── types/              # TypeScript type definitions
├── public/                 # Static assets
├── Dockerfile              # Container configuration
├── cloudbuild-infinity.yaml # Google Cloud Build configuration
└── package.json           # Dependencies and scripts
```

## 🎨 Theme Customization

### Colors & Styling
The Infinity Castle theme uses:
- **Primary Colors**: Deep purples, cosmic blues, and mystical gradients
- **Typography**: Elegant fonts with subtle glow effects
- **Animations**: Smooth transitions and floating elements
- **Layout**: Immersive full-screen experience

### Custom Components
- **Themed Chat Interface**: Dark mystical chat bubbles
- **Animated Backgrounds**: Floating particles and gradient shifts
- **Model Selection**: Stylized AI model cards
- **Status Indicators**: Themed loading and success states

## 🛠️ Development

### Prerequisites
- Node.js 18+ 
- npm or yarn
- Google Cloud SDK (for deployment)

### Local Development
```bash
cd "E:\Projects\OrchestrateX\FRONTEND\CHAT BOT UI\ORCHACHATBOT_INFINITY_CASTLE\project"
npm install
npm run dev
```

### Building for Production
```bash
npm run build
```

### Testing
```bash
npm run lint
```

## 🚀 Deployment Details

### Google Cloud Run Configuration
- **Service Name**: `orchestratex-infinity-castle`
- **Region**: `us-central1`
- **Port**: `8080`
- **Memory**: `1Gi`
- **CPU**: `1`
- **Max Instances**: `10`
- **Min Instances**: `0`

### Domain Configuration
- **Main Domain**: `orchestratex.me`
- **Subdomain**: `castle.orchestratex.me`
- **SSL**: Automatically managed by Google Cloud

### DNS Setup Required
Add CNAME record to your DNS provider:
```
Type: CNAME
Name: castle
Value: ghs.googlehosted.com
```

## 📊 Monitoring & Logs

### Google Cloud Console
- **Service Logs**: Cloud Run → orchestratex-infinity-castle → Logs
- **Metrics**: Cloud Run → orchestratex-infinity-castle → Metrics
- **Traffic**: Cloud Run → orchestratex-infinity-castle → Details

### Health Checks
- **Endpoint**: `https://castle.orchestratex.me/`
- **Status**: Should return React application
- **API Health**: Backend health checks via main API

## 🔍 Troubleshooting

### Common Issues

#### 1. Deployment Fails
```bash
# Check if you're authenticated
gcloud auth list

# Re-authenticate if needed
gcloud auth login
```

#### 2. Domain Not Working
- Verify DNS records are properly configured
- Allow 5-30 minutes for DNS propagation
- Check domain verification in Google Cloud Console

#### 3. API Connection Issues
- Ensure the main OrchestrateX API is running at `api.orchestratex.me`
- Check network connectivity
- Verify CORS settings on the backend

#### 4. Build Errors
```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Support
For issues or questions:
1. Check the main OrchestrateX documentation
2. Review Google Cloud Run logs
3. Verify API connectivity

## 🎭 Usage Examples

### Basic Chat
```javascript
// Send a message through the themed interface
await apiService.sendMessage("What's the best AI model for creative writing?");
```

### Model Selection
```javascript
// The theme includes enhanced model selection with visual previews
const selectedModel = await modelSelector.selectBestModel(prompt, context);
```

## 📈 Performance

### Optimization Features
- **Code Splitting**: Lazy loading of components
- **Asset Optimization**: Compressed images and fonts
- **Caching**: Efficient browser caching strategies
- **CDN**: Google Cloud CDN integration

### Expected Performance
- **Initial Load**: < 3 seconds
- **Subsequent Navigation**: < 1 second
- **API Response Time**: 2-5 seconds (depends on AI model)

## 🔐 Security

### Security Features
- **HTTPS Only**: All traffic encrypted
- **CORS Protection**: Configured for orchestratex.me domains
- **Input Sanitization**: User inputs are properly sanitized
- **Rate Limiting**: Backend API includes rate limiting

## 🎉 Success Metrics

After successful deployment, you should have:
- ✅ Working Infinity Castle themed chatbot
- ✅ Custom domain (castle.orchestratex.me)
- ✅ Full AI model orchestration capabilities
- ✅ Monitoring and logging in place
- ✅ Secure HTTPS access
- ✅ Mobile-responsive design

---

**Enjoy your mystical AI orchestration experience! 🎌✨**