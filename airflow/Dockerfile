FROM apache/airflow:2.3.3
USER root

RUN apt-get update && \
    apt-get -y install gcc g++ libsasl2-dev mono-mcs && \
    rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir apache-airflow-providers-apache-hive