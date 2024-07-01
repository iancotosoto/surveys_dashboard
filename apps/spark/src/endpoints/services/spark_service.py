from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import pyspark.sql.types as t
from pymongo import MongoClient
import threading
import time
import os

from src.endpoints.utils.message_management import generate_response
import src.endpoints.utils.convertion as c

class SparkService:

    def __init__(self):
        # Variables de entorno
        database = os.getenv("DB_NAME")
        collection_surveys = os.getenv("COLLECTION_SURVEYS")
        collection_answers = os.getenv("COLLECTION_ANSWERS")
        mongo_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        mongo_uri = f"mongodb://{mongo_username}:{mongo_password}@mongodb:27017/"

        # Conexión a MongoDB
        self.client = MongoClient(mongo_uri)
        self.db = self.client[database]
        self.encuestas = self.db[collection_surveys]
        self.respuestas = self.db[collection_answers]

        # Inicializar SparkSession
        self.spark = SparkSession.builder.appName("PySparkMongo").getOrCreate()

        # Definir esquemas
        self.encuestas_schema = t.StructType([ 
            t.StructField("Autor", t.StringType(), True), 
            t.StructField("Disponible", t.IntegerType(),True), 
            t.StructField("FechaActualizacion", t.TimestampType(), True), 
            t.StructField("FechaCreacion", t.TimestampType(), True), 
            t.StructField("IdAutor", t.IntegerType(), True),
            t.StructField("NumeroEncuesta", t.IntegerType(), True),
            t.StructField("Titulo", t.StringType(), True),
            t.StructField("Preguntas", t.ArrayType(t.StructType([
                t.StructField("Categoria", t.StringType(), True),
                t.StructField("Numero", t.IntegerType(), True),
                t.StructField("Pregunta", t.StringType(), True),
                t.StructField("Opciones", t.ArrayType(t.StringType()), True)
            ])), True)
        ])

        self.respuestas_schema = t.StructType([ 
            t.StructField("Correo", t.StringType(), True), 
            t.StructField("FechaRealizado", t.TimestampType(), True), 
            t.StructField("IdEncuestado", t.IntegerType(), True),
            t.StructField("NumeroEncuesta", t.IntegerType(), True),
            t.StructField("Nombre", t.StringType(), True),
            t.StructField("Preguntas", t.ArrayType(t.StructType([
                t.StructField("Categoria", t.StringType(), True),
                t.StructField("Numero", t.IntegerType(), True),
                t.StructField("Pregunta", t.StringType(), True),
                t.StructField("Respuesta", t.StringType(), True)
            ])), True)
        ])

        # Variables globales para la data de MongoDB
        self.encuestas_data = None
        self.respuestas_data = None

        # Variables globales para los DataFrames
        self.encuestas_df = None
        self.respuestas_df = None

        # Iniciar el hilo para obtener los datos de MongoDB
        self.fetch_data_thread = threading.Thread(target=self.fetch_data)
        self.fetch_data_thread.start()

    # Métodos
    # Obtener datos de MongoDB
    def fetch_data(self):
        while True:
            # Obtener datos de MongoDB
            self.encuestas_data = list(self.encuestas.find({}, {"_id": 0}))
            self.respuestas_data = list(self.respuestas.find({}, {"_id": 0}))

            # Crear DataFrame de PySpark
            self.encuestas_df = self.spark.createDataFrame(data=self.encuestas_data, schema=self.encuestas_schema)
            self.respuestas_df = self.spark.createDataFrame(data=self.respuestas_data, schema=self.respuestas_schema)
            self.respuestas_intactas_df = self.respuestas_df

            # Convertir respuestas
            self.convertir_respuestas()

            # Esperar 10 segundos antes de la próxima ejecución
            time.sleep(10)

    # Convertir respuestas
    def convertir_respuestas(self):
        # Extender las respuestas por pregunta
        self.respuestas_df = self.respuestas_df.select(
            "NumeroEncuesta", 
            "FechaRealizado",
            f.explode("Preguntas").alias("P")
        )

        # Crear columnas para cada tipo de respuesta
        self.respuestas_df = self.respuestas_df.withColumn(
            "RespuestaArray", 
            f.when(f.col("P.Categoria") == "EleccionMultiples", f.split(f.regexp_replace(f.col("P.Respuesta"), "[\\[\\]]", ""), ",\\s*"))
        ).withColumn(
            "RespuestaNumerica", 
            f.when((f.col("P.Categoria") == "EscalaCalificacion") | (f.col("P.Categoria") == "Numericas"), f.col("P.Respuesta").cast(t.IntegerType()))
        ).withColumn(
            "RespuestaBoleana", 
            f.when(f.col("P.Categoria") == "SiNo", f.col("P.Respuesta").cast(t.BooleanType()))
        ).withColumn(
            "RespuestaString", 
            f.when((f.col("P.Categoria") == "Abiertas") | (f.col("P.Categoria") == "EleccionSimples"), f.col("P.Respuesta").cast(t.StringType()))
        )

        # Seleccionar columnas y renombrarlas
        self.respuestas_df = self.respuestas_df.select(
            "NumeroEncuesta", "FechaRealizado", "P.Numero", "P.Pregunta", "P.Categoria",
            "RespuestaArray","RespuestaNumerica", "RespuestaBoleana","RespuestaString")\
            .withColumnRenamed("Numero", "NumeroPregunta")\
            .withColumnRenamed("Pregunta", "Pregunta")\
            .withColumnRenamed("Categoria", "CategoriaPregunta")

    # Funciones de Spark
    # Encuestas
    def get_encuestas_cant_autores(self):
        try:
            # Cantidad de encuestas realizadas por autor
            cantidad_por_user_df = self.encuestas_df.groupBy("Autor", "IdAutor").count()\
                                            .withColumnRenamed("count", "CantidadEncuestas")
            
            return generate_response("success", "Surveys retrieved successfully.", cantidad_por_user_df, 200)
        except Exception as e:
            return generate_response("error", str(e), None, 500)

    def get_encuestas_cant_disponibles(self):
        try:
            # Cantidad de disponibles y no disponibles
            cantidad_disponibles_df = self.encuestas_df.groupBy("Disponible").count()\
                                                .withColumnRenamed("count", "CantidadEncuestas")
            
            return generate_response("success", "Surveys retrieved successfully.", cantidad_disponibles_df, 200)
        except Exception as e:
            return generate_response("error", str(e), None, 500)
    
    def get_encuestas_cant_categorias(self):
        try:
            # Cantidades de preguntas por categoría
            cantidad_por_categoria_df = self.encuestas_df.select("Preguntas", f.explode("Preguntas").alias("P"))\
                                                    .select("P.Categoria").groupBy("Categoria").count()\
                                                    .withColumnRenamed("count", "CantidadPreguntas")
            
            return generate_response("success", "Surveys retrieved successfully.", cantidad_por_categoria_df, 200)
        except Exception as e:
            return generate_response("error", str(e), None, 500)
        
    def get_encuestas_cant_preguntas(self):
        try:      
            # Cantidades de preguntas por encuesta
            cantidad_preguntas_por_encuesta_df = self.encuestas_df.select("NumeroEncuesta", 
                                                                          f.size("Preguntas").alias("CantidadPreguntas"))

            return generate_response("success", "Surveys retrieved successfully.", cantidad_preguntas_por_encuesta_df, 200)
        except Exception as e:
            return generate_response("error", str(e), None, 500)

    def get_encuestas_cant_respuestas(self):
        try:      
            # Cantidad de respuestas por encuesta
            cantidad_respuestas_por_encuesta_df = self.respuestas_intactas_df.groupBy("NumeroEncuesta").count()\
                                                            .withColumnRenamed("count", "CantidadRespuestas")
            
            return generate_response("success", "Surveys retrieved successfully.", cantidad_respuestas_por_encuesta_df, 200)
        except Exception as e:
            return generate_response("error", str(e), None, 500)

    # Respuestas
    def get_respuestas_df(self):
        try:
            # Obtener cantidad de veces que se ha repetido la respuesta de cada pregunta
            # Seleccionar las respuestas de tipo array
            respuestas_multiples_df = self.respuestas_df.filter(f.col("RespuestaArray").isNotNull())\
                                                        .withColumn("RespuestaArray", f.explode("RespuestaArray"))

            respuestas_multiples_df = respuestas_multiples_df.groupBy("NumeroEncuesta", "NumeroPregunta", 
                                                                "Pregunta", "CategoriaPregunta", "RespuestaArray")\
                                                        .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                        .withColumnRenamed("RespuestaArray", "Respuesta")

            # Seleccionar las respuestas de tipo numérico
            respuestas_numerica_df = self.respuestas_df.filter(f.col("RespuestaNumerica").isNotNull())

            respuestas_numerica_df = respuestas_numerica_df.groupBy("NumeroEncuesta", "NumeroPregunta", 
                                                              "Pregunta", "CategoriaPregunta", "RespuestaNumerica")\
                                                        .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                        .withColumnRenamed("RespuestaNumerica", "Respuesta")
            
            respuestas_numerica_df = respuestas_numerica_df.withColumn("Respuesta", 
                                                                       f.col("Respuesta").cast(t.StringType()))
            
            # Seleccionar las respuestas de tipo booleano
            respuestas_booleana_df = self.respuestas_df.filter(f.col("RespuestaBoleana").isNotNull())

            respuestas_booleana_df = respuestas_booleana_df.groupBy("NumeroEncuesta", "NumeroPregunta", 
                                                              "Pregunta", "CategoriaPregunta", "RespuestaBoleana")\
                                                        .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                        .withColumnRenamed("RespuestaBoleana", "Respuesta")\
                                                        .select("NumeroEncuesta", "NumeroPregunta", "Pregunta", 
                                                                "CategoriaPregunta", "Respuesta", "CantidadRespuestas")
            
            respuestas_booleana_df = respuestas_booleana_df.withColumn("Respuesta", 
                                                                       f.col("Respuesta").cast(t.StringType()))
            
            # Seleccionar las respuestas de tipo texto
            respuestas_texto_df = self.respuestas_df.filter(f.col("RespuestaString").isNotNull())

            respuestas_texto_df = respuestas_texto_df.groupBy("NumeroEncuesta", "NumeroPregunta",
                                                              "Pregunta", "CategoriaPregunta", "RespuestaString")\
                                                          .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                          .withColumnRenamed("RespuestaString", "Respuesta")\
                                                        .select("NumeroEncuesta", "NumeroPregunta", "Pregunta", 
                                                                "CategoriaPregunta", "Respuesta", "CantidadRespuestas")
            
            # Unir los DataFrames
            respuestas_totales_df = respuestas_multiples_df.union(respuestas_numerica_df)\
                                                        .union(respuestas_booleana_df)\
                                                        .union(respuestas_texto_df)
            
            # Ordenar por número de encuesta y número de pregunta
            respuestas_totales_df = respuestas_totales_df.orderBy("NumeroEncuesta", "NumeroPregunta")


            
            return generate_response("success", "Answers retrieved successfully.", respuestas_totales_df, 200)
        except Exception as e:
            return generate_response("error", str(e), None, 500)
        
    def get_respuestas_esp_df(self, encuesta_id):
        try:
            # Obtener las respuestas de una encuesta específica
            respuestas_esp_df = self.respuestas_df.filter(f.col("NumeroEncuesta") == encuesta_id)

            # Obtener cantidad de veces que se ha repetido la respuesta de cada pregunta
            # Seleccionar las respuestas de tipo array
            respuestas_multiples_df = respuestas_esp_df.filter(f.col("RespuestaArray").isNotNull())\
                                                        .withColumn("RespuestaArray", f.explode("RespuestaArray"))

            respuestas_multiples_df = respuestas_multiples_df.groupBy("NumeroEncuesta", "NumeroPregunta", 
                                                                "Pregunta", "CategoriaPregunta", "RespuestaArray")\
                                                        .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                        .withColumnRenamed("RespuestaArray", "Respuesta")

            # Seleccionar las respuestas de tipo numérico
            respuestas_numerica_df = respuestas_esp_df.filter(f.col("RespuestaNumerica").isNotNull())

            respuestas_numerica_df = respuestas_numerica_df.groupBy("NumeroEncuesta", "NumeroPregunta", 
                                                              "Pregunta", "CategoriaPregunta", "RespuestaNumerica")\
                                                        .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                        .withColumnRenamed("RespuestaNumerica", "Respuesta")
            
            respuestas_numerica_df = respuestas_numerica_df.withColumn("Respuesta", 
                                                                       f.col("Respuesta").cast(t.StringType()))
            
            # Seleccionar las respuestas de tipo booleano
            respuestas_booleana_df = respuestas_esp_df.filter(f.col("RespuestaBoleana").isNotNull())

            respuestas_booleana_df = respuestas_booleana_df.groupBy("NumeroEncuesta", "NumeroPregunta", 
                                                              "Pregunta", "CategoriaPregunta", "RespuestaBoleana")\
                                                        .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                        .withColumnRenamed("RespuestaBoleana", "Respuesta")\
                                                        .select("NumeroEncuesta", "NumeroPregunta", "Pregunta", 
                                                                "CategoriaPregunta", "Respuesta", "CantidadRespuestas")
            
            respuestas_booleana_df = respuestas_booleana_df.withColumn("Respuesta", 
                                                                       f.col("Respuesta").cast(t.StringType()))
            
            # Seleccionar las respuestas de tipo texto
            respuestas_texto_df = respuestas_esp_df.filter(f.col("RespuestaString").isNotNull())

            respuestas_texto_df = respuestas_texto_df.groupBy("NumeroEncuesta", "NumeroPregunta",
                                                              "Pregunta", "CategoriaPregunta", "RespuestaString")\
                                                          .count().withColumnRenamed("count", "CantidadRespuestas")\
                                                          .withColumnRenamed("RespuestaString", "Respuesta")\
                                                        .select("NumeroEncuesta", "NumeroPregunta", "Pregunta", 
                                                                "CategoriaPregunta", "Respuesta", "CantidadRespuestas")
            
            # Unir los DataFrames
            respuestas_totales_df = respuestas_multiples_df.union(respuestas_numerica_df)\
                                                        .union(respuestas_booleana_df)\
                                                        .union(respuestas_texto_df)
            
            # Ordenar por número de encuesta y número de pregunta
            respuestas_totales_df = respuestas_totales_df.orderBy("NumeroEncuesta", "NumeroPregunta")
            
            return generate_response("success", "Answers retrieved successfully.", respuestas_totales_df, 200)
        except Exception as e:
            return generate_response("error", str(e), None, 500)