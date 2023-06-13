import pandas as pd
import ast
import pyarrow as pa
import pyarrow.parquet as pq

#se lee el documento csv de credits
df_credits = pd.read_csv('datasets/credits.csv')

# se evalua el valor de cast, y se toma literalment como es: una lista de diccionarios
df_credits.cast =  df_credits.cast.apply(lambda x : ast.literal_eval(x) )
#se crea la función iterador_cast, que extrae el campo "nombre" de los diccionarios de la lista y los almacena en una lista aparte, retorna la lista
# con los nombres
def iterador_cast(x):
    lista = []
    for i in x:
        lista.append(i['name'])
    return lista
#se aplica la función en la columna cast
df_credits.cast =  df_credits.cast.apply(lambda x : iterador_cast(x) )

# se evalua el valor de crew, y se toma literalmente como es: una lista de diccionarios
df_credits.crew =  df_credits.crew.apply(lambda x : ast.literal_eval(x) )
#se crea la función iterador_crew, que extrae los campos "nombre" y "job" de los diccionarios de la lista y los almacena en una lista aparte, retorna la lista
# con los nombres y jobs
def iterador_crew(x):
    lista = []
    for i in x:
        lista.append({'name': i['name'],
                      'job' : i['job']})
    return lista
#se aplica la función en la columna crew
df_credits.crew =  df_credits.crew.apply(lambda x : iterador_crew(x) )

#se guarda el archivo como un archivo parquet en la carpeta datasets
table = pa.Table.from_pandas(df_credits)
pq.write_table(table, 'datasets/credits.parquet')