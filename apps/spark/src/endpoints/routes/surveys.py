from flask import Blueprint

from src.endpoints.services.spark_instance import spark_service as sp

# Blueprint
surveys_routes = Blueprint('surveys_routes', __name__)

# Endpoints
@surveys_routes.route('/encuestas/cantidad/autores', methods=['GET'])
def get_encuestas_cant_autores():
    result = sp.get_encuestas_cant_autores()
    return result

@surveys_routes.route('/encuestas/cantidad/disponibles', methods=['GET'])
def get_encuestas_cant_disponibles():
    result = sp.get_encuestas_cant_disponibles()
    return result

@surveys_routes.route('/encuestas/cantidad/categorias', methods=['GET'])
def get_encuestas_cant_categorias():
    result = sp.get_encuestas_cant_categorias()
    return result

@surveys_routes.route('/encuestas/cantidad/preguntas', methods=['GET'])
def get_encuestas_cant_preguntas():
    result = sp.get_encuestas_cant_preguntas()
    return result

@surveys_routes.route('/encuestas/cantidad/respuestas', methods=['GET'])
def get_encuestas_cant_respuestas():
    result = sp.get_encuestas_cant_respuestas()
    return result