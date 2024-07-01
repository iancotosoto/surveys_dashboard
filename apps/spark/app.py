import threading
from flask import Flask

import src.endpoints.services.spark_service as spark_service

from src.endpoints.routes.surveys import surveys_routes
from src.endpoints.routes.answers import answers_routes

# Create the Flask app
app = Flask(__name__, static_url_path='/static')

# Register the blueprints
app.register_blueprint(surveys_routes)
app.register_blueprint(answers_routes)

# Inicializar SparkSession
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)