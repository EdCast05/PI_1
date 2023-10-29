# Steam: Sistema de Recomendación de Videojuegos para Usuarios.
![](./img/steam.jpg)

Este repositorio contiene un conjunto de funciones y un modelo de machine learning mediante el cual podrás obtener una recomendación de 5 videojuegos similares a algún videojuego particular que sea de tu interés.

## Índice de Contenido
- [Introducción](#introducción)
- [Configuración](#configuración)
- [Uso](#uso)
- [Contribución](#contribución)
- [Licencia](#licencia)

# Configuración
1. Clona este repositorio en tu sistema local.

2. Asegúrate de tener los archivos de datos disponibles en la carpeta data/ en el directorio del proyecto:

3. Ejecuta el archivo main.py para iniciar el servidor FastAPI:
   ```python
   python main.py

# Uso
Una vez tu servidor de FastAPI esté funcionando podrás usar las siguientes funciones:
* `/developer/`: Obtendrás la cantidad de juegos creados y el porcentaje de contenido Free por año, dada una empresa desarrolladora.
* `/userdata/`: Obtendrás la cantidad de dinero gastado para un usuario dado, y el porcentaje de recomendación de dicho usuario.
* `/UserForGenre/`: Obtendrás el usuario que acumula más horas jugadas para el género dado, y una lista de la acumulación de horas jugadas por año de lanzamiento.
* `/best_developer_year/`: Obtendrás el top 3 de desarrolladores con juegos más recomendados por los usuarios para el año dado.
* `/sentiment/`: Obtendrás la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor positivo o negativo, dada una empresa desarrolladora.
* `/prediccion`: Dado un id de juego, obtendrás una lista con 5 juegos recomendados, similares al juego ingresado.

