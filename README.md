# Steam: Sistema de Recomendación de Videojuegos para Usuarios.
![](./img/steam.jpg)

Este repositorio contiene un conjunto de funciones y un modelo de machine learning mediante el cual podrás obtener una recomendación de 5 videojuegos similares a algún videojuego particular que sea de tu interés.

## Índice de Contenido
- [Introducción](#introducción)
- [Configuración](#configuración)
- [Uso](#uso)
- [Sistema de recomendación](#recomendación)
- [Contacto](#contacto)
- [Tecnologías utilizadas](#tecnologías)

# Configuración
1. Clona este repositorio en tu sistema local.

2. Asegúrate de tener los archivos de datos disponibles en la carpeta data/ en el directorio del proyecto, así como las librerías listadas en requirements.txt

3. Ejecuta el archivo main.py para iniciar el servidor FastAPI:
   ```python
   python main.py

# Uso
Una vez tu servidor de FastAPI esté funcionando podrás usar las siguientes funciones:
* `/developer`: Dada una empresa desarrolladora, obtendrás la cantidad de juegos creados por año y el porcentaje de contenido Free por año.
* `/userdata`: Dado un id de usuario, obtendrás la cantidad de dinero gastado y el porcentaje de recomendación de dicho usuario.
* `/UserForGenre`: Dado un género, obtendrás el usuario que acumula más horas jugadas para ese género, y una lista de la acumulación de horas jugadas por año de lanzamiento.
* `/best_developer_year`: Dado un año, obtendrás el top 3 de desarrolladores con juegos más recomendados por los usuarios para dicho año.
* `/sentiment`: Dada una empresa desarrolladora, obtendrás la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo.
* `/recomendacion_juego`: Dado un id de juego, obtendrás una lista con 5 juegos recomendados, similares al juego ingresado.

**NOTA**: También puedes usar las funciones accediendo al enlace https://api1-vmeg.onrender.com/docs, que corresponde a la API deployada en Render.

# Sistema de recomendación
El sistema de recomendación utiliza un modelo de machine learning basado en similitud de contenido, el cual usa las características de los ítems para generar recomendaciones personalizadas.

1. **Elementos del Modelo**:

   - *Videojuegos (Items)*: Estos son los objetos que se recomiendan. En este caso, los ítems son videojuegos.

   - *Atributos del juego*: Son las características o metadatos asociados a cada videojuego. En este caso, los atributos incluyen los géneros, etiquetas, especificaciones de cada juego.

2. **Funcionamiento del Modelo**:

   - *Extracción de Características (Feature Extraction)*: En este modelo, se extraen características de los juegos a partir de sus atributos. Estas características se utilizan para medir la similitud entre los juegos. En este caso, se utiliza una matriz TF-IDF para representar los atributos de los juegos.

   - *Cálculo de Similitud*: Se calcula la similitud entre los ítems en función de las características extraídas. La similitud del coseno es una medida común que se utiliza para determinar cuán similares son dos ítems. Cuanto más cercano a 1 sea el valor del coseno, mayor será la similitud entre los ítems.

   - *Generación de Recomendaciones*: Una vez que se obtiene la matriz de similitud, se pueden generar recomendaciones para un juego específico, devolviendo otros juegos con alta similitud al ítem dado.

**NOTA**: Por falta de recursos computacionales, se tomó una muestra aleatoria de 5.000 juegos, ya que la matriz de similitud era demasiado pesada al generarse con los 28.766 juegos distintos que hay en el dataset original. Para testear la función puedes usar los juegos listados en el archivo [df_steam_games_selected.csv](./data/df_steam_games_selected.csv).

# Contacto
Eduar A. Castañeda Molina

LinkedIn: [edcast05](https://www.linkedin.com/in/edcast05/)

Correo electrónico: eduarcastanedam@gmail.com

# Tecnologías utilizadas
Python | Pandas | Matplotlib | Seaborn | Scikit-Learn | FastAPI | Render
