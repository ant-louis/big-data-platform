# Locate the user app in the server
SPARK_APPLICATION="/opt/spark-apps/customerstreamapp1.py"

#We have to use the same network as the spark cluster(internally the image resolves spark master as spark://spark-master:7077)
docker run --network code_spark-network \
-v "/$(pwd)/../mysimbdp-analytics/spark-apps:/opt/spark-apps" \
--env SPARK_APPLICATION=$SPARK_APPLICATION \
spark-submit:latest