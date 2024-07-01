survey_schema = {
    "$jsonSchema": {
        "bsonType": "object",
        "required": ["NumeroEncuesta", "Titulo", "IdAutor", "Autor", "FechaCreacion", "FechaActualizacion", "Disponible", "Preguntas"],
        "properties": {
            "NumeroEncuesta": {
                "bsonType": "int",
                "description": "must be an integer and is required"
            },
            "Titulo": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "IdAutor": {
                "bsonType": "int",
                "description": "must be an integer and is required"
            },
            "Autor": {
                "bsonType": "string",
                "description": "must be a string and is required"
            },
            "FechaCreacion": {
                "bsonType": "date",
                "description": "must be a datetime object and is required"
            },
            "FechaActualizacion": {
                "bsonType": "date",
                "description": "must be a datetime object and is required"
            },
            "Disponible": {
                "bsonType": "int",
                "description": "must be an integer and is required"
            },
            "Preguntas": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["Numero", "Categoria", "Pregunta"],
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
                        "Opciones": {
                            "bsonType": "array",
                            "items": {
                                "bsonType": ["string", "int"],
                                "description": "must be an array of strings or integers"
                            },
                            "description": "optional field, required for certain categories"
                        }
                    }
                },
                "description": "must be an array of questions and is required"
            }
        }
    }
}