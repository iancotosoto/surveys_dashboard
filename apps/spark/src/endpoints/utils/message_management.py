from flask import jsonify

# Manejo de mensajes
def generate_response(status: str, message: str, data, code: int):
        return jsonify( {
                            "status": status,
                            "message": message,
                            "data": data.toPandas().to_dict(orient='records') if data is not None else None,
                            "code": code
                        }), code