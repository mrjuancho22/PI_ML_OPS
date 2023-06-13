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
    # se hace del string mes en minusculas, en caso de que se haya ingresado de una forma erronea
    mes = mes.lower()
    # se convierte los datos de la columna release_date en tipo fecha
    df_movies.release_date = pd.to_datetime(df_movies.release_date)
    
    #se genera una función donde se ingresa un string de mes y se devuelve el numero que corresponde
    def mes_a_numero (mes:str):
        meses = {
            'enero':1,'febrero':2,'marzo':3,'abril':4,
            'mayo':5,'junio':6,'julio':7,'agosto':8,
            'septiembre':9,'octubre':10,'noviembre':11,'diciembre':12
            }
        return meses[mes]
    #aquí se aplica la función y se cuenta los items dados. se compara con el string ingresado para solo contar aquél que se solicito
    cantidad = df_movies.release_date.loc[df_movies.release_date.dt.month == mes_a_numero(mes)].count().item()
    #se muestran los resultados
    return {'mes':mes, 'cantidad':cantidad}


@app.get('/cantidad_filmaciones_dia/{dia}')
def cantidad_filmaciones_dia(dia:str):
    '''Se ingresa el dia y la funcion retorna la cantidad de peliculas que se estrebaron ese dia historicamente'''
    dia = dia.lower()  # Convertir el día ingresado a minúsculas
    df_movies.release_date = pd.to_datetime(df_movies.release_date, errors= 'coerce')  # Convertir la columna 'release_date' a formato de fecha y hora
    def dia_numero(dia_numero):
        dias = {'lunes' : 0,'martes' : 1, 'miercoles': 2, 'jueves':3, 'viernes':4, 'sabado':5, 'domingo':6}  # Diccionario que mapea los días a números
        return dias[dia_numero]
    cantidad = df_movies.release_date.loc[df_movies.release_date.dt.weekday == dia_numero(dia)].count()  # Contar la cantidad de películas cuya fecha de lanzamiento coincide con el día ingresado
    return {'dia' : dia , 'cantidad' : cantidad.item()}  # Devolver el día y la cantidad de filmaciones


@app.get('/score_titulo/{titulo}')
def score_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score'''
    titulo = titulo.lower()  # Convertir el título ingresado a minúsculas
    respuesta = df_movies[['title','release_year','popularity']].loc[df_movies.title.apply(lambda x : x.lower()) == titulo]  # Filtrar el dataframe 'df_movies' por el título ingresado
    titulo = str(respuesta['title'].values[0])  # Obtener el título de la respuesta
    anio = int(respuesta['release_year'].values[0])  # Obtener el año de estreno de la respuesta
    popularidad = float(respuesta['popularity'].values[0])  # Obtener la popularidad de la respuesta
    return {'titulo':titulo, 'anio':anio, 'popularidad':popularidad}  # Devolver el título, el año de estreno y la popularidad


@app.get('/votos_titulo/{titulo}')
def votos_titulo(titulo:str):
    '''Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. 
    La misma variable deberá de contar con al menos 2000 valoraciones, 
    caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.'''
    respuesta = df_movies[['title','release_year','vote_count','vote_average']].loc[df_movies.title.apply(lambda x : x.lower()) == titulo.lower()]  # Filtrar el dataframe 'df_movies' por el título ingresado
    titulo = str(respuesta['title'].values[0])  # Obtener el título de la respuesta
    anio = int(respuesta['release_year'].values[0])  # Obtener el año de estreno de la respuesta
    voto_total = int(respuesta['vote_count'].values[0])  # Obtener la cantidad total de votos de la respuesta
    voto_promedio = float(respuesta['vote_average'].values[0])  # Obtener el valor promedio de las votaciones de la respuesta
    if respuesta['vote_count'].values[0] <2000:  # Verificar si la cantidad de votos es menor a 2000
        return 'La variable ingresada no cumple con la condición necesaria de tener más de 2000 valoraciones'  # Devolver un mensaje de error
    else:
        return {'titulo':titulo, 'anio':anio, 'voto_total':voto_total, 'voto_promedio':voto_promedio}  # Devolver el título, el año de estreno, la cantidad de votos y el valor promedio de las votaciones


@app.get('/get_actor/{nombre_actor}')
def get_actor(nombre_actor:str):
    '''Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, la cantidad de películas en las que ha participado y el promedio de retorno'''
    resultado = df_credits[df_credits['cast'].apply(lambda x : nombre_actor.lower().rstrip() in "".join(x.tolist()).lower())]  # Filtrar el dataframe 'df_credits' por el nombre del actor ingresado
    cantidad_filmaciones = resultado.shape[0]  # Obtener la cantidad de filmaciones en las que ha participado el actor
    lista_proyectos = resultado.id.tolist()  # Obtener una lista de los IDs de los proyectos en los que ha participado el actor
    proyectos = df_movies[df_movies['id'].isin(lista_proyectos)]  # Filtrar el dataframe 'df_movies' por los IDs de los proyectos
    retorno_total = sum(proyectos.revenue.tolist())  # Calcular el retorno total sumando los ingresos (revenue) de los proyectos
    retorno_promedio = round(retorno_total/cantidad_filmaciones)  # Calcular el retorno promedio dividiendo el retorno total entre la cantidad de filmaciones
    return {'actor':nombre_actor, 'cantidad_filmaciones':cantidad_filmaciones, 'retorno_total':retorno_total, 'retorno_promedio':retorno_promedio}  # Devolver el nombre del actor, la cantidad de filmaciones, el retorno total y el retorno promedio


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
    ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
    Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.'''
    condicion = df_credits['crew'].apply(lambda x : {'name':nombre_director.title(),'job' : 'Director'} in x)  # Verificar si el nombre del director y su trabajo ('Director') están presentes en la lista de miembros del equipo de cada película
    resultado = df_credits[condicion]  # Filtrar el dataframe 'df_credits' por la condición
    
    lista_proyectos = resultado.id.tolist()  # Obtener una lista de los IDs de los proyectos dirigidos por el director
    proyectos = df_movies[df_movies['id'].isin(lista_proyectos)]  # Filtrar el dataframe 'df_movies' por los IDs de los proyectos
    
    revenue_pelicula = proyectos.revenue.tolist()  # Obtener una lista de los ingresos (revenue) de las películas
    retorno_pelicula = proyectos['return'].tolist()  # Obtener una lista de los retornos individuales de las películas
    budget_pelicula = proyectos.budget.tolist()  # Obtener una lista de los presupuestos (budget) de las películas
    retorno_total_director = sum(revenue_pelicula)  # Calcular el retorno total del director sumando los ingresos (revenue) de las películas
    peliculas = proyectos.title.tolist()  # Obtener una lista de los títulos de las películas
    anio_peliculas = [fecha.strftime('%Y-%m-%d') for fecha in proyectos.release_date.dt.date]  # Obtener una lista de las fechas de lanzamiento de las películas
    
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
    #se hace de la primera letra de lo ingresado mayuscula si es que ya no lo está. Esto por que todos los datos del df están con la letra inicial mayuscula, de esta forma, la busqueda se dara 
    #bien
    titulo = titulo.capitalize()
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