#!/bin/bash
# OrchestrateX MongoDB Backup Script
# Comprehensive backup solution for Docker-based MongoDB

set -e  # Exit on any error

# Configuration
CONTAINER_NAME="orchestratex_mongodb"
BACKUP_DIR="/data/backup"
LOCAL_BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
DATABASE_NAME="orchestratex"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if container is running
check_container() {
    if ! docker ps --format "table {{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
        error "MongoDB container '${CONTAINER_NAME}' is not running!"
        echo "Start it with: docker compose up -d"
        exit 1
    fi
    success "MongoDB container is running"
}

# Create backup directory if it doesn't exist
prepare_backup_dir() {
    if [ ! -d "$LOCAL_BACKUP_DIR" ]; then
        mkdir -p "$LOCAL_BACKUP_DIR"
        log "Created backup directory: $LOCAL_BACKUP_DIR"
    fi
    
    # Create dated backup subdirectory
    BACKUP_PATH="$LOCAL_BACKUP_DIR/$DATE"
    mkdir -p "$BACKUP_PATH"
    log "Backup will be stored in: $BACKUP_PATH"
}

# Full database backup
backup_full() {
    log "Starting full database backup..."
    
    # Create backup inside container
    docker exec "$CONTAINER_NAME" mongodump \
        --host localhost:27017 \
        --authenticationDatabase admin \
        --username project_admin \
        --password project_password \
        --out "$BACKUP_DIR/$DATE" \
        --gzip || {
        error "Full backup failed!"
        exit 1
    }
    
    # Copy backup to host
    docker cp "$CONTAINER_NAME:$BACKUP_DIR/$DATE" "$LOCAL_BACKUP_DIR/"
    
    success "Full database backup completed: $LOCAL_BACKUP_DIR/$DATE"
}

# Specific database backup
backup_database() {
    local db_name=${1:-$DATABASE_NAME}
    log "Starting backup for database: $db_name"
    
    docker exec "$CONTAINER_NAME" mongodump \
        --host localhost:27017 \
        --authenticationDatabase admin \
        --username project_admin \
        --password project_password \
        --db "$db_name" \
        --out "$BACKUP_DIR/$DATE" \
        --gzip || {
        error "Database backup failed for: $db_name"
        exit 1
    }
    
    # Copy backup to host
    docker cp "$CONTAINER_NAME:$BACKUP_DIR/$DATE" "$LOCAL_BACKUP_DIR/"
    
    success "Database backup completed for $db_name: $LOCAL_BACKUP_DIR/$DATE"
}

# Specific collection backup
backup_collection() {
    local db_name=${1:-$DATABASE_NAME}
    local collection_name=$2
    
    if [ -z "$collection_name" ]; then
        error "Collection name is required for collection backup"
        exit 1
    fi
    
    log "Starting backup for collection: $db_name.$collection_name"
    
    docker exec "$CONTAINER_NAME" mongodump \
        --host localhost:27017 \
        --authenticationDatabase admin \
        --username project_admin \
        --password project_password \
        --db "$db_name" \
        --collection "$collection_name" \
        --out "$BACKUP_DIR/$DATE" \
        --gzip || {
        error "Collection backup failed for: $db_name.$collection_name"
        exit 1
    }
    
    # Copy backup to host
    docker cp "$CONTAINER_NAME:$BACKUP_DIR/$DATE" "$LOCAL_BACKUP_DIR/"
    
    success "Collection backup completed for $db_name.$collection_name: $LOCAL_BACKUP_DIR/$DATE"
}

# Restore from backup
restore_backup() {
    local backup_path=$1
    local target_db=${2:-$DATABASE_NAME}
    
    if [ -z "$backup_path" ]; then
        error "Backup path is required for restore"
        echo "Usage: $0 restore <backup_path> [target_database]"
        exit 1
    fi
    
    if [ ! -d "$backup_path" ]; then
        error "Backup path does not exist: $backup_path"
        exit 1
    fi
    
    warning "This will restore data to database: $target_db"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log "Restore cancelled"
        exit 0
    fi
    
    log "Starting restore from: $backup_path"
    
    # Copy backup to container
    docker cp "$backup_path" "$CONTAINER_NAME:$BACKUP_DIR/restore/"
    
    # Restore backup
    docker exec "$CONTAINER_NAME" mongorestore \
        --host localhost:27017 \
        --authenticationDatabase admin \
        --username project_admin \
        --password project_password \
        --db "$target_db" \
        --gzip \
        --drop \
        "$BACKUP_DIR/restore/$(basename $backup_path)/$target_db" || {
        error "Restore failed!"
        exit 1
    }
    
    success "Restore completed successfully to database: $target_db"
}

