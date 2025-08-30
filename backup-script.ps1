# OrchestrateX MongoDB Backup Script for Windows PowerShell
# Comprehensive backup solution for Docker-based MongoDB on Windows

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(Position=1)]
    [string]$Parameter1,
    
    [Parameter(Position=2)]
    [string]$Parameter2,
    
    [Parameter()]
    [int]$KeepCount = 7
)

# Configuration
$CONTAINER_NAME = "orchestratex_mongodb"
$BACKUP_DIR = "/data/backup"
$LOCAL_BACKUP_DIR = ".\backups"
$DATE = Get-Date -Format "yyyyMMdd_HHmmss"
$DATABASE_NAME = "orchestratex"

# Logging functions
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor Blue
}

function Write-Error-Log {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

function Write-Warning-Log {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

# Check if container is running
function Test-Container {
    $containers = docker ps --format "table {{.Names}}"
    if ($containers -notmatch $CONTAINER_NAME) {
        Write-Error-Log "MongoDB container '$CONTAINER_NAME' is not running!"
        Write-Host "Start it with: docker compose up -d"
        exit 1
    }
    Write-Success "MongoDB container is running"
}

# Create backup directory if it doesn't exist
function Initialize-BackupDir {
    if (!(Test-Path $LOCAL_BACKUP_DIR)) {
        New-Item -ItemType Directory -Path $LOCAL_BACKUP_DIR -Force | Out-Null
        Write-Log "Created backup directory: $LOCAL_BACKUP_DIR"
    }
    
    # Create dated backup subdirectory
    $script:BACKUP_PATH = Join-Path $LOCAL_BACKUP_DIR $DATE
    New-Item -ItemType Directory -Path $BACKUP_PATH -Force | Out-Null
    Write-Log "Backup will be stored in: $BACKUP_PATH"
}

# Full database backup
function Backup-Full {
    Write-Log "Starting full database backup..."
    
    # Create backup inside container
    $result = docker exec $CONTAINER_NAME mongodump `
        --host localhost:27017 `
        --authenticationDatabase admin `
        --username project_admin `
        --password project_password `
        --out "$BACKUP_DIR/$DATE" `
        --gzip
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Log "Full backup failed!"
        exit 1
    }
    
    # Copy backup to host
    docker cp "${CONTAINER_NAME}:$BACKUP_DIR/$DATE" $LOCAL_BACKUP_DIR
    
    Write-Success "Full database backup completed: $LOCAL_BACKUP_DIR\$DATE"
}

# Specific database backup
function Backup-Database {
    param([string]$DbName = $DATABASE_NAME)
    
    Write-Log "Starting backup for database: $DbName"
    
    $result = docker exec $CONTAINER_NAME mongodump `
        --host localhost:27017 `
        --authenticationDatabase admin `
        --username project_admin `
        --password project_password `
        --db $DbName `
        --out "$BACKUP_DIR/$DATE" `
        --gzip
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Log "Database backup failed for: $DbName"
        exit 1
    }
    
    # Copy backup to host
    docker cp "${CONTAINER_NAME}:$BACKUP_DIR/$DATE" $LOCAL_BACKUP_DIR
    
    Write-Success "Database backup completed for $DbName`: $LOCAL_BACKUP_DIR\$DATE"
}

# Specific collection backup
function Backup-Collection {
    param(
        [string]$DbName = $DATABASE_NAME,
        [string]$CollectionName
    )
    
    if ([string]::IsNullOrEmpty($CollectionName)) {
        Write-Error-Log "Collection name is required for collection backup"
        exit 1
    }
    
    Write-Log "Starting backup for collection: $DbName.$CollectionName"
    
    $result = docker exec $CONTAINER_NAME mongodump `
        --host localhost:27017 `
        --authenticationDatabase admin `
        --username project_admin `
        --password project_password `
        --db $DbName `
        --collection $CollectionName `
        --out "$BACKUP_DIR/$DATE" `
        --gzip
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Log "Collection backup failed for: $DbName.$CollectionName"
        exit 1
    }
    
    # Copy backup to host
    docker cp "${CONTAINER_NAME}:$BACKUP_DIR/$DATE" $LOCAL_BACKUP_DIR
    
    Write-Success "Collection backup completed for $DbName.$CollectionName`: $LOCAL_BACKUP_DIR\$DATE"
}

# Restore from backup
function Restore-Backup {
    param(
        [string]$BackupPath,
        [string]$TargetDb = $DATABASE_NAME
    )
    
    if ([string]::IsNullOrEmpty($BackupPath)) {
        Write-Error-Log "Backup path is required for restore"
        Write-Host "Usage: .\backup-script.ps1 restore <backup_path> [target_database]"
        exit 1
    }
    
    if (!(Test-Path $BackupPath)) {
        Write-Error-Log "Backup path does not exist: $BackupPath"
        exit 1
    }
    
    Write-Warning-Log "This will restore data to database: $TargetDb"
    $confirmation = Read-Host "Are you sure you want to continue? (y/N)"
    if ($confirmation -ne "y" -and $confirmation -ne "Y") {
        Write-Log "Restore cancelled"
        exit 0
    }
    
    Write-Log "Starting restore from: $BackupPath"
    
    # Copy backup to container
    docker cp $BackupPath "${CONTAINER_NAME}:$BACKUP_DIR/restore/"
    
    $backupName = Split-Path $BackupPath -Leaf
    
    # Restore backup
    $result = docker exec $CONTAINER_NAME mongorestore `
        --host localhost:27017 `
        --authenticationDatabase admin `
        --username project_admin `
        --password project_password `
        --db $TargetDb `
        --gzip `
        --drop `
        "$BACKUP_DIR/restore/$backupName/$TargetDb"
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error-Log "Restore failed!"
        exit 1
    }
    
    Write-Success "Restore completed successfully to database: $TargetDb"
}

