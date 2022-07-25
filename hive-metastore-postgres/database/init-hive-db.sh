#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
  CREATE DATABASE metastore;
  GRANT ALL PRIVILEGES ON DATABASE metastore TO $POSTGRES_USER;
  \c metastore

  \i /hive/hive-schema-2.3.0.postgres.sql
  \i /hive/hive-txn-schema-2.3.0.postgres.sql
  \i /hive/upgrade-2.3.0-to-3.0.0.postgres.sql
  \i /hive/upgrade-3.0.0-to-3.1.0.postgres.sql
EOSQL