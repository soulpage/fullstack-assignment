#!/bin/bash

# Configuration
DB_PATH="../backend/db.sqlite3"       # Path to your SQLite database
BACKUP_DIR="./backups"            # Directory where backups will be stored
DATE=$(date +%Y-%m-%d_%H-%M-%S)          # Timestamp for the backup filename

# Make the backup directory if it doesn't exist
sudo mkdir -p $BACKUP_DIR

# Backup the SQLite database by copying it to the backup folder with a timestamp
sudo cp $DB_PATH $BACKUP_DIR/db_backup_$DATE.sqlite3

# Optionally, clean up backups older than 7 days
sudo find $BACKUP_DIR -type f -name "*.sqlite3" -mtime +7 -exec rm -f {} \;

echo "Backup completed: $BACKUP_DIR/db_backup_$DATE.sqlite3"

# Crontab Configuration
# chmod +x db_backup.sh
# crontab -e
# 0 3 * * * db_backup.sh - running at 3AM everyday
