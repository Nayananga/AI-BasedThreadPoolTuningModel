import random

from flask import Flask, request

app = Flask(__name__)


@app.route('/', methods=['POST'])
def threadpool_tuner():
    request_data = request.get_json()

    print(request_data)

    return str(random.randint(0, 100))


if __name__ == '__main__':
    app.run()
