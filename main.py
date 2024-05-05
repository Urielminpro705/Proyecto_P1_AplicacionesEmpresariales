# Crear venv: python -m venv venv
# Usar venv: venv\Scripts\activate
# Instalar fastapi: pip install pydantic
# Instalar pydantic: pip install fastapi
# uvicorn main:app --reload
# Objetivos :
# •Perfeccionamiento en la lógica de la creación de apis con FastApi
# •Reforzar conocimientos en python
# •Reconocer errores de lógica
#  ------------------------------------------------
# PARTICIPANTES:
# Ivan Haziel
# Baldwin Esau
# Uriel Mata Castellanos  
# Y ya, somos todos
# y Dios

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routers.libro import libro_router
from routers.categoria import categoria_router
from config.database import Base, engine

app = FastAPI()
app.title = "Libreria"
app.version = "0.1"

app.include_router(libro_router)
app.include_router(categoria_router)

Base.metadata.create_all(bind = engine)

# Pagina inicio
@app.get("/", tags=["Inicio"])
def message():
    return HTMLResponse('<h1 style="color:red"> ¡Bienvenido a la libreria! </h1>')