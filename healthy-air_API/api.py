from flask import Flask, jsonify, request
import pickle


model = pickle.load(open('../model.pkl', 'rb'))

def create_app():
    app = Flask(__name__)

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