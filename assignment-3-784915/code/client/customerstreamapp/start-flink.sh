mvn install
docker cp target/mysimbdp-0.1-SNAPSHOT.jar flink-jobmanager:/job_user1.jar
docker exec -ti flink-jobmanager flink run /job_user1.jar --amqpurl rabbit  --iqueue in1 --oqueue out1 --parallelism 1