# Auto-Tuning-with-Bayesian

Developed for maximum one parameter and one feature.

Define the variables in Config.py

Run - 1.docker run --name some-redis -d -p 6379:6379 redis 2.pip install requirements.txt -r 3.python3 app.py

Data is generated in the data generator

To change the concurrency changing function write a new function in
/Auto-Tuning-with-Bayesian/data_generation/feature_generator.py/ and call the function name from the config.py
