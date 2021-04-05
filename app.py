from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
import threading
import time
import json
import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.neural_network import MLPRegressor

app = Flask(__name__)

DB_URL = os.environ.get("DB_URL")
client = MongoClient(DB_URL)
db = client.db1
nodes = db.nodes

data = []
qtd_data = 0
TIME_TRAINING = 300

# Setting the date in a string var...
datetime_format = "%d/%m/%Y %H:%M"
date_read = datetime.now()
date_time_last = str(date_read.strftime(datetime_format))

model_1 = MLPRegressor(activation='relu',
                       hidden_layer_sizes=(6,),
                       learning_rate='constant',
                       learning_rate_init=0.1,
                       max_iter=500,
                       momentum=0.5,
                       solver='lbfgs'
                       )

model_2 = MLPRegressor(activation='relu',
                       hidden_layer_sizes=(6,),
                       learning_rate='constant',
                       learning_rate_init=0.1,
                       max_iter=500,
                       momentum=0.5,
                       solver='lbfgs'
                       )

predictions_1 = []
predictions_2 = []

X_train_1 = None
X_test_1 = None
y_train_1 = None
y_test_1 = None
X_train_2 = None
X_test_2 = None
y_train_2 = None
y_test_2 = None


@ app.route('/', methods=['GET'])
def index():
    global data
    return jsonify(data)


@ app.route('/add', methods=['POST'])
def add_data():
    id_node = request.json['id_node']
    sensors = request.json['sensors']

    tz = timezone('America/Sao_Paulo')
    now = datetime.now()
    datetimenow = now.astimezone(tz)
    dt = datetimenow.strftime('%d/%m/%Y %H:%M')

    _id = nodes.insert(
        {'id_node': id_node, 'datetime': dt, 'sensors': sensors})

    new_data = db.nodes.find_one({'_id': _id})
    output = {'id_node': new_data['id_node'],
              'datetime': new_data['datetime'], 'sensors': new_data['sensors']}
    return jsonify(output)


@ app.route('/predict', methods=['GET'])
def get_predict():
    global model_1, model_2, y_test_1, predictions_1, y_test_2, predictions_2

    now = datetime.now()
    dt = str(now.strftime('%d/%m/%Y %H:%M'))
    hora = now.hour*60
    t = hora+now.minute

    temperature = pd.Series(model_1.predict(np.array([[t]]))).to_json(
        orient='values').replace('[', '').replace(']', '')
    humidity = pd.Series(model_2.predict(np.array([[t]]))).to_json(
        orient='values').replace('[', '').replace(']', '')

    predictions_1 = model_1.predict(X_test_1)
    predictions_2 = model_2.predict(X_test_2)
    print(predictions_1)
    print(predictions_2)

    output = {
        'datetime': dt,
        'data_predict': {
            'temperature': {
                'value': round(float(temperature), 2),
                'MAE': round(metrics.mean_absolute_error(y_test_1, predictions_1), 2),
                'MSE': round(metrics.mean_squared_error(y_test_1, predictions_1), 2),
                'RMSE': round(np.sqrt(metrics.mean_squared_error(y_test_1, predictions_1)), 2)
            },
            'humidity': {
                'value': round(float(humidity), 2),
                'MAE': round(metrics.mean_absolute_error(y_test_2, predictions_2), 2),
                'MSE': round(metrics.mean_squared_error(y_test_2, predictions_2), 2),
                'RMSE': round(np.sqrt(metrics.mean_squared_error(y_test_2, predictions_2)), 2)
            }
        },
    }

    return jsonify(output)


def get_data_initial():
    global data, qtd_data
    for i in nodes.find():
        datetime_in_string = i['datetime']
        dt = datetime.strptime(datetime_in_string, datetime_format)
        hora = dt.hour*60
        t = hora+dt.minute
        data.append(
            {'datetime': t, 'temperature': i['sensors'][0]['value'], 'humidity': i['sensors'][1]['value']})
    qtd_data = len(data)
    print("Base de dados inserida")


def training_initial():
    global model_1, model_2, data, X_train_1, X_test_1, y_train_1, y_test_1, X_train_2, X_test_2, y_train_2, y_test_2
    get_data_initial()
    print("Training initial...")
    df = pd.DataFrame(data)

    X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(df.drop(
        columns=['temperature', 'humidity']), df['temperature'], random_state=1)
    X_train_2, X_test_2, y_train_2, y_test_2 = train_test_split(df.drop(
        columns=['temperature', 'humidity']), df['humidity'], random_state=1)

    model_1.fit(X_train_1, y_train_1)
    model_2.fit(X_train_2, y_train_2)

    print("initial models created")


def get_data():
    global date_read, date_time_last, data, qtd_data
    output = []
    print("datetime last training:", date_time_last)
    count = nodes.count_documents({})-qtd_data
    print("qtd new data:", count)
    if(count > 0):
        c = 0
        for i in nodes.find():
            c = c+1
            if(c > len(data)):
                datetime_in_string = i['datetime']
                dt = datetime.strptime(datetime_in_string, datetime_format)
                hora = dt.hour*60
                t = hora+dt.minute
                output.append(
                    {'datetime': t, 'temperature': i['sensors'][0]['value'], 'humidity': i['sensors'][1]['value']})
                data.append(
                    {'datetime': t, 'temperature': i['sensors'][0]['value'], 'humidity': i['sensors'][1]['value']})
        date_read = datetime.now()
        date_time_last = str(date_read.strftime(datetime_format))
    qtd_data = len(data)
    print("qtd data:", len(data))
    return output


def training():
    global model_1, model_2, data
    while True:
        time.sleep(TIME_TRAINING)
        print("Training...")
        dataNew = get_data()
        if(len(dataNew) == 0):
            print("nothing new for training")
        else:
            print("partial fit for new data")
            df = pd.DataFrame(dataNew)
            model_1.partial_fit(
                df.drop(columns=['temperature', 'humidity']), df['temperature'])
            model_2.partial_fit(
                df.drop(columns=['temperature', 'humidity']), df['humidity'])


def startWebServer():
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, host='0.0.0.0', port=port, threaded=True)


if __name__ == "__main__":
    threading.Thread(target=training_initial).start()
    threading.Thread(target=training).start()
    startWebServer()