# List available backups
list_backups() {
    log "Available backups in $LOCAL_BACKUP_DIR:"
    if [ -d "$LOCAL_BACKUP_DIR" ] && [ "$(ls -A $LOCAL_BACKUP_DIR)" ]; then
        ls -la "$LOCAL_BACKUP_DIR" | grep ^d | awk '{print $9}' | grep -v '^\.$\|^\.\.$'
    else
        warning "No backups found in $LOCAL_BACKUP_DIR"
    fi
}

# Cleanup old backups (keep last N backups)
cleanup_backups() {
    local keep_count=${1:-7}  # Keep last 7 backups by default
    
    log "Cleaning up old backups (keeping last $keep_count)..."
    
    if [ ! -d "$LOCAL_BACKUP_DIR" ]; then
        warning "Backup directory does not exist"
        return
    fi
    
    # Find and remove old backup directories
    find "$LOCAL_BACKUP_DIR" -maxdepth 1 -type d -name "2*" | \
        sort -r | \
        tail -n +$((keep_count + 1)) | \
        while read backup_dir; do
            log "Removing old backup: $(basename "$backup_dir")"
            rm -rf "$backup_dir"
        done
    
    success "Cleanup completed"
}

# Verify backup integrity
verify_backup() {
    local backup_path=$1
    
    if [ -z "$backup_path" ]; then
        error "Backup path is required for verification"
        exit 1
    fi
    
    if [ ! -d "$backup_path" ]; then
        error "Backup path does not exist: $backup_path"
        exit 1
    fi
    
    log "Verifying backup integrity: $backup_path"
    
    # Check if backup contains expected files
    if [ -d "$backup_path/$DATABASE_NAME" ]; then
        local bson_files=$(find "$backup_path/$DATABASE_NAME" -name "*.bson.gz" | wc -l)
        local metadata_files=$(find "$backup_path/$DATABASE_NAME" -name "*.metadata.json.gz" | wc -l)
        
        log "Found $bson_files BSON files and $metadata_files metadata files"
        
        if [ "$bson_files" -gt 0 ] && [ "$metadata_files" -gt 0 ]; then
            success "Backup verification passed"
        else
            error "Backup verification failed - missing files"
            exit 1
        fi
    else
        error "Backup directory structure is invalid"
        exit 1
    fi
}

# Show usage
usage() {
    echo "OrchestrateX MongoDB Backup Script"
    echo
    echo "Usage: $0 <command> [options]"
    echo
    echo "Commands:"
    echo "  full                     - Create full database backup"
    echo "  database [db_name]       - Backup specific database (default: orchestratex)"
    echo "  collection <db> <coll>   - Backup specific collection"
    echo "  restore <path> [db]      - Restore from backup"
    echo "  list                     - List available backups"
    echo "  cleanup [count]          - Remove old backups (keep last N, default: 7)"
    echo "  verify <path>            - Verify backup integrity"
    echo "  help                     - Show this help"
    echo
    echo "Examples:"
    echo "  $0 full"
    echo "  $0 database orchestratex"
    echo "  $0 collection orchestratex user_sessions"
    echo "  $0 restore ./backups/20240828_143022"
    echo "  $0 cleanup 5"
}

# Main script logic
main() {
    case ${1:-help} in
        "full")
            check_container
            prepare_backup_dir
            backup_full
            ;;
        "database")
            check_container
            prepare_backup_dir
            backup_database "$2"
            ;;
        "collection")
            check_container
            prepare_backup_dir
            backup_collection "$2" "$3"
            ;;
        "restore")
            check_container
            restore_backup "$2" "$3"
            ;;
        "list")
            list_backups
            ;;
        "cleanup")
            cleanup_backups "$2"
            ;;
        "verify")
            verify_backup "$2"
            ;;
        "help"|*)
            usage
            ;;
    esac
}

# Run main function with all arguments
main "$@"
