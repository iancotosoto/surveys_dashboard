from pyspark.sql import functions as F
from pyspark.sql.types import IntegerType, BooleanType, StringType, ArrayType

# Define la función de conversión
def convertir_respuesta(categoria, respuesta):
    if categoria == "EleccionMultiples":
        respuesta = respuesta[1:-1]
        return respuesta.split(", ")
    elif categoria == "EscalaCalificacion" or categoria == "Numericas":
        return int(respuesta)
    elif categoria == "SiNo":
        return bool(int(respuesta))
    elif categoria == "Abiertas" or categoria == "EleccionSimples":
        return respuesta
    else:
        return respuesta

# Registrar la UDF
convertir_respuesta_udf = F.udf(convertir_respuesta)