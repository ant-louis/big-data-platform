#!/bin/bash

/spark/bin/spark-submit \
--packages ${SPARK_PACKAGES} \
--master ${SPARK_MASTER_URL} \
${SPARK_APPLICATION} \
