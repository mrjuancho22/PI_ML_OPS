import ast
import pandas as pd
from fastapi import FastAPI
from sklearn.neighbors import NearestNeighbors

app = FastAPI()

df = pd.read_csv('Clean_dataset/movies_dataset.csv',index_col=0)



@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str):
    return None



@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia : str):
    return None



@app.get("/score_titulo/{titulo_de_la_filmacion}")
def score_titulo(titulo_de_la_filmacion: str):
    return None



@app.get("/votos_titulo/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion: str):
    return None



@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    return None



@app.get("/get_director/{nombre_director}")
def get_director(nombre_director : str):
    return None