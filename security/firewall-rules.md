# OrchestrateX Firewall Rules and Network Security

## 📋 Overview
This document outlines the network security configuration for OrchestrateX MongoDB deployment.

## 🔥 Firewall Rules

### Development Environment
```bash
# Allow MongoDB access only from localhost
sudo ufw allow from 127.0.0.1 to any port 27018
sudo ufw allow from ::1 to any port 27018

# Block all other access to MongoDB
sudo ufw deny 27018
```

### Production Environment
```bash
# Allow MongoDB access only from application servers
sudo ufw allow from 10.0.1.0/24 to any port 27017  # App server subnet
sudo ufw allow from 10.0.2.0/24 to any port 27017  # Backup server subnet

# Allow monitoring from specific IP
sudo ufw allow from 10.0.3.100 to any port 27017   # Monitoring server

# Block all other access
sudo ufw deny 27017

# Allow only HTTPS traffic for web application
sudo ufw allow 443/tcp
sudo ufw allow 80/tcp   # Redirect to HTTPS

# SSH access (change default port for security)
sudo ufw allow 2222/tcp  # Custom SSH port
sudo ufw deny 22/tcp     # Block default SSH port
```

## 🐳 Docker Network Security

### Docker Compose Network Configuration
```yaml
# Secure internal network for OrchestrateX
networks:
  orchestratex_network:
    driver: bridge
    internal: true  # No external access
    ipam:
      driver: default
      config:
        - subnet: 172.20.0.0/16
```

### Container Network Rules
```bash
# Block container access to host network
docker network create --internal orchestratex_internal

# Use custom bridge with restricted access
docker network create --driver bridge --subnet=172.20.0.0/16 orchestratex_secure
```

## 🛡️ MongoDB Network Security

### Bind IP Configuration
```yaml
# mongod.conf - Production settings
net:
  port: 27017
  bindIp: 127.0.0.1,10.0.1.100  # Only specific IPs
  # bindIp: 0.0.0.0  # NEVER use in production!
```

### IP Whitelist Examples
```javascript
// MongoDB IP whitelist (if using Atlas or cloud)
const allowedIPs = [
  "10.0.1.0/24",      // Application servers
  "10.0.2.100/32",    // Backup server
  "10.0.3.100/32",    // Monitoring server
  "203.0.113.0/24"    // Office network
];
```

## 🌐 Cloud Provider Security Groups

### AWS Security Groups
```bash
# Create security group for MongoDB
aws ec2 create-security-group \
  --group-name orchestratex-mongodb \
  --description "OrchestrateX MongoDB Security Group"

# Allow MongoDB access only from app servers
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 27017 \
  --source-group sg-yyyyy  # App server security group

# Allow SSH from bastion host only
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxxxx \
  --protocol tcp \
  --port 22 \
  --source-group sg-zzzzz  # Bastion security group
```

### Azure Network Security Groups
```bash
# Create NSG rule for MongoDB
az network nsg rule create \
  --resource-group orchestratex-rg \
  --nsg-name orchestratex-nsg \
  --name AllowMongoDBFromAppServers \
  --protocol Tcp \
  --priority 100 \
  --source-address-prefixes 10.0.1.0/24 \
  --destination-port-ranges 27017 \
  --access Allow
```

### Google Cloud Firewall Rules
```bash
# Allow MongoDB access from specific subnet
gcloud compute firewall-rules create allow-mongodb-from-apps \
  --allow tcp:27017 \
  --source-ranges 10.0.1.0/24 \
  --target-tags mongodb-server
```

## 🔐 VPN and Private Network Access

### VPN Configuration
```bash
# Allow VPN users to access MongoDB
sudo ufw allow from 10.8.0.0/24 to any port 27017  # VPN subnet

# Require VPN for all database access
# Block direct internet access to MongoDB ports
sudo ufw deny from any to any port 27017
```

### Private Subnet Configuration
```bash
# Ensure MongoDB is in private subnet
# No public IP assignment
# Access only through VPN or bastion host
```

## 🚨 Security Monitoring

### Log Monitoring Rules
```bash
# Monitor failed connection attempts
tail -f /var/log/mongodb/mongod.log | grep "Authentication failed"

# Alert on unusual connection patterns
grep "connection accepted" /var/log/mongodb/mongod.log | \
  awk '{print $NF}' | sort | uniq -c | sort -nr
```

### Automated Security Checks
```bash
#!/bin/bash
# security-check.sh - Daily security audit

# Check for open MongoDB ports
netstat -tuln | grep :27017

# Verify firewall rules
sudo ufw status numbered

# Check for unauthorized users
mongosh --eval "db.getUsers()" admin

# Monitor connection attempts
tail -100 /var/log/mongodb/mongod.log | grep -E "(auth|connection)"
```

## 📊 Network Topology

```
Internet
    ↓ (HTTPS only)
Load Balancer (443/80)
    ↓ (Internal network)
Application Servers (10.0.1.0/24)
    ↓ (MongoDB protocol, port 27017)
MongoDB Cluster (10.0.2.0/24)
    ↓ (Backup network)
Backup Servers (10.0.3.0/24)
```

## ✅ Security Checklist

### Pre-Production
- [ ] MongoDB not accessible from internet
- [ ] Firewall rules configured and tested
- [ ] VPN access configured
- [ ] Security groups properly configured
- [ ] Monitoring and alerting enabled
- [ ] Backup network isolated

### Production Deployment
- [ ] Change default MongoDB port
- [ ] Implement IP whitelisting
- [ ] Enable SSL/TLS encryption
- [ ] Configure audit logging
- [ ] Set up intrusion detection
- [ ] Regular security assessments

## 🚨 Emergency Procedures

### Security Breach Response
1. Immediately block all external access
2. Review audit logs for unauthorized access
3. Change all passwords and regenerate keys
4. Rebuild compromised systems
5. Conduct security assessment

### Emergency Access
```bash
# Emergency firewall shutdown
sudo ufw --force reset

# Block all MongoDB access
sudo ufw deny 27017

# Allow only emergency access
sudo ufw allow from YOUR_IP to any port 27017
```

---

**⚠️ Security Note**: Always test firewall rules in a staging environment before applying to production. Ensure you have alternative access methods configured before implementing restrictive rules.
