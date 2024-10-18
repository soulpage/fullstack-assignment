# Script to wait for SQLite to be ready

set -e

until [ -e /app/backend/db.sqlite3 ]; do
    >&2 echo "+ SQLite is not ready"
    sleep 1
done

>&2 echo "+ SQLite is ready - exec command"
exec "$@"
