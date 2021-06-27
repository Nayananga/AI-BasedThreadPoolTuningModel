#!/bin/bash

docker container kill db_Server some-redis tuner java_service jmeter_service
docker container prune -f

docker network prune -f
docker network create --subnet=192.168.1.0/24 myNet

## Spawn mysql db server
docker run --publish 3306:3306 --name db_Server -d --net myNet --ip 192.168.1.6 --cpus=1 nayanagamuhandiram/mysql_service

#Prime

##Concurrency 1

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/Prime1m_1:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py Prime1m_1
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/Prime1m_1:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 1_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

##Concurrency 10

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/Prime1m_10:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py Prime1m_10
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/Prime1m_10:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 10_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

##Concurrency 50

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/Prime1m_50:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py Prime1m_50
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/Prime1m_50:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 50_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

#DbWrite

##Concurrency 1

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/DbWrite_1:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py DbWrite_1
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/DbWrite_1:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 1_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

##Concurrency 10

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/DbWrite_10:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py DbWrite_10
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/DbWrite_10:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 10_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

##Concurrency 50

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/DbWrite_50:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py DbWrite_50
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/DbWrite_50:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 50_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

#DbRead

##Concurrency 1

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/DbRead_1:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py DbRead_1
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/DbRead_1:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 1_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

##Concurrency 10

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/DbRead_10:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py DbRead_10
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/DbRead_10:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 10_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

##Concurrency 50

docker run --publish 6379:6379 --name some-redis -d --net myNet --ip 192.168.1.2 --cpus=1 redis
docker run --publish 5000:5000 --name tuner -d --net myNet --ip 192.168.1.3 --volume /home/nayananga/output/isuru/python/DbRead_50:/app/Data/ACTUAL --cpus=1 nayanagamuhandiram/python_service:hpc_testing_5  python app.py DbRead_50
docker run --publish 15000:15000 --name java_service -d --net myNet --ip 192.168.1.4 --volume /home/nayananga/output/isuru/java/DbRead_50:/home/log --cpus=1 nayanagamuhandiram/java_service java -jar adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P
docker run --name jmeter_service -d --net myNet --ip 192.168.1.5 --cpus=1 nayanagamuhandiram/jmeter_service java -jar bin/ApacheJMeter.jar -n -t 50_concurrency.jmx -q user.properties
sleep 1200
docker container kill jmeter_service
sleep 120
docker container kill some-redis tuner java_service
docker container prune -f

docker network prune -f
exit