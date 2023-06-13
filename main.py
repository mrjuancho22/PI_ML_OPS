import pandas as pd
import ast
from fastapi import FastAPI
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

app = FastAPI()

df_movies = pd.read_parquet('datasets/clean_movies_dataset.parquet')
df_credits = pd.read_parquet('datasets/credits.parquet')

@app.get('/')
def home():
    return {'message': 
    r"""¡Bienvenido a la API del proyecto!, estas son las posibles configuraciones:  
    /cantidad_filmaciones_mes/{mes}  
    /cantidad_filmaciones_dia/{dia} 
    /score_titulo/{titulo} 
    /votos_titulo/{titulo} 
    /get_actor/{nombre_actor} 
    /get_director/{nombre_director} 
    /recomendacion/{titulo} """}


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


@app.get('/cantidad_filmaciones_dia/{dia}')
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
    titulo = titulo.lower()
    respuesta = df_movies[['title','release_year','popularity']].loc[df_movies.title.apply(lambda x : x.lower()) == titulo]
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
    
    resultado = df_credits[df_credits['cast'].apply(lambda x : nombre_actor.lower().rstrip() in "".join(x.tolist()).lower())]
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
    condicion = df_credits['crew'].apply(lambda x : {'name':nombre_director.title(),'job' : 'Director'} in x)
    resultado = df_credits[condicion]

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

    #se crea un clon del df original con las columnas genres, title, vote_average, popularity, para que la funcion recomendacion no consuma demasiados recursos
    df_b = df_movies.loc[:, ['belongs_to_collection','genres','title','vote_average','popularity']].copy()

    #la columna genres, tiene valores muy complejos, cada fila tiene una lista de diccionarios, con el codigo de abajo, los generos quedan un string sencillo
    df_b.genres = df_b.genres.apply(lambda x : ast.literal_eval(x))
    def normalizar_generos(x):
        #esta funcion, saca los generos de los diccioanrios, volviendolos un string con todos los generos de la pelicula
        lista =""
        for i in x:
            lista += (i['name'])
            if i == x[-1]:
                break
            lista += ","
        return lista
    #se aplica el codigo de arriba
    df_b.genres = df_b.genres.apply(lambda x : normalizar_generos(x)) 

    #al igual que la columna genres, la columna belongs_to_collection tiene datos complejos, con el codigo de abajo se normaliza
    df_b.belongs_to_collection = df_b.belongs_to_collection.apply(lambda x : ast.literal_eval(x) if type(x) == str else x)
    df_b.belongs_to_collection = df_b.belongs_to_collection.apply(lambda x : x['name'] if type(x) == dict else x)

    #se crea columnas de valores unicos con cada uno de los valores disponibles de la columna genres
    generos_df = df_b.genres.str.get_dummies(sep=',')

    #Se crea una columna donde se almacena si los titulos del df son similares al ingresado, con 1 ( si contiene el titulo en su nombre) y con 0 ( si no contiene el titulo en su nombre)
    df_b['titulo_similar']= df_b.title.apply(lambda x: 1 if titulo in x else 0)

    #Se crea una columna donde se almacena si los titulos del df pertenecen a la misma coleccion que el ingresado,
    # con 1 ( si contiene el titulo en su nombre) y con 0 ( si no contiene el titulo en su nombre)
    
    if df_b.belongs_to_collection.loc[df_b.title == titulo].item() == None:
        coleccion = 'no pertenece a ninguna coleccion'
    else:
        coleccion = df_b.belongs_to_collection.loc[df_b.title == titulo].item()
    df_b['pertenece_colecion'] = df_b.belongs_to_collection.apply(lambda x: 1 if  coleccion== x else 0)

    #se crea el objeto knn, que será el modelo de recomendación a través de vecinos cercanos
    knn = NearestNeighbors(n_neighbors=6, algorithm='auto')

    #se normalizan las columnas popularity y vote_average
    escalar = StandardScaler()
    df_b[['popularity', 'vote_average']] = escalar.fit_transform(df_b[['popularity', 'vote_average']])

    #se definen los parametros con los que se van a entrenar al modelo, concatenando varias columnas anteriomente descritas
    parametros_entrenamiento = pd.concat([generos_df,df_b['pertenece_colecion'],df_b['titulo_similar'],df_b['vote_average'],df_b['popularity']],axis=1)

    #se entrena el modelo
    knn.fit(parametros_entrenamiento)

    # se sustraen los indices de los titulos mas cercanos al titulo ingresado
    indices = knn.kneighbors(parametros_entrenamiento.loc[df_b['title'] == titulo])[1].flatten()
    
    #se hace una lista de los titulos recomendados por medio de sus indices
    recomendaciones = list(df_b.iloc[indices]['title'])

    # se organizan las recomendaciones por el valor del promedio de los votos
    recomendaciones = sorted( recomendaciones, key= lambda x:(df_b.loc[df_b.title ==x]['titulo_similar'].values[0],df_b.loc[df_b['title'] == x]['vote_average'].values[0] ),reverse=True )

    # se retira de las recomendaciones el mismo titulo ingresado en la funcion
    recomendaciones = [pelicula for pelicula in recomendaciones if pelicula != titulo]

    #se retorna la lista de recomendaciones
    return {'lista recomendada': recomendaciones[:5]}