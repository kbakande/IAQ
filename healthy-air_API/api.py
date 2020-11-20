from flask import Flask, jsonify



def create_app():
    app = Flask(__name__)

    @app.route('/')
    def home():
        return "Welcome to Healthy-Air - Improving the Indoor Air Quality"

    return app

app = create_app()

# if __name__ == "__main__":
#     app.run()