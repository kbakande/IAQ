from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import requests

#set up the sensor parameters
sensorIDs = [25879, 8510, 61397, 33729]
link ="https://www.purpleair.com/json?show={}".format(sensorIDs[1])

#upload the trained model
model = pickle.load(open('../model.pkl', 'rb'))

def create_app():
    app = Flask(__name__)

    CORS(app, resources = {r"/*": {"origins" : "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allowed-Headers", "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allowed-Methods", "GET, PATCH, POST, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allowed-Origin", "*")
        return response

    @app.route('/')
    def home():
        return "Welcome to Healthy-Air - Improving the Indoor Air Quality"

    @app.route('/predict', methods=["POST"])
    def predict():
        data = request.get_json()["data"]
        PM_predicted = model.predict([data]).tolist()
        return jsonify({"PM_predicted" : PM_predicted})

    @app.route('/live')
    def liveReadings():
        data = requests.get(link).json()
        PM2_5 = data["results"][0]["PM2_5Value"]
        PM10 = data["results"][0]["pm10_0_cf_1"]
        temp = data["results"][0]["temp_f"]
        Humidity = data["results"][0]["humidity"]
        Pressure = data["results"][0]["pressure"]
        liveVals = {"PM2.5": PM2_5, "PM10": PM10, "temp": temp, "humid": Humidity, "pres": Pressure}
        print(liveVals)
        return jsonify(liveVals)

    return app

app = create_app()

# if __name__ == "__main__":
#     app.run()