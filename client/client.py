import requests
import time
import json
import csv
from datetime import datetime

i = 0

client = './data/client_y.csv'
# client_heroku = './data/X/client_x_2.csv'

while(i < 144):
    print("########################################################")
    print(i)
    i = i+1
    temp_real, hum_real, temp_predict, hum_predict, temp_predict2, hum_predict2 = (
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    r1 = requests.get("http://localhost:5000/now?idNode=ESP")
    real = json.loads(r1.json())
    temp_real = real['sensors'][0]['value']
    hum_real = real['sensors'][1]['value']

    r2 = requests.get("http://localhost:5001/predict")
    print(r2.json())
    predict = json.loads(json.dumps(r2.json()))
    temp_predict = predict['data_predict']['temperature']['value']
    hum_predict = predict['data_predict']['humidity']['value']

    # r3 = requests.get("https://prediction-service-api.herokuapp.com/predict")
    # predict2 = json.loads(json.dumps(r3.json()))
    # temp_predict2 = predict2['data_predict']['temperature']['value']
    # hum_predict2 = predict2['data_predict']['humidity']['value']

    # print("#################### Valor Temperatura #################")
    # print("Real:", temp_real)
    # print("Predição:", temp_predict, "---", "heroku:", temp_predict2)
    # print("#################### Valor Humidade ####################")
    # print("Real:", hum_real)
    # print("Predição:", hum_predict, "---", "heroku: ", hum_predict2)
    # print("########################################################")

    print("#################### Valor Temperatura #################")
    print("Real:", temp_real, "Predição:", temp_predict)
    print("#################### Valor Humidade ####################")
    print("Real:", hum_real, "Predição:", hum_predict)
    print("########################################################")

    datetime_format = "%d/%m/%Y %H:%M"
    date_read = datetime.now()
    date_time = str(date_read.strftime(datetime_format))

    with open(client, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [date_time, temp_real, temp_predict, hum_real, hum_predict]
        )

    print("Salvo")
    time.sleep(600)
