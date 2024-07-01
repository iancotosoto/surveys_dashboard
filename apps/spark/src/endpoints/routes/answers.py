from flask import Blueprint

from src.endpoints.services.spark_instance import spark_service as sp

# Blueprint
answers_routes = Blueprint('answers_routes', __name__)

# Endpoints
@answers_routes.route('/respuestas', methods=['GET'])
def get_respuestas():
    result = sp.get_respuestas_df()
    return result

@answers_routes.route('/respuestas/<int:encuesta_id>', methods=['GET'])
def get_respuestas_esp(encuesta_id):
    result = sp.get_respuestas_esp_df(encuesta_id)
    return result