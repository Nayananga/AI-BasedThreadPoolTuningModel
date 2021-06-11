#!/bin/bash

docker kill some-redis
docker rm some-redis
docker run --name some-redis -d -p 6379:6379 redis
source /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/venv/bin/activate
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
##Concurrency 1

#Prime10k
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime10k_1 &
java -jar -DLOG_FILE_NAME=Prime10k_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime10k 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime10k_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime100k
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime100k_1 &
java -jar -DLOG_FILE_NAME=Prime100k_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime100k 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime100k_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime1m
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime1m_1 &
java -jar -DLOG_FILE_NAME=Prime1m_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime1m_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime10m
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime10m_1 &
java -jar -DLOG_FILE_NAME=Prime10m_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime10m 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime10m_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#DbWrite
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py DbWrite_1 &
java -jar -DLOG_FILE_NAME=DbWrite_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar DbWrite 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/DbWrite_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#DbRead
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py DbRead_1 &
java -jar -DLOG_FILE_NAME=DbRead_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar DbRead 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/DbRead_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Sqrt
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Sqrt_1 &
java -jar -DLOG_FILE_NAME=Sqrt_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Sqrt 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Sqrt_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Factorial
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Factorial_1 &
java -jar -DLOG_FILE_NAME=Factorial_1 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Factorial 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/1_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Factorial_1.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)

##Concurrency 10

#Prime10k
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime10k_10 &
java -jar -DLOG_FILE_NAME=Prime10k_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime10k 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime10k_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime100k
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime100k_10 &
java -jar -DLOG_FILE_NAME=Prime100k_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime100k 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime100k_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime1m
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime1m_10 &
java -jar -DLOG_FILE_NAME=Prime1m_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime1m_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime10m
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime10m_10 &
java -jar -DLOG_FILE_NAME=Prime10m_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime10m 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime10m_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#DbWrite
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py DbWrite_10 &
java -jar -DLOG_FILE_NAME=DbWrite_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar DbWrite 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/DbWrite_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#DbRead
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py DbRead_10 &
java -jar -DLOG_FILE_NAME=DbRead_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar DbRead 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/DbRead_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Sqrt
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Sqrt_10 &
java -jar -DLOG_FILE_NAME=Sqrt_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Sqrt 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Sqrt_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Factorial
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Factorial_10 &
java -jar -DLOG_FILE_NAME=Factorial_10 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Factorial 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/10_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Factorial_10.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)

##Concurrency 50

#Prime10k
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime10k_50 &
java -jar -DLOG_FILE_NAME=Prime10k_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime10k 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime10k_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime100k
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime100k_50 &
java -jar -DLOG_FILE_NAME=Prime100k_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime100k 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime100k_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime1m
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime1m_50 &
java -jar -DLOG_FILE_NAME=Prime1m_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime1m 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime1m_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Prime10m
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Prime10m_50 &
java -jar -DLOG_FILE_NAME=Prime10m_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Prime10m 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Prime10m_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#DbWrite
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py DbWrite_50 &
java -jar -DLOG_FILE_NAME=DbWrite_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar DbWrite 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/DbWrite_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#DbRead
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py DbRead_50 &
java -jar -DLOG_FILE_NAME=DbRead_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar DbRead 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/DbRead_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Sqrt
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Sqrt_50 &
java -jar -DLOG_FILE_NAME=Sqrt_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Sqrt 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Sqrt_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
#Factorial
python3 /home/nayananga/PycharmProjects/AI-BasedThreadPoolTuningModel/app.py Factorial_50 &
java -jar -DLOG_FILE_NAME=Factorial_50 ~/Desktop/adaptive-concurrency-control_original/target/adaptive-concurrency-control-1.0-SNAPSHOT-jar-with-dependencies.jar Factorial 10 99P &
java -jar ~/Downloads/apache-jmeter-5.4/bin/ApacheJMeter.jar -n -t ~/Desktop/jmeter_service/50_concurrency.jmx -l ~/Desktop/jmeter_service/jmeter_results_with_pretrained_data/Factorial_50.jtl -q ~/Desktop/jmeter_service/performance_common/distribution/scripts/jmeter/user.properties &
wait
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:5000)
# shellcheck disable=SC2046
kill -9 $(lsof -t -i tcp:15000)
exit