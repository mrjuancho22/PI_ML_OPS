import pandas as pd
from fastapi import FastAPI
from sklearn.neighbors import NearestNeighbors

app = FastAPI()

df_movies = pd.read_parquet('dataset/clean_movies_dataset.parquet')
df_credits = pd.read_parquet('dataset/credits.parquet')



@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes:str):
    '''Se ingresa el mes y la funcion retorna la cantidad de peliculas que se estrenaron ese mes historicamente'''
    mes = mes.lower()
    df_movies.release_date = pd.to_datetime(df_movies.release_date)
    def mes_a_numero (mes):
        meses = {
            'enero':1,'febrero':2,'marzo':3,'abril':4,
            'mayo':5,'junio':6,'julio':7,'agosto':8,
            'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12
            }
        return meses[mes]
    cantidad = df_movies.release_date.loc[df_movies.release_date.dt.month == mes_a_numero(mes)].count().item()
    return {'mes':mes, 'cantidad':cantidad}


@app.get('/cantidad_filmaciones_dia{dia}')
def cantidad_filmaciones_dia(dia:str):
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''
    dia = dia.lower()
    df_movies.release_date = pd.to_datetime(df_movies.release_date, errors= 'coerce')
    def dia_numero(dia_numero):
        dias = {'lunes' : 0,'martes' : 1, 'miercoles': 2, 'jueves':3, 'viernes':4, 'sabado':5, 'domingo':6}
        return dias[dia_numero]
    cantidad = df_movies.release_date.loc[df_movies.release_date.dt.weekday == dia_numero(dia)].count()
    return {'dia' : dia , 'cantidad' : cantidad.item()}



@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    respuesta = df_movies[['title','release_year','popularity']].loc[df_movies.title.apply(lambda x : x.lower()) == titulo_de_la_filmacion]
    titulo = str(respuesta['title'].values[0])
    anio = int(respuesta['release_year'].values[0])
    popularidad = float(respuesta['popularity'].values[0])
    return {'titulo':titulo, 'anio':anio, 'popularidad':popularidad}



@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
    respuesta = df_movies[['title','release_year','vote_count','vote_average']].loc[df_movies.title.apply(lambda x : x.lower()) == titulo.lower()]
    titulo = str(respuesta['title'].values[0])
    anio = int(respuesta['release_year'].values[0])
    voto_total = int(respuesta['vote_count'].values[0])
    voto_promedio = float(respuesta['vote_average'].values[0])
    if respuesta['vote_count'].values[0] <2000:
        return 'La variable ingresada no cumple con la condición necesaria de tener más de 2000 valoraciones'
    else:
        return {'titulo':titulo, 'anio':anio, 'voto_total':voto_total, 'voto_promedio':voto_promedio}



@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas que en las que ha participado y el promedio de retorno'''
    resultado = df_credits[df_credits['cast'].apply(lambda x : nombre_actor.lower().rstrip() in x.lower())]
    cantidad_filmaciones = resultado.shape[0]
    lista_proyectos = resultado.id.tolist()
    proyectos = df_movies[df_movies['id'].isin(lista_proyectos)]
    retorno_total = sum(proyectos.revenue.tolist())
    retorno_promedio = round(retorno_total/cantidad_filmaciones)
    return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad_filmaciones, 'retorno_total':retorno_total, 'retorno_promedio':retorno_promedio}



@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    condicion1 = df_credits['crew'].str.contains(r'\b{}\b'.format(nombre_director.title()), regex=True)
    condicion2 = df_credits['crew'].str.contains(r'\b{}\b'.format('Director'), regex=True)
    resultado = df_credits[condicion1 & condicion2]

    lista_proyectos = resultado.id.tolist()
    proyectos = df_movies[df_movies['id'].isin(lista_proyectos)]

    revenue_pelicula = proyectos.revenue.tolist()
    retorno_pelicula = proyectos['return'].tolist()
    budget_pelicula = proyectos.budget.tolist()
    retorno_total_director = sum(revenue_pelicula)
    peliculas = proyectos.title.tolist()
    anio_peliculas = [fecha.strftime('%Y-%m-%d') for fecha in proyectos.release_date.dt.date]
    
    return {
        'director':nombre_director, 
        'retorno_total_director':retorno_total_director, 
        'peliculas':peliculas, 
        'anio':anio_peliculas, 
        'retorno_pelicula':retorno_pelicula, 
        'budget_pelicula':budget_pelicula, 
        'revenue_pelicula':revenue_pelicula}


@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    return {'lista recomendada': respuesta}