# List available backups
function Get-Backups {
    Write-Log "Available backups in $LOCAL_BACKUP_DIR`:"
    if (Test-Path $LOCAL_BACKUP_DIR) {
        $backups = Get-ChildItem -Path $LOCAL_BACKUP_DIR -Directory | Where-Object { $_.Name -match "^\d{8}_\d{6}$" }
        if ($backups) {
            $backups | Format-Table Name, CreationTime
        } else {
            Write-Warning-Log "No backups found in $LOCAL_BACKUP_DIR"
        }
    } else {
        Write-Warning-Log "Backup directory does not exist"
    }
}

# Cleanup old backups
function Remove-OldBackups {
    param([int]$KeepCount = 7)
    
    Write-Log "Cleaning up old backups (keeping last $KeepCount)..."
    
    if (!(Test-Path $LOCAL_BACKUP_DIR)) {
        Write-Warning-Log "Backup directory does not exist"
        return
    }
    
    $backups = Get-ChildItem -Path $LOCAL_BACKUP_DIR -Directory | 
               Where-Object { $_.Name -match "^\d{8}_\d{6}$" } | 
               Sort-Object CreationTime -Descending
    
    if ($backups.Count -gt $KeepCount) {
        $toDelete = $backups | Select-Object -Skip $KeepCount
        foreach ($backup in $toDelete) {
            Write-Log "Removing old backup: $($backup.Name)"
            Remove-Item -Path $backup.FullName -Recurse -Force
        }
    }
    
    Write-Success "Cleanup completed"
}

# Verify backup integrity
function Test-Backup {
    param([string]$BackupPath)
    
    if ([string]::IsNullOrEmpty($BackupPath)) {
        Write-Error-Log "Backup path is required for verification"
        exit 1
    }
    
    if (!(Test-Path $BackupPath)) {
        Write-Error-Log "Backup path does not exist: $BackupPath"
        exit 1
    }
    
    Write-Log "Verifying backup integrity: $BackupPath"
    
    $dbPath = Join-Path $BackupPath $DATABASE_NAME
    if (Test-Path $dbPath) {
        $bsonFiles = Get-ChildItem -Path $dbPath -Filter "*.bson.gz" -Recurse
        $metadataFiles = Get-ChildItem -Path $dbPath -Filter "*.metadata.json.gz" -Recurse
        
        Write-Log "Found $($bsonFiles.Count) BSON files and $($metadataFiles.Count) metadata files"
        
        if ($bsonFiles.Count -gt 0 -and $metadataFiles.Count -gt 0) {
            Write-Success "Backup verification passed"
        } else {
            Write-Error-Log "Backup verification failed - missing files"
            exit 1
        }
    } else {
        Write-Error-Log "Backup directory structure is invalid"
        exit 1
    }
}

# Show usage
function Show-Usage {
    Write-Host "OrchestrateX MongoDB Backup Script for Windows PowerShell"
    Write-Host ""
    Write-Host "Usage: .\backup-script.ps1 <command> [options]"
    Write-Host ""
    Write-Host "Commands:"
    Write-Host "  full                     - Create full database backup"
    Write-Host "  database [db_name]       - Backup specific database (default: orchestratex)"
    Write-Host "  collection <db> <coll>   - Backup specific collection"
    Write-Host "  restore <path> [db]      - Restore from backup"
    Write-Host "  list                     - List available backups"
    Write-Host "  cleanup [-KeepCount N]   - Remove old backups (keep last N, default: 7)"
    Write-Host "  verify <path>            - Verify backup integrity"
    Write-Host "  help                     - Show this help"
    Write-Host ""
    Write-Host "Examples:"
    Write-Host "  .\backup-script.ps1 full"
    Write-Host "  .\backup-script.ps1 database orchestratex"
    Write-Host "  .\backup-script.ps1 collection orchestratex user_sessions"
    Write-Host "  .\backup-script.ps1 restore .\backups\20240828_143022"
    Write-Host "  .\backup-script.ps1 cleanup -KeepCount 5"
}

# Main script logic
switch ($Command.ToLower()) {
    "full" {
        Test-Container
        Initialize-BackupDir
        Backup-Full
    }
    "database" {
        Test-Container
        Initialize-BackupDir
        Backup-Database -DbName $Parameter1
    }
    "collection" {
        Test-Container
        Initialize-BackupDir
        Backup-Collection -DbName $Parameter1 -CollectionName $Parameter2
    }
    "restore" {
        Test-Container
        Restore-Backup -BackupPath $Parameter1 -TargetDb $Parameter2
    }
    "list" {
        Get-Backups
    }
    "cleanup" {
        Remove-OldBackups -KeepCount $KeepCount
    }
    "verify" {
        Test-Backup -BackupPath $Parameter1
    }
    default {
        Show-Usage
    }
}
