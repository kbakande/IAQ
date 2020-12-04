from flask import Flask, jsonify, request
from datetime import datetime as dt, timedelta
import pandas as pd
from flask_cors import CORS
import pickle
import requests

# set up the sensor parameters
sensorIDs = [25879, 8510, 61397, 33729, 59391]
pollutants = {"PM1.0": 0, "PM2.5": 1,
              "PM10.0": 2, "Temperature": 5, "Humidity": 6}
link = "https://www.purpleair.com/json?show={}".format(sensorIDs[2])

# upload the trained model
# model = pickle.load(open('../models/model.pkl', 'rb'))

# function to retrieve past week data


def getPastData(sensorId, dtReq, pollutant):
    sensor = sensorIDs[sensorId]

    fileStr = "../sensorData/" + str(sensor) + ".csv"
    def custom_parser(date): return dt.strptime(date, '%Y-%m-%d')
    sensorDf = pd.read_csv(fileStr, parse_dates=[
                           'created_at'], date_parser=custom_parser)
    sensorDf = sensorDf.drop_duplicates(subset=["created_at"], keep='first')
    sensorDf = sensorDf.set_index('created_at')

    wk_days = []
    wk_dates = []
    start_dt = dt.strptime(dtReq, '%Y-%m-%d')
    end_dt = start_dt - timedelta(days=6)

    def daterange(date1, date2):
        for n in range(int((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    for dts in daterange(end_dt, start_dt):
        wk_days.append(dts.strftime("%A"))
        wk_dates.append(dts.strftime("%Y-%m-%d"))

    dataList = sensorDf.loc[wk_dates[0]: wk_dates[-1],
                            sensorDf.columns[pollutants[pollutant]]].values.tolist()
    return(dataList, wk_dates, wk_days)


def getForecastData(sensorId, dtReq, pollutant):
    sensor = sensorIDs[sensorId]

    fileStr = "../sensorData/" + str(sensor) + ".csv"
    def custom_parser(date): return dt.strptime(date, '%Y-%m-%d')
    sensorDf = pd.read_csv(fileStr, parse_dates=[
                           'created_at'], date_parser=custom_parser)
    sensorDf = sensorDf.drop_duplicates(subset=["created_at"], keep='first')
    sensorDf = sensorDf.set_index('created_at')

    wk_days = []
    wk_dates = []
    start_dt = dt.strptime(dtReq, '%Y-%m-%d')
    end_dt = start_dt - timedelta(days=3)

    def daterange(date1, date2):
        for n in range(int((date2 - date1).days)+1):
            yield date1 + timedelta(n)

    for dts in daterange(end_dt, start_dt):
        wk_days.append(dts.strftime("%A"))
        wk_dates.append(dts.strftime("%Y-%m-%d"))
    dataList = sensorDf.loc[wk_dates[0]: wk_dates[-1],
                            sensorDf.columns[pollutants[pollutant]]].values.tolist()

    avg = sum(dataList)/len(dataList)
    dataList.append(avg)

    # get the dates and days for 3day forecast
    futureDays = []
    futureDates = []
    tday = dt.strptime(wk_dates[-1], '%Y-%m-%d')
    forecastEndDate = tday + timedelta(days=3)
    for dts in daterange(tday, forecastEndDate):
        futureDays.append(dts.strftime("%A"))
        futureDates.append(dts.strftime("%Y-%m-%d"))
    return(dataList, futureDates, futureDays)


def getForecastVals(dataList, wk_dates, wk_days):
    wk_dates = wk_dates[1:]
    wk_days = wk_days[1:]
    forecastList = []
    for k in range(len(wk_dates)):
        tempForecast = round(sum(dataList[-3:])/len(dataList[-3:]), 2)
        forecastList.append(tempForecast)
        dataList.append(tempForecast)
        print(forecastList)
    return(forecastList, wk_days, wk_dates)


def create_app():
    app = Flask(__name__)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allowed-Headers",
                             "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allowed-Methods",
                             "GET, PATCH, POST, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allowed-Origin", "*")
        return response

    @app.route('/')
    def home():
        return "Welcome to Healthy-Air - Improving the Indoor Air Quality"

    # @app.route('/predict', methods=["POST"])
    # def predict():
    #     data = request.get_json()["data"]
    #     PM_predicted = model.predict([data]).tolist()
    #     return jsonify({"PM_predicted": PM_predicted})

    @app.route('/live')
    def liveReadings():
        data = requests.get(link).json()
        PM2_5 = data["results"][0]["PM2_5Value"]
        PM10 = data["results"][0]["pm10_0_cf_1"]
        temp = data["results"][0]["temp_f"]
        Humidity = data["results"][0]["humidity"]
        Pressure = data["results"][0]["pressure"]
        PM1_0 = data["results"][0]["pm1_0_cf_1"]
        liveVals = {"PM2.5": PM2_5, "PM10": PM10,
                    "temp": temp, "humid": Humidity, "pres": Pressure, "PM1.0": PM1_0}
        return jsonify(liveVals)

    @app.route('/pastData', methods=['POST'])
    def getWeekData():
        data = request.get_json()
        sensorid = data["sensor"]
        pollutant = data["pollutant"]
        reqDate = data["reqDate"]

        [dataList, wk_dates, wk_days] = getPastData(
            sensorid, reqDate, pollutant)

        return jsonify({"dataList": dataList, "wkDates": wk_dates, "wkDays": wk_days})

    @app.route('/forecast', methods=['POST'])
    def getForecast():
        data = request.get_json()
        sensorid = data["sensor"]
        pollutant = data["pollutant"]
        reqDate = data["reqDate"]

        [dataList, wk_dates, wk_days] = getForecastData(
            sensorid, reqDate, pollutant)

        [forcastList, forcastDates, forcastDays] = getForecastVals(
            dataList, wk_dates, wk_days)
        return jsonify({"forecastList": forcastList, "forcastDates": forcastDates, "forcastDays": forcastDays})

    return app


app = create_app()

# if __name__ == "__main__":
#     app.run()
