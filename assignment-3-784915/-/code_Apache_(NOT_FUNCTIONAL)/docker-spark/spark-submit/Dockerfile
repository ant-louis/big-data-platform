FROM spark-base:latest

COPY start-submit.sh /

ENV SPARK_MASTER_URL="spark://spark-master:7077"
ENV SPARK_APPLICATION=""
ENV SPARK_PACKAGES="org.apache.spark:spark-streaming-kafka-0-8_2.11:2.4.4"

CMD ["/bin/bash", "/start-submit.sh"]