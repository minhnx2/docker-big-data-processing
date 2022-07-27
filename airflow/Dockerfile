FROM apache/airflow:2.3.3
USER root

ENV HIVE_VERSION=${HIVE_VERSION:-3.1.3}
ENV HIVE_HOME /opt/hive
ENV PATH $HIVE_HOME/bin:$PATH

RUN apt-get update && \
    apt-get -y install gcc g++ libsasl2-dev mono-mcs && \   
    apt-get --purge remove -y wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

RUN pip install --no-cache-dir apache-airflow-providers-apache-hive thrift sasl thrift_sasl pyhive 