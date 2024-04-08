import json
import random
import time
from datetime import datetime
import pandas as pd
import socket
import matplotlib.pyplot as plt
import numpy as np
from flask import Flask, render_template, jsonify
import re
import csv
import time
from flask import Flask, Response, render_template, stream_with_context
import random

application = Flask(__name__)
random.seed()  # Initialize the random number generator

def generate_data():
    raspberrypiData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    raspberrypiData.connect(('192.168.11.90', 5000))
    data_decode = (raspberrypiData.recv(1024).decode('utf-8'))
    return data_decode
def timer():
    t = time.time()  # UNIX時間（1970/01/01 00:00:00からの経過時刻）を取得
    local_time = time.localtime(t)  # ローカル時刻をtime.struct_time型として取得
    asc_time = time.asctime(local_time)  # 上のlocal_timeを文字列表現に変換
    dt = datetime.now().strptime(asc_time, '%a %b %d %H:%M:%S %Y')
    return dt

# def generate_data1():
#     raspberrypiData = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     raspberrypiData.connect(('192.168.11.75', 6000))
#     data_decode = (raspberrypiData.recv(1024).decode('utf-8'))
#     return data_decode

@application.route('/')
def index():
            data_decode = generate_data()
            split = re.split('\s+', data_decode)
            temperature = float(split[0])
            humidity = float(split[1])
            pressure = float(split[2])
            sensor = [
                {
                    "temperature": temperature,
                    "huminity": humidity,
                    "pressure": pressure
                }
            ]
            return render_template('index.html', text=sensor)   

@application.route('/data')
def data():
    while True:
        sensor_data = generate_data()
        split = re.split('\s+', sensor_data)
        print("split", split)
        temperature = float(split[0])
        humidity = float(split[1])
        pressure = float(split[2])
        data = [
            {
                "temperature": temperature,
                "huminity": humidity,
                "pressure": pressure
            }
        ]
        return jsonify(data)

@application.route('/chart-data')
def chart_data():
    def generate_random_data():
        data = []
        while True:
            nowtime = timer()
            sensor_data = generate_data()
            split = re.split('\s+', sensor_data)
            print("split", split)
            temperature = float(split[0])
            humidity = float(split[1])
            pressure = float(split[2])
            data.append([nowtime, temperature, humidity, pressure])
            suujirandom = random.randrange(25, 27)
            print("suujirandom", suujirandom)
            with open('sample.csv', 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': temperature, 'value1': humidity, 'value2': suujirandom})
            yield f"data:{json_data}\n\n"
            time.sleep(10)
    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@application.route('/chart-data1')
def chart_data1():
    def generate_random_data():
        while True:
            sensor_data = generate_data()
            split = re.split('\s+', sensor_data)
            print("split", split)
            humidity = float(split[1])
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': humidity})
            yield f"data:{json_data}\n\n"
            time.sleep(10)
    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response

@application.route('/chart-data2')
def chart_data2():
    def generate_random_data():
        while True:
            sensor_data = generate_data()
            split = re.split('\s+', sensor_data)
            print("split", split)
            pressure = float(split[2])
            json_data = json.dumps(
                {'time': datetime.now().strftime('%H:%M:%S'), 'value': pressure})
            yield f"data:{json_data}\n\n"
            time.sleep(10)
    response = Response(stream_with_context(generate_random_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == "__main__":
    application.run(debug=True, host="localhost", port=3000)