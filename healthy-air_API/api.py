from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle


model = pickle.load(open('../model.pkl', 'rb'))

def create_app():
    app = Flask(__name__)

    CORS(app, resources = {r"/*": {"origins" : "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allowed-Headers", "Content-Type, Authorization, true")
        response.headers.add("Access-Control-Allowed-Methods", "GET, PATCH, POST, DELETE, OPTIONS")
        return response

    @app.route('/')
    def home():
        return "Welcome to Healthy-Air - Improving the Indoor Air Quality"

    @app.route('/predict', methods=["POST"])
    def predict():
        data = request.get_json()["data"]
        PM_predicted = model.predict([data]).tolist()
        return jsonify({"PM_predicted" : PM_predicted})




    return app

app = create_app()

# if __name__ == "__main__":
#     app.run()