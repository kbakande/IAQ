from flask import Flask, jsonify, request
import pickle



def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Welcome to Healthy-Air - Improving the Indoor Air Quality"

    @app.route('/predict', methods=["POST"])
    def predict():
        data = request.get_json()
        data_json = data['data'][0]
        return jsonify(data_json)




    return app

app = create_app()

# if __name__ == "__main__":
#     app.run()