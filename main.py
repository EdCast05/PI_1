from fastapi import FastAPI
import pandas as pd 
import pyarrow.parquet as pq
import joblib

app = FastAPI()

@app.get('/') #Endpoint
def home():
    return {"message": "Hola mundo FastAPI"}

@app.get("/developer/")
def developer(desarrollador: str):
    
    # Cargar la base de datos
    df = pd.read_parquet('data/df_endpoint1.parquet')

    if desarrollador not in df['developer'].tolist():
        return {"Respuesta": "No se encontraron resultados para la búsqueda realizada"}


    cantidad = df[df['developer'] == desarrollador].groupby('anio').count()
    cantidad_free = df[(df['developer'] == desarrollador) & (df['price'] == 0.0)].groupby('anio').count()

    cantidad_juegos = cantidad['developer'].tolist()
    cantidad_juegos_free = cantidad_free['developer'].tolist()

    anio = cantidad.index.tolist()
    anio_free = cantidad_free.index.tolist()

    porc_cont_free = {}

    for i in range(len(anio)):
        if anio[i] not in anio_free:
            porc_cont_free[anio[i]] = [cantidad_juegos[i],"0%"]
        else:
            for j in range(len(anio_free)):
                if anio_free[j]==anio[i]:
                    porc_cont_free[anio[i]] = [cantidad_juegos[i], f'{round(cantidad_juegos_free[j]/cantidad_juegos[i]*100,2)}%']
    
    return {f'Respuesta para {desarrollador}': porc_cont_free}


@app.get("/sentiment/")
def developer_reviews_analysis(desarrolladora: str):

    # Cargar la base de datos
    df = pd.read_parquet('data/df_endpoint2.parquet')

    if desarrolladora not in df['developer'].tolist():
        return {"Respuesta": "No se encontraron resultados para la búsqueda realizada"}

    reviews = df[(df['developer'] == desarrolladora)].groupby('sentiment_analysis').count()
    
    cantidad_reviews = reviews['developer'].tolist()

    negativos = str(cantidad_reviews[0])
    negativos = 'Negativos: ' + negativos

    positivos = str(cantidad_reviews[1])
    positivos = 'Positivos: ' + positivos

    dicc = {}
    dicc[desarrolladora] = [negativos,positivos]

    return {f'Respuesta para {desarrolladora}': dicc}


@app.get("/userdata/")
def userdata(user_id: str):
    # Cargar la base de datos
    df = pd.read_parquet('data/df_endpoint3.parquet')

    if user_id not in df['user_id'].tolist():
        return {"Respuesta": "No se encontraron resultados para la búsqueda realizada"}


    cantidad = df[(df['user_id'] == user_id)].groupby('recommend').count()
    dinero = df[(df['user_id'] == user_id)].groupby('price').count()

    spent = dinero.index.tolist()
    spent = [float(value) for value in spent]

    recommend = cantidad.index.tolist()

    cantidad_items_recom = cantidad['item_id'].tolist()

    if len(recommend) == 1:
        if recommend[0] == 'true':
            dicc = {"Usuario": user_id, "Dinero gastado": f'${round(sum(spent),2)}', "% de recomendación": f'100%', "cantidad de items": sum(cantidad_items_recom)}
        else:
            dicc = {"Usuario": user_id, "Dinero gastado": f'${round(sum(spent),2)}', "% de recomendación": f'0%', "cantidad de items": sum(cantidad_items_recom)} 
    else:
        dicc = {"Usuario": user_id, "Dinero gastado": f'${round(sum(spent),2)}', "% de recomendación": f'{round(cantidad_items_recom[1]/sum(cantidad_items_recom)*100,2)}%', "cantidad de items": sum(cantidad_items_recom)}

    return {'Respuesta': dicc}


'''@app.get("/UserForGenre/")
def UserForGenre(genero: str):
    # Cargar la base de datos
    df = pd.read_parquet('data/df_endpoint4.parquet')

    cantidad = df[(df['genres'] == genero)].groupby('user_id').sum()
    cantidad.reset_index(inplace=True)

    usuario = cantidad.loc[cantidad['playtime_forever'].idxmax()]['user_id']

    poranio = df[(df['genres'] == genero) & (df['user_id']==usuario)].groupby('anio').sum()
    poranio.drop('item_id',axis=1,inplace=True)

    poranio = poranio.to_dict()
    dicc = {}
    dicc['usuario'] = usuario
    dicc['años'] = poranio["playtime_forever"]
    
    return dicc'''

@app.get("/UserForGenre/")
def obtener_informacion_por_genero(genero: str):
    # Cargar la base de datos
    df = pd.read_parquet('data/df_endpoint4.parquet')

    # Filtrar el DataFrame para el género especificado
    df_genero = df[df['genres'] == genero]

    # Agrupar por 'user_id' y sumar 'playtime_forever'
    cantidad = df_genero.groupby('user_id')['playtime_forever'].sum().reset_index()

    # Encontrar al usuario con la máxima cantidad de playtime
    usuario_max_playtime = cantidad.loc[cantidad['playtime_forever'].idxmax()]['user_id']

    # Filtrar el DataFrame original por usuario y género
    df_usuario_genero = df[(df['genres'] == genero) & (df['user_id'] == usuario_max_playtime)]

    # Agrupar por año y sumar el tiempo de juego
    poranio = df_usuario_genero.groupby('anio')['playtime_forever'].sum().to_dict()

    # Crear un diccionario con la información
    dicc = {
        'usuario': usuario_max_playtime,
        'años': poranio
    }

    return dicc

@app.get("/best_developer_year/")
def best_developer_year(año: int):

    df = pd.read_parquet('data/df_endpoint5.parquet')

    cantidad = df[(df['anio'] == año)].groupby('developer').count()
    cantidad.reset_index(inplace=True)

    cantidad = cantidad.sort_values(by='anio', ascending=False)
    cantidad = cantidad[['developer','anio']]

    cantidad.set_index('developer', inplace=True)
    cantidad.columns = ['Cantidad']

    primeros_tres = cantidad.iloc[:3]
    dicc = primeros_tres.to_dict()

    return dicc


@app.get("/prediccion")
def recomendacion(juego:str):
    # Cargar el modelo entrenado desde el archivo pickle
    with open('data/Mejor_pipeline.pkl', 'rb') as file:
        modelo = joblib.load(file)

    data = pd.read_parquet('data/df_endpoint6.parquet')

    def get_recommendations(app_name, cosine_sim=modelo ):
        idx = data[data['app_name'] == app_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]  # Top 5 juegos similares
        game_indices = [i[0] for i in sim_scores]
        return data['app_name'].iloc[game_indices]


    recommendations = get_recommendations(juego)

    dicc = recommendations.to_dict()

    return dicc
