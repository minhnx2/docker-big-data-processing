FROM postgres:13

MAINTAINER "minhnx2"

COPY database/hive-schema-2.3.0.postgres.sql /hive/hive-schema-2.3.0.postgres.sql
COPY database/hive-txn-schema-2.3.0.postgres.sql /hive/hive-txn-schema-2.3.0.postgres.sql
COPY database/upgrade-2.3.0-to-3.0.0.postgres.sql /hive/upgrade-2.3.0-to-3.0.0.postgres.sql
COPY database/upgrade-3.0.0-to-3.1.0.postgres.sql /hive/upgrade-3.0.0-to-3.1.0.postgres.sql

COPY database/init-hive-db.sh /docker-entrypoint-initdb.d/init-user-db.sh