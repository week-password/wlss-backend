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
DAYS_BEFORE_ACCESS_TOKEN_EXPIRATION="1"
DAYS_BEFORE_REFRESH_TOKEN_EXPIRATION="60"

MINIO_HOST="minio"
MINIO_PORT="9000"
MINIO_ROOT_PASSWORD=""  # provide correct value here
MINIO_ROOT_USER=""  # provide correct value here
MINIO_SCHEMA="HTTP"

POSTGRES_DB="postgres"
POSTGRES_HOST="postgres"
POSTGRES_PASSWORD=""  # provide correct value here
POSTGRES_PORT="5432"
POSTGRES_USER=""  # provide correct value here

SECRET_KEY="keyboardcat"
EOF

# ======================================================================================================================

cat << EOF

Default environment variables has been written to:
$ENV_FILE

Please adjust variables in this file.

EOF
