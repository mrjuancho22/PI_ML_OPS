
#Para este etl, se usará la librería pandas con el apodo de pd
import pandas as pd

# Creando un dataframe con la informacion del archivo movies_dataset.csv
df = pd.read_csv('datasets/movies_dataset.csv',sep=',',low_memory=False)

# Rellenando con 0 los valores nulos de las columnas revenue, budget
valores_a_rellenar = {'revenue':0,'budget':0}
df.fillna(value= valores_a_rellenar, inplace=True)

# Eliminando los valores nulos de la columna release date
df.dropna ( axis = 0, subset = 'release_date', inplace=True)

# Vuelviendo la columna release_date al formato fecha AAAA-mm-dd
df['release_date'] = pd.to_datetime(df.release_date, format='%Y-%m-%d')

# Creando la columna release_year, llenando con 0 aquellos campos donde no hay fecha registrada y lo vuelvo en un dato tipo int en caso de utilizar
# esta columna en una alguna operación matematica posterior
df['release_year'] = df.release_date.dt.year.fillna(0).astype(int)

# Creando la columna return dada por la operación revenue/budget
df['return'] = df.revenue/ df.budget.astype(float)

# En caso de haber datos nulos, se reemplazan con cero
df['return'].fillna(0,inplace=True)

# En caso de encontrarse datos infinitos o no definidos (dado por dividir por cero), se reemplazan con cero
df['return'].replace([float('inf'), float('-inf')],0,inplace=True)

# Eliminando las columnas
#'video','imdb_id','adult','original_title','vote_count','poster_path','homepage'
df.drop(['video','imdb_id','adult','original_title','vote_count','poster_path','homepage'],axis=1,inplace=True)

# Se guarda el dataframe con el nombre de clean_movies_dataset
df.to_csv('datasets/clean_movies_dataset.csv')
