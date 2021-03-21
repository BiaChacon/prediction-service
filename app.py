
from flask import Flask, jsonify, request
import os
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

DB_URL = os.environ.get("DB_URL")
client = MongoClient(DB_URL)
db = client.database
nodes = db.nodes

@app.route('/', methods=['GET'])
def index():
    return "<h1>Rodou! Show de buela</h1>"

@app.route('/data', methods=['GET'])
def get_all_data():
    output = []
    for i in nodes.find():
        output.append({'id_node' : i['id_node'], 'datetime' : i['datetime'], 'sensors' : i['sensors']})
    return jsonify(output)

@app.route('/add', methods=['POST'])
def add_data():
    id_node = request.json['id_node']
    sensors = request.json['sensors']

    tz = timezone('America/Sao_Paulo')
    now = datetime.now()
    datetimenow = now.astimezone(tz)
    dt = datetimenow.strftime('%d/%m/%Y %H:%M')

    _id = nodes.insert({'id_node': id_node, 'datetime': dt, 'sensors': sensors})

    new_data = db.nodes.find_one({'_id': _id })
    output = {'id_node' : new_data['id_node'], 'datetime': new_data['datetime'], 'sensors' : new_data['sensors']}
    return jsonify(output)

def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()