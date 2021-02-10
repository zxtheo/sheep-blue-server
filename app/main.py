from flask import Flask, request, json
from flask_cors import CORS
import csv

from os import listdir
from os.path import isfile, join


app = Flask(__name__) 
CORS(app)

@app.route("/") 
def home_view(): 
    return "<h1>you are not in the right place...</h1>"

@app.route("/postdata", methods=["POST"])
def post_data():
    if request.is_json:

        # Parse the JSON into a Python dictionary
        req = request.get_json()
       

        # Print the dictionary
        # print(req)
        save_csv(req)
        # Return a string along with an HTTP status code
        return "JSON received!", 200

    else:

        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@app.route("/getdata", methods=["GET"])
def get_data():
    return make_test_json()

@app.route("/postnet", methods=["POST"])
def post_net():
    if request.is_json:

        # Parse the JSON into a Python dictionary
        req = request.get_json()
       

        # Print the dictionary
        # print(req)
        save_net(req)
        # Return a string along with an HTTP status code
        return "JSON received!", 200

    else:

        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

@app.route("/getnet", methods=["GET"])
def get_net():
    return load_net()


def save_csv(json):
    csv_data = json['csv']
    file_name = json['datetime'].replace('/','-').replace(':', '-')
    #csv = [",".join("'{0}'".format(n) for n in row) for row in csv]
    # print(csv_data)
    with open("app/data/{}.csv".format(file_name), mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL )
        for row in csv_data:
            writer.writerow(row)

def make_test_json():
    onlyfiles = [f for f in listdir("app/data") if isfile(join("app/data", f))]

    json_file = {}
    for file_name in onlyfiles:
        with open("app/data/{}".format(file_name), mode='r', newline='') as csv_file:
            reader = csv.reader(csv_file, delimiter=',', quotechar='"' )
            data = []
            for row in reader:
                data.append(row)

            json_file[file_name] = data

    return ( json.dumps(json_file))

def save_net(net):
    with open("app/net.json", mode='w', newline='') as net_file:
        net_file.truncate(0)
        json.dump(net, net_file)

def load_net():
    with open("app/net.json", mode='r', newline='') as net_file:
        net = json.load(net_file)
        return net