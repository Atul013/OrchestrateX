#!/bin/bash

# OrchestrateX Infinity Castle - Deployment Validation Script
echo "🎌 Validating Infinity Castle Deployment..."
echo "════════════════════════════════════════════"

PROJECT_ID="orchestratex-441819"
SERVICE_NAME="orchestratex-infinity-castle"
REGION="us-central1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Checking Google Cloud authentication...${NC}"
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "."; then
    echo -e "${RED}❌ Not authenticated with Google Cloud${NC}"
    echo "Please run: gcloud auth login"
    exit 1
fi
echo -e "${GREEN}✅ Authenticated${NC}"

echo -e "${BLUE}🔍 Checking project configuration...${NC}"
CURRENT_PROJECT=$(gcloud config get-value project 2>/dev/null)
if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo -e "${YELLOW}⚠️  Setting project to $PROJECT_ID${NC}"
    gcloud config set project $PROJECT_ID
fi
echo -e "${GREEN}✅ Project: $PROJECT_ID${NC}"

echo -e "${BLUE}🔍 Checking if service exists...${NC}"
if gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Service $SERVICE_NAME exists${NC}"
    
    # Get service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME \
        --region=$REGION \
        --project=$PROJECT_ID \
        --format="value(status.url)")
    
    echo -e "${BLUE}🌐 Service URL: $SERVICE_URL${NC}"
    
    echo -e "${BLUE}🔍 Testing service health...${NC}"
    if curl -s --max-time 10 "$SERVICE_URL" >/dev/null; then
        echo -e "${GREEN}✅ Service is responding${NC}"
    else
        echo -e "${YELLOW}⚠️  Service may still be starting up${NC}"
    fi
    
else
    echo -e "${RED}❌ Service $SERVICE_NAME not found${NC}"
    echo "Please deploy first using: deploy-infinity-castle.bat"
    exit 1
fi

echo -e "${BLUE}🔍 Checking domain mapping...${NC}"
if gcloud run domain-mappings describe castle.orchestratex.me --region=$REGION --project=$PROJECT_ID >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Domain mapping exists for castle.orchestratex.me${NC}"
    
    echo -e "${BLUE}🔍 Testing custom domain...${NC}"
    if curl -s --max-time 10 "https://castle.orchestratex.me" >/dev/null; then
        echo -e "${GREEN}✅ Custom domain is working${NC}"
    else
        echo -e "${YELLOW}⚠️  Custom domain may still be propagating${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No domain mapping found${NC}"
    echo "Run setup-infinity-castle-domain.ps1 to set up custom domain"
fi

echo -e "${BLUE}🔍 Checking API connectivity...${NC}"
if curl -s --max-time 10 "https://api.orchestratex.me/health" >/dev/null; then
    echo -e "${GREEN}✅ Backend API is accessible${NC}"
else
    echo -e "${YELLOW}⚠️  Backend API may be unavailable${NC}"
fi

echo ""
echo -e "${GREEN}🎭 Infinity Castle Deployment Status:${NC}"
echo "═══════════════════════════════════════════════"
echo -e "📱 Direct URL: ${BLUE}$SERVICE_URL${NC}"
echo -e "🏰 Custom Domain: ${BLUE}https://castle.orchestratex.me${NC}"
echo -e "🎌 Theme: ${YELLOW}Demon Slayer Infinity Castle${NC}"
echo -e "⚡ Status: ${GREEN}Deployed${NC}"
echo ""
echo -e "${YELLOW}🚀 Ready to use your mystical AI chatbot!${NC}"