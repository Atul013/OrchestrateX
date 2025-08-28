# OrchestrateX MongoDB Persistence & Performance Optimization Guide

## 📋 Overview

This guide covers data persistence, performance optimization, and maintenance procedures for the OrchestrateX MongoDB database running in Docker containers.

## 💾 Data Persistence

### Volume Configuration

OrchestrateX uses named Docker volumes to ensure data persistence across container restarts:

```yaml
volumes:
  orchestratex_data:       # Main database data
    driver: local
  orchestratex_config:     # Configuration database data  
    driver: local
```

### Volume Mappings

| Container Path | Volume/Mount | Purpose |
|----------------|--------------|---------|
| `/data/db` | `orchestratex_data` | **Primary database storage** |
| `/data/configdb` | `orchestratex_config` | **Config database storage** |
| `/var/log/mongodb` | `./logs` | **Log files** |
| `/data/backup` | `./backups` | **Backup storage** |

### Persistence Verification

To verify data persists across container lifecycle:

```bash
# 1. Create test data
docker exec orchestratex_mongodb mongosh --eval "
  use orchestratex;
  db.test_persistence.insertOne({
    message: 'Data persistence test',
    timestamp: new Date()
  });
"

# 2. Stop and remove container
docker compose down

# 3. Start container again
docker compose up -d

# 4. Verify data still exists
docker exec orchestratex_mongodb mongosh --eval "
  use orchestratex;
  db.test_persistence.find().pretty();
"
```

## ⚡ Performance Optimization

### Current Configuration

Our MongoDB configuration is optimized for OrchestrateX workloads:

#### **Memory Management**
```yaml
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 1.5              # Increased cache for better performance
      maxCacheOverflowFileSizeGB: 0.5  # Overflow cache management
```

#### **Connection Management**
```yaml
net:
  maxIncomingConnections: 1000      # Support high concurrency
  compression:
    compressors: "snappy,zstd"      # Data compression
```

#### **Journal & Sync**
```yaml
storage:
  journal:
    commitIntervalMs: 100           # Optimized journal commits
  syncPeriodSecs: 60               # Sync every 60 seconds
```

### Performance Monitoring

#### **Slow Query Profiling**
```yaml
operationProfiling:
  mode: slowOp
  slowOpThresholdMs: 100           # Log operations slower than 100ms
```

#### **View Slow Queries**
```bash
# Connect to MongoDB
docker exec -it orchestratex_mongodb mongosh

# View profiling data
use orchestratex
db.system.profile.find().limit(5).sort({ts: -1}).pretty()

# Find slowest operations
db.system.profile.find({millis: {$gt: 100}}).sort({millis: -1}).limit(10)
```

### Performance Tuning Parameters

#### **Memory Settings**
- **Cache Size**: Set to 1.5GB (adjust based on available RAM)
- **Journal**: Optimized commit interval for balance of safety and performance
- **Compression**: Snappy compression for good performance with space savings

#### **Connection Settings**
- **Max Connections**: 1000 concurrent connections
- **Connection Pooling**: Optimized pool sizes for application connections

#### **Query Optimization**
- **Index Usage**: Comprehensive indexes defined in `database/indexes.js`
- **Memory Limits**: Set limits for sorting and aggregation operations

## 🔧 Configuration Tuning

### Adjusting Cache Size

Based on your system resources:

```bash
# For systems with 4GB+ RAM
# Edit config/mongod.conf:
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 2.0    # Use ~50% of available RAM

# For systems with 8GB+ RAM  
storage:
  wiredTiger:
    engineConfig:
      cacheSizeGB: 3.0    # Use ~40% of available RAM
```

### Docker Resource Limits

Current container limits:

```yaml
deploy:
  resources:
    limits:
      memory: 2G          # Maximum memory usage
      cpus: '1.0'         # Maximum CPU usage
```

**To adjust for your system:**

```yaml
# For high-performance systems
deploy:
  resources:
    limits:
      memory: 4G          # Increase memory limit
      cpus: '2.0'         # Increase CPU limit
```

## 💽 Backup & Restore Procedures

### Automated Backup Scripts

Two backup scripts are provided:

- **Linux/Mac**: `backup-script.sh`
- **Windows**: `backup-script.ps1`

### Backup Types

#### **Full Database Backup**
```bash
# Linux/Mac
./backup-script.sh full

# Windows PowerShell
.\backup-script.ps1 full
```

#### **Single Database Backup**
```bash
# Linux/Mac
./backup-script.sh database orchestratex

# Windows PowerShell  
.\backup-script.ps1 database orchestratex
```

#### **Collection Backup**
```bash
# Linux/Mac
./backup-script.sh collection orchestratex user_sessions

# Windows PowerShell
.\backup-script.ps1 collection orchestratex user_sessions
```

### Restore Procedures

#### **Full Restore**
```bash
# Linux/Mac
./backup-script.sh restore ./backups/20240828_143022

# Windows PowerShell
.\backup-script.ps1 restore .\backups\20240828_143022
```

