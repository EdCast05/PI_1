from fastapi import FastAPI
import pandas as pd 
import pyarrow.parquet as pq
import joblib

app = FastAPI()

@app.get('/') #Endpoint
def home():
    return {"Message": "Bienvenido a mi API de recomendación de videojuegos de la plataforma Steam"}

@app.get("/developer")
def developer(desarrollador: str):
    # Leo la data
    df = pd.read_parquet('data/df_endpoint1.parquet')

    # Valido si el valor ingresado existe
    if desarrollador not in df['developer'].tolist():
        return {"Respuesta": f"No se encontraron resultados para {desarrollador}, verifique el valor ingresado."}

    # Filtro para el total de juegos y juegos_free
    cantidad = df[df['developer'] == desarrollador].groupby('anio').count()
    cantidad_free = df[(df['developer'] == desarrollador) & (df['price'] == 0.0)].groupby('anio').count()

    # Convierto a lista
    cantidad_juegos = cantidad['developer'].tolist()
    cantidad_juegos_free = cantidad_free['developer'].tolist()

    anio = cantidad.index.tolist()
    anio_free = cantidad_free.index.tolist()

    # Creo el diccionario con la información requerida
    porc_cont_free = {}
    for i in range(len(anio)):
        if anio[i] not in anio_free:
            porc_cont_free[anio[i]] = {'Cantidad de Items': cantidad_juegos[i], 'Contenido Free': "0%"}
        else:
            for j in range(len(anio_free)):
                if anio_free[j]==anio[i]:
                    porc_cont_free[anio[i]] = {'Cantidad de Items': cantidad_juegos[i], 'Contenido Free': f'{round(cantidad_juegos_free[j]/cantidad_juegos[i]*100,2)}%'}
    
    return {f'Respuesta para {desarrollador}': porc_cont_free}


@app.get("/userdata")
def userdata(user_id: str):
    # Cargar la base de datos
    df = pd.read_parquet('data/df_endpoint3.parquet')

    # Verifico si el usuario existe
    if user_id not in df['user_id'].tolist():
        return {"Respuesta": f"No se encontraron resultados para {user_id}, verifique el valor ingresado."}

    # Filtro por userd_id 
    cantidad = df[(df['user_id'] == user_id)].groupby('recommend').count()
    dinero = df[(df['user_id'] == user_id)].groupby('price').count()

    # Guardo el dinero gastado
    spent = dinero.index.tolist()
    spent = [float(value) for value in spent]

    recommend = cantidad.index.tolist()

    # Guardo la cantidad de juegos que posee el usuario
    cantidad_items_recom = cantidad['item_id'].tolist()

    if len(recommend) == 1:
        if recommend[0] == 'true':
            dicc = {"Usuario": user_id, "Dinero gastado": f'${round(sum(spent),2)}', "% de recomendación": f'100%', "cantidad de items": sum(cantidad_items_recom)}
        else:
            dicc = {"Usuario": user_id, "Dinero gastado": f'${round(sum(spent),2)}', "% de recomendación": f'0%', "cantidad de items": sum(cantidad_items_recom)} 
    else:
        dicc = {"Usuario": user_id, "Dinero gastado": f'${round(sum(spent),2)}', "% de recomendación": f'{round(cantidad_items_recom[1]/sum(cantidad_items_recom)*100,2)}%', "cantidad de items": sum(cantidad_items_recom)}

    return dicc


@app.get("/UserForGenre")
def UserForGenre(genero: str):
    # Leo la data
    df = pd.read_parquet('data/df_endpoint4.parquet')

    if genero not in df['genres'].values:
        return {"Respuesta": f"No se encontraron resultados para {genero}, verifique el valor ingresado."}

    # Filtro para el género
    genre_df = df[df['genres'] == genero]

    del df

    # Hallo usuario con más horas de juego
    usuario = genre_df.groupby('user_id')['playtime_forever'].sum().idxmax()

    # Agrupo por usuario y sumo las horas de juego
    poranio = genre_df[genre_df['user_id'] == usuario].groupby('anio')['playtime_forever'].sum()

    del genre_df
    poranio_dict = poranio.to_dict()

    dicc = {
        "usuario": usuario,
        "años": poranio_dict
    }

    del poranio

    return dicc


@app.get("/best_developer_year")
def best_developer_year(año: int):

    # Leo la data
    df = pd.read_parquet('data/df_endpoint5.parquet')

    # Valido si el año existe
    if año not in df['anio'].tolist():
        return {"Respuesta": f"No se encontraron resultados para {año}, verifique el valor ingresado."}

    # Filtro por año y agrupo por desarrollador
    cantidad = df[(df['anio'] == año)].groupby('developer').count()
    cantidad.reset_index(inplace=True)

    # Ordeno de mayor a menor
    cantidad = cantidad.sort_values(by='anio', ascending=False)
    cantidad = cantidad[['developer','anio']]
    
    primeros_tres = cantidad.iloc[:3]
    dicc = {}
    dicc['Primer puesto'] = primeros_tres.iloc[0]['developer']
    dicc['Segundo puesto'] = primeros_tres.iloc[1]['developer']
    dicc['Tercer puesto'] = primeros_tres.iloc[2]['developer']
   
    return dicc


@app.get("/sentiment")
def developer_reviews_analysis(desarrollador: str):

    # Leo los datos
    df = pd.read_parquet('data/df_endpoint2.parquet')

    # Valido si el valor ingresado existe
    if desarrollador not in df['developer'].tolist():
        return {"Respuesta": f"No se encontraron resultados para {desarrollador}, verifique el valor ingresado."}
    
    # Filtro para el developer y agrupo por sentimiento
    reviews = df[(df['developer'] == desarrollador)].groupby('sentiment_analysis').count()
    
    # Convierto a lista
    cantidad_reviews = reviews['developer'].tolist()

    negativos = str(cantidad_reviews[0])
    negativos = 'Negativos = ' + negativos

    positivos = str(cantidad_reviews[1])
    positivos = 'Positivos = ' + positivos

    # Creo el diccionario con la información requerida
    dicc = {}
    dicc[desarrollador] = [negativos,positivos]

    return dicc



@app.get("/prediccion")
def recomendacion(id_juego:int):
    # Cargar el modelo entrenado desde el archivo pickle
    with open('data/Matriz.pkl', 'rb') as file:
        modelo = joblib.load(file)

    data = pd.read_parquet('data/df_modelo.parquet')

    # Valido si el id existe en la muestra seleccionada
    if id_juego not in data['id'].tolist():
        return {"Respuesta": f"No se encontraron resultados para {id_juego}, verifique el valor ingresado."}

    # Defino función para obtener juegos similares
    def get_recommendations(app_name, cosine_sim=modelo ):
        idx = data[data['id'] == app_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:7]  # Top 6 juegos similares
        game_indices = [i[0] for i in sim_scores]
        if idx in game_indices:
            game_indices.remove(idx)
        else:
            sim_scores = sim_scores[1:6]  # Top 5 juegos similares
            game_indices = [i[0] for i in sim_scores]
        return data['app_name'].iloc[game_indices]


    recommendations = get_recommendations(id_juego)

    dicc = recommendations.to_dict()

    return {'Juego consultado':data['app_name'][data['id']==id_juego], 'Juegos similares': dicc}

