#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
ENV_FILE=$SCRIPT_DIR/.env

# ======================================================================================================================

# The environment vairables below will be written
# to the .env file in the directory along with this script.

# Please keep environment variables in the current script
# alphabetically sorted and use double quotes around the values.

# You can read more why we need to use quotes here:
# https://stackoverflow.com/a/71538763/8431075

cat > $ENV_FILE << EOF
BUILDX_CACHE_DEST="/tmp/.buildx-cache-new"
BUILDX_CACHE_SRC="/tmp/.buildx-cache"

DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION="1"
DAYS_BEFORE_REFRESH_TOKEN_EXPIRATION="60"

# Minio related variables are not used for envs/ci/db checks
# because we don't need to connect to minio to check db-related stuff.
# But these variables are required by the application config.
# And since alembic uses application config to connect to db
# we need to provide them even if they're not used in this case.
MINIO_HOST="minio"
MINIO_PORT="9000"
MINIO_ROOT_PASSWORD="minioadmin"
MINIO_ROOT_USER="minioadmin"
MINIO_SCHEMA="HTTP"

POSTGRES_DB="postgres"
POSTGRES_HOST="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_PORT="5432"
POSTGRES_USER="postgres"

SECRET_KEY="keyboardcat"
EOF

# ======================================================================================================================

cat << EOF

Default environment variables has been written to:
$ENV_FILE

This setup should just work fine right out of the box,
but you can adjust this file in the way you want.

EOF
