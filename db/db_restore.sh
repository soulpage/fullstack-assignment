#!/bin/bash

# Configuration
DB_PATH="../backend/db.sqlite3"
BACKUP_DIR="./backups"

# Check if a backup file was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <backup_file>"
    exit 1
fi

BACKUP_FILE="$1"

# Check if the backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file '$BACKUP_FILE' not found."
    exit 1
fi

# Restore the database
cp "$BACKUP_FILE" "$DB_PATH"
echo "Database restored from '$BACKUP_FILE' to '$DB_PATH'."

# Run migrations (optional)
cd ../backend/
python manage.py migrate

# chmod +x db_restore.sh
