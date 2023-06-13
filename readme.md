# Proyecto de Data Science - API de Películas

Este proyecto de Data Science se enfoca en el análisis de datos relacionados con películas y proporciona una API para acceder a diferentes funcionalidades y consultas sobre películas. La API está desarrollada utilizando Uvicorn y FastAPI, y ofrece diversas funciones para obtener información sobre películas, votaciones, actores y directores.

En este proyecto encontrarás:

- Carpeta .venv:

    En esta carpeta se encuentran los archivos necesarios para que "corra" el proyecto, desde librerías, scripts etc. En el archivo requirements.txt, encontraras qué librerías se usaron para el proyecto en conjunto a sus versiones.

- Carpeta datasets:

    En esta se hayan las fuentes de información que se usaron para la API, se encuentran 2 archivos parquet que son archivos limpios después del ETL del proyecto y 1 archivo csv, éste último siendo los datos de tipo RAW que se suministraron al comienzo del proyecto.
    Si se necesita el archivo credits original, puedes ingresar a este [link](https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu)


- Carpeta documentacion:

    En esta se hayan las consignas para realizar este proyecto. Aqui encontraras el Readme original con las metricas para realizar el proyecto, un archivo md con material de apoyo, y un diccionario de los valores de las columnas de movies_dataset.csv


- Carpeta src:

    Se almacenan algunas imagenes para el Readme original


- Documento eda:

    Documento hecho en jupyter notebook del analisis exploratorio hecho para el sistema de recomendaciones


- Documentos etl:

    Documentos hecho en python con el procedimiento de limpieza que se realizo al documento movies_dataset.csv y credits.csv, cada archivo tiene el nombre del documento al cual le hizo limpieza. EL documento de movies, realiza los procedimientos descritos en el readme original con las metricas del proyecto; mientras que el de credits, lo hice a por labor propia para resumir la información de este, los cambios realizados son:
    - la columna cast, ahora solo contiene una lista por fila de los nombre de los actores participes en los proyectos
    - la columna crew, ahora solo contiene el nombre y trabajo del staff relacionado a la pelicula
    - el id del proyecto no sufrió cambios

- Documento main:

    Documento hecho en python que contiene todo lo relacionado a la API, aquí se puede encontrar todas las funciones de la API, 

- Documento requeriments:

    Documento hecho en txt que contiene los requerimientos para que render pueda correr la API


# Funciones de la API

## Función cantidad_filmaciones_mes(mes:str)

Descripción: Esta función recibe como parámetro el nombre de un mes y devuelve la cantidad de películas que se estrenaron históricamente en ese mes.

Parámetros:

    mes (str): El nombre del mes en formato de texto.

Retorno:

    mes (str): El nombre del mes ingresado.
    cantidad (int): La cantidad de películas estrenadas en ese mes.

## Función cantidad_filmaciones_dia(dia:str)

Descripción: Esta función recibe como parámetro el nombre de un día y devuelve la cantidad de películas que se estrenaron históricamente en ese día.

Parámetros:

    dia (str): El nombre del día en formato de texto.

Retorno:

    dia (str): El nombre del día ingresado.
    cantidad (int): La cantidad de películas estrenadas en ese día.

## Función score_titulo(titulo:str)

Descripción: Esta función recibe como parámetro el título de una filmación y devuelve el título, el año de estreno y el puntaje de popularidad de la película.

Parámetros:

    titulo (str): El título de la filmación.

Retorno:

    titulo (str): El título de la película.
    anio (int): El año de estreno de la película.
    popularidad (float): El puntaje de popularidad de la película.

## Función votos_titulo(titulo:str)

Descripción: Esta función recibe como parámetro el título de una filmación y devuelve el título, la cantidad de votos y el promedio de votos de la película. Si la película tiene menos de 2000 votos, se devuelve un mensaje indicando que no cumple con la condición.

Parámetros:

    titulo (str): El título de la filmación.

Retorno:

    Si la película tiene más de 2000 votos:
        titulo (str): El título de la película.
        anio (int): El año de estreno de la película.
        voto_total (int): La cantidad total de votos recibidos por la película.
        voto_promedio (float): El promedio de votos de la película.
    Si la película tiene menos de 2000 votos:
        Mensaje indicando que la película no cumple con la condición de tener más de 2000 votos.

## Función get_actor(nombre_actor:str)

Descripción: Esta función recibe como parámetro el nombre de un actor y devuelve información sobre el éxito del actor en base a la cantidad de películas en las que ha participado y el retorno total y promedio de esas películas.

Parámetros:

    nombre_actor (str): El nombre del actor.

Retorno:

    actor (str): El nombre del actor.
    cantidad_filmaciones (int): L

## Función recomendacion(titulo:str)

Descripción: Esta función recibe como parámetro el título de una filmación una lista de titulos de recomendacion, a través de un modelo de aprendizaje de vecinos cercanos, donde se muestran aquellos 5 valores que cumplan con mayor cantidad de similaridades al titulo ingresado

Parámetros:

    titulo (str): El nombre del titulo.

Retorno:

    Recomendaciones: Lista de con 5 recomendaciones.


# Video

Con este [link](www.youtube.com) podrás ver un video donde se muestra el funcionamiento de la API


# API

Puedes ingresar a la API en este [link](https://proyecto-individual-1-upjh.onrender.com), esta está en Render. solo para que sepan jajaja


