answer_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["NumeroEncuesta", "IdEncuestado", "Nombre", "Correo", "FechaRealizado", "Preguntas"],
        "properties": {
            "NumeroEncuesta": {
                "bsonType": "int",
                "description": "must be an integer and is required"
            },
            "IdEncuestado": {
                "bsonType": "int",
                "description": "must be an integer and is required"
            },
            "Nombre": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "Correo": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "FechaRealizado": {
                "bsonType": "date",
                "description": "must be a datetime object and is required"
            },
            "Preguntas": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["Numero", "Categoria", "Pregunta", "Respuesta"],
                    "properties": {
                        "Numero": {
                            "bsonType": "int",
                            "description": "must be an integer and is required"
                        },
                        "Categoria": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "Pregunta": {
                            "bsonType": "string",
                            "description": "must be a string and is required"
                        },
                        "Respuesta": {
                            "bsonType": ["string", "array", "int"],
                            "description": "must be a string, an array, or an integer, depending on the question type"
                        }
                    }
                },
                "description": "must be an array of answers and is required"
            }
        }
    }
}