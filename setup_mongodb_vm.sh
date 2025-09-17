#!/bin/bash
# MongoDB Installation and Setup Script for Google Cloud VM

echo "🚀 Setting up MongoDB on Google Cloud..."

# Update system
sudo apt-get update -y

# Install MongoDB 7.0
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update -y
sudo apt-get install -y mongodb-org

# Start and enable MongoDB
sudo systemctl start mongod
sudo systemctl enable mongod

# Configure MongoDB for external access
sudo cp /etc/mongod.conf /etc/mongod.conf.backup

# Update MongoDB configuration
sudo tee /etc/mongod.conf > /dev/null <<EOF
# MongoDB configuration for OrchestrateX
storage:
  dbPath: /var/lib/mongodb
  journal:
    enabled: true

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 0.0.0.0  # Allow external connections

processManagement:
  timeZoneInfo: /usr/share/zoneinfo

security:
  authorization: enabled

replication:
  replSetName: "orchestratex-replica"
EOF

# Restart MongoDB with new configuration
sudo systemctl restart mongod

# Wait for MongoDB to start
sleep 10

# Initialize MongoDB with admin user
mongosh --eval "
rs.initiate({
  _id: 'orchestratex-replica',
  members: [{ _id: 0, host: 'localhost:27017' }]
});
"

sleep 5

# Create admin user
mongosh --eval "
use admin;
db.createUser({
  user: 'admin',
  pwd: 'OrchestratexAdmin2025!',
  roles: [{ role: 'userAdminAnyDatabase', db: 'admin' }, { role: 'readWriteAnyDatabase', db: 'admin' }]
});
"

# Create OrchestrateX database and user
mongosh --eval "
use orchestratex;
db.createUser({
  user: 'orchestratex_user',
  pwd: 'OrchestrateX2025!',
  roles: [{ role: 'readWrite', db: 'orchestratex' }]
});
"

# Create initial collections and indexes
mongosh "mongodb://orchestratex_user:OrchestrateX2025%21@localhost:27017/orchestratex" --eval "
// Create collections
db.createCollection('user_sessions');
db.createCollection('prompts');
db.createCollection('responses');
db.createCollection('orchestration_workflows');
db.createCollection('ai_model_metrics');
db.createCollection('system_logs');

// Create indexes for better performance
db.user_sessions.createIndex({ 'user_id': 1 });
db.user_sessions.createIndex({ 'session_start': 1 });
db.user_sessions.createIndex({ 'status': 1 });

db.prompts.createIndex({ 'user_id': 1 });
db.prompts.createIndex({ 'timestamp': 1 });
db.prompts.createIndex({ 'session_id': 1 });

db.responses.createIndex({ 'prompt_id': 1 });
db.responses.createIndex({ 'model_name': 1 });
db.responses.createIndex({ 'timestamp': 1 });

db.orchestration_workflows.createIndex({ 'session_id': 1 });
db.orchestration_workflows.createIndex({ 'status': 1 });

db.ai_model_metrics.createIndex({ 'model_name': 1 });
db.ai_model_metrics.createIndex({ 'timestamp': 1 });

db.system_logs.createIndex({ 'timestamp': 1 });
db.system_logs.createIndex({ 'level': 1 });

print('✅ OrchestrateX database initialized successfully!');
"

# Set up automatic backups
sudo mkdir -p /backup/mongodb
sudo chown mongodb:mongodb /backup/mongodb

# Create backup script
sudo tee /usr/local/bin/mongodb-backup.sh > /dev/null <<'EOF'
#!/bin/bash
BACKUP_DIR="/backup/mongodb"
DATE=$(date +%Y%m%d_%H%M%S)
mongodump --uri="mongodb://orchestratex_user:OrchestrateX2025%21@localhost:27017/orchestratex" --out="$BACKUP_DIR/backup_$DATE"
find $BACKUP_DIR -type d -name "backup_*" -mtime +7 -exec rm -rf {} +
EOF

sudo chmod +x /usr/local/bin/mongodb-backup.sh

# Add daily backup cron job
echo "0 2 * * * /usr/local/bin/mongodb-backup.sh" | sudo crontab -

# Display connection information
echo "✅ MongoDB setup complete!"
echo "==============================================="
echo "MongoDB Connection Details:"
echo "Host: $(curl -s http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip -H 'Metadata-Flavor: Google')"
echo "Port: 27017"
echo "Database: orchestratex"
echo "Username: orchestratex_user"
echo "Password: OrchestrateX2025!"
echo "Admin Username: admin"
echo "Admin Password: OrchestratexAdmin2025!"
echo ""
echo "Connection String:"
echo "mongodb://orchestratex_user:OrchestrateX2025%21@$(curl -s http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip -H 'Metadata-Flavor: Google'):27017/orchestratex"
echo "==============================================="