### Backup Schedule Recommendations

#### **Development Environment**
- **Daily**: Full database backup
- **Weekly**: Backup cleanup (keep last 7 backups)

#### **Production Environment**
- **Every 6 hours**: Full database backup
- **Daily**: Incremental backup (if supported)
- **Weekly**: Backup verification and cleanup
- **Monthly**: Archive important backups offsite

### Backup Storage

#### **Local Storage Structure**
```
backups/
├── 20240828_143022/    # Timestamped backup folders
│   └── orchestratex/   # Database-specific backups
├── 20240828_153045/
│   └── orchestratex/
└── ...
```

#### **Production Recommendations**
- **Offsite Storage**: AWS S3, Google Cloud Storage, or Azure Blob
- **Encryption**: Encrypt backups before storing
- **Retention**: Keep daily backups for 30 days, weekly for 3 months
- **Testing**: Regularly test restore procedures

## 📊 Performance Monitoring

### Key Metrics to Monitor

#### **MongoDB Metrics**
```bash
# Database stats
docker exec orchestratex_mongodb mongosh --eval "
  db.runCommand({dbStats: 1, scale: 1024*1024})
"

# Server status
docker exec orchestratex_mongodb mongosh --eval "
  db.runCommand({serverStatus: 1})
"

# Connection stats
docker exec orchestratex_mongodb mongosh --eval "
  db.runCommand({connPoolStats: 1})
"
```

#### **System Metrics**
```bash
# Container resource usage
docker stats orchestratex_mongodb

# Volume usage
docker system df -v

# Network stats
docker exec orchestratex_mongodb netstat -tuln
```

### Performance Alerts

Set up monitoring for:
- **Memory Usage**: Alert if cache hit ratio < 95%
- **Slow Queries**: Alert if queries > 1 second
- **Connections**: Alert if connections > 80% of max
- **Disk Space**: Alert if disk usage > 85%
- **Replication Lag**: Alert if lag > 5 seconds (in replica sets)

## 🔍 Troubleshooting

### Common Performance Issues

#### **High Memory Usage**
```bash
# Check current cache usage
docker exec orchestratex_mongodb mongosh --eval "
  db.runCommand({serverStatus: 1}).wiredTiger.cache
"

# Solution: Adjust cacheSizeGB in mongod.conf
```

#### **Slow Queries**
```bash
# Identify slow queries
docker exec orchestratex_mongodb mongosh --eval "
  db.system.profile.find({millis: {\$gt: 100}}).sort({millis: -1})
"

# Solution: Add indexes, optimize queries
```

#### **Connection Limits**
```bash
# Check current connections
docker exec orchestratex_mongodb mongosh --eval "
  db.runCommand({serverStatus: 1}).connections
"

# Solution: Adjust maxIncomingConnections or implement connection pooling
```

### Log Analysis

#### **View MongoDB Logs**
```bash
# Recent logs
docker logs orchestratex_mongodb --tail 100

# Follow logs in real-time
docker logs orchestratex_mongodb -f

# Search for errors
docker logs orchestratex_mongodb 2>&1 | grep -i error
```

#### **Log File Locations**
- **Container Logs**: Available via `docker logs`
- **MongoDB Logs**: Mounted at `./logs/mongod.log`
- **Audit Logs**: `./logs/audit.log` (if enabled)

## ✅ Maintenance Checklist

### Daily Tasks
- [ ] Check container health status
- [ ] Monitor log files for errors
- [ ] Verify backup completion
- [ ] Check disk space usage

### Weekly Tasks
- [ ] Review slow query log
- [ ] Analyze performance metrics
- [ ] Cleanup old backups
- [ ] Update performance baselines

### Monthly Tasks
- [ ] Review and adjust cache settings
- [ ] Perform backup restore test
- [ ] Security audit and updates
- [ ] Capacity planning review

### Quarterly Tasks
- [ ] MongoDB version update evaluation
- [ ] Performance optimization review
- [ ] Disaster recovery testing
- [ ] Archive historical data

## 🚀 Scaling Considerations

### Vertical Scaling (Single Node)
- Increase container memory limits
- Add more CPU cores
- Use faster storage (SSD)
- Optimize indexes and queries

### Horizontal Scaling (Future)
- Implement replica sets for read scaling
- Consider sharding for write scaling
- Use MongoDB Atlas for managed scaling
- Implement application-level caching

## 📈 Performance Benchmarking

### Baseline Measurements
Record initial performance metrics:
- Average query response time
- Peak concurrent connections
- Memory usage patterns
- Disk I/O patterns

### Regular Testing
- Monthly performance tests
- Load testing for peak scenarios
- Backup/restore time measurements
- Index effectiveness analysis

---

**Note**: This configuration is optimized for the OrchestrateX multi-AI orchestration system. Adjust settings based on your specific workload patterns and system resources.
