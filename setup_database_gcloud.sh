#!/bin/bash
# MongoDB Atlas Setup Script for OrchestrateX on Google Cloud
# This script guides you through setting up MongoDB Atlas

echo "🚀 Setting up MongoDB Atlas for OrchestrateX"
echo "=============================================="

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q "@"; then
    echo "❌ Please authenticate with gcloud first: gcloud auth login"
    exit 1
fi

echo "✅ Google Cloud CLI is ready"

# Get current project
PROJECT_ID=$(gcloud config get-value project)
echo "📋 Current project: $PROJECT_ID"

echo ""
echo "OPTION 1: MongoDB Atlas (Recommended)"
echo "====================================="
echo "1. MongoDB Atlas provides the best MongoDB hosting experience"
echo "2. It runs on Google Cloud Platform infrastructure"
echo "3. Offers free tier (M0) and paid tiers"
echo "4. Full MongoDB compatibility with OrchestrateX"
echo ""
echo "To set up MongoDB Atlas:"
echo "1. Go to: https://www.mongodb.com/cloud/atlas"
echo "2. Create account and new project 'OrchestrateX'"
echo "3. Create M0 cluster on Google Cloud (us-central1)"
echo "4. Username: orchestratex_user"
echo "5. Add IP whitelist: 0.0.0.0/0"
echo "6. Get connection string"

echo ""
echo "OPTION 2: Google Cloud Firestore (Alternative)"
echo "=============================================="
echo "1. Native Google Cloud NoSQL database"
echo "2. Requires code modifications"
echo "3. Different from MongoDB syntax"

echo ""
read -p "Choose option (1 for Atlas, 2 for Firestore, 3 for Cloud SQL): " choice

case $choice in
    1)
        echo "📋 Setting up for MongoDB Atlas..."
        
        # Enable required APIs
        echo "🔧 Enabling required Google Cloud APIs..."
        gcloud services enable secretmanager.googleapis.com
        
        # Create secret for database connection
        echo "🔐 Creating secret manager entries..."
        
        echo "Please complete MongoDB Atlas setup manually:"
        echo "1. Visit: https://cloud.mongodb.com/"
        echo "2. Create cluster on Google Cloud Platform"
        echo "3. Choose region: us-central1 (same as Cloud Run)"
        echo "4. Create database user: orchestratex_user"
        echo "5. Whitelist IP: 0.0.0.0/0"
        echo ""
        
        read -p "Enter your MongoDB Atlas connection string: " MONGO_CONNECTION
        
        # Store in Secret Manager
        echo "$MONGO_CONNECTION" | gcloud secrets create mongodb-connection-string --data-file=-
        
        # Update Cloud Run service with new environment variable
        echo "🚀 Updating Cloud Run service..."
        gcloud run services update orchestratex \
            --region=us-central1 \
            --set-env-vars="MONGODB_CONNECTION_STRING=$MONGO_CONNECTION" \
            --set-env-vars="DATABASE_NAME=orchestratex"
            
        echo "✅ MongoDB Atlas configured successfully!"
        ;;
        
    2)
        echo "📋 Setting up Google Cloud Firestore..."
        
        # Enable Firestore API
        gcloud services enable firestore.googleapis.com
        
        # Create Firestore database
        gcloud firestore databases create --region=us-central
        
        echo "⚠️  Note: This requires code modifications to use Firestore instead of MongoDB"
        echo "✅ Firestore database created"
        ;;
        
    3)
        echo "📋 Setting up Cloud SQL for PostgreSQL..."
        
        # Enable Cloud SQL API
        gcloud services enable sqladmin.googleapis.com
        
        # Create Cloud SQL instance
        echo "🔧 Creating Cloud SQL instance..."
        gcloud sql instances create orchestratex-postgres \
            --database-version=POSTGRES_13 \
            --tier=db-f1-micro \
            --region=us-central1
            
        # Create database
        gcloud sql databases create orchestratex --instance=orchestratex-postgres
        
        # Create user
        gcloud sql users create orchestratex_user \
            --instance=orchestratex-postgres \
            --password=orchestratex_password
            
        echo "⚠️  Note: This requires significant code modifications"
        echo "✅ Cloud SQL instance created"
        ;;
        
    *)
        echo "❌ Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🎉 Database setup complete!"
echo "Next steps:"
echo "1. Update your environment variables in Cloud Run"
echo "2. Redeploy your application"
echo "3. Test the database connection"

# Create deployment script
cat > deploy_with_database.sh << EOF
#!/bin/bash
# Deploy OrchestrateX with database configuration

echo "🚀 Deploying OrchestrateX with database..."

# Build and deploy with updated configuration
gcloud builds submit --config cloudbuild-simple.yaml . --async

echo "✅ Deployment started. Check Cloud Build console for progress."
EOF

chmod +x deploy_with_database.sh

echo ""
echo "📜 Created deploy_with_database.sh script for easy redeployment"