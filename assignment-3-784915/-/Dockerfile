# Pull base Alpine Linux image
FROM openjdk:8-alpine

# Install wget, tar and bash utilities needed to download and install Spark
RUN apk --update add wget tar bash

# Download and install Spark (2.4.0, based on Scala 2.11 and Hadoop 2.7)
RUN wget http://apache.mirror.anlx.net/spark/spark-2.4.0/spark-2.4.0-bin-hadoop2.7.tgz

# Extract archive
RUN tar -xzf spark-2.4.0-bin-hadoop2.7.tgz && \
    mv spark-2.4.0-bin-hadoop2.7 /spark && \
    rm spark-2.4.0-bin-hadoop2.7.tgz

# Create launching scripts
COPY start-master.sh /start-master.sh
COPY start-worker.sh /start-worker.sh





  spark-master:
    image: gettyimages/spark
    container_name: spark-master
    hostname: spark-master
    command: bin/spark-class org.apache.spark.deploy.master.Master -h master
    environment:
      MASTER: spark://master:7077
      SPARK_CONF_DIR: /conf
      #SPARK_PUBLIC_DNS: localhost
    ports:
      - 7077:7077
      - 8080:8080
    volumes:
      - ./mysimbdp-analytics/conf/master:/conf
      - ./mysimbdp-analytics/data:/tmp/data

  spark-worker:
    image: gettyimages/spark
    container_name: spark-worker
    hostname: spark-worker
    command: bin/spark-class org.apache.spark.deploy.worker.Worker spark://master:7077
    environment:
      SPARK_CONF_DIR: /conf
      SPARK_WORKER_CORES: 1
      SPARK_WORKER_MEMORY: 1g
      SPARK_WORKER_PORT: 8881
      SPARK_WORKER_WEBUI_PORT: 8081
      #SPARK_PUBLIC_DNS: localhost
    links:
      - spark-master
      - kafka
      - cassandra
    expose:
      - 8881
    ports:
      - 8081:8081
    volumes:
      - ./mysimbdp-analytics/conf/worker:/conf
      - ./mysimbdp-analytics/data:/tmp/data