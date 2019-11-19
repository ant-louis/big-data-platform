install:
	docker build -t spark-base:latest ./spark-base
	docker build -t spark-master:latest ./spark-master
	docker build -t spark-worker:latest ./spark-worker
	docker build -t spark-submit:latest ./spark-submit
	docker-compose -f docker-compose.yml down -v
	docker-compose -f docker-compose.yml up -d --scale spark-worker=2 --force-recreate
