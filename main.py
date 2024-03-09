# Crear venv: python -m venv venv
# Usar venv: venv\Scripts\activate
# Instalar fastapi: pip install pydantic
# Instalar pydantic: pip install fastapi
# uvicorn main:app --reload
# Objetivos :
# •Perfeccionamiento en la lógica de la creación de apiscon FastApi
# •Reforzar conocimientos en python
# •Reconocer errores de lógica
#  ------------------------------------------------
# PARTICIPANTES:
# Ivan Haziel
# Baldwin Esau
# Uriel Mata Castellanos  
# Y ya, somos todos
# y dios

from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List

app = FastAPI()
app.title = "Libreria"
app.version = "0.1"

class Libro(BaseModel):
    codigo: Optional[int] = None
    titulo: str = Field(min_length = 1, max_length = 40)
    autor: str  = Field(min_length = 1, max_length = 30)
    año: int = Field(le=2024)
    categoria: str = Field(min_length = 3, max_length = 20)
    numPaginas: int = Field(le = 3, max_length = 2500)

    class Config:
        json_schema_extra = {
            "example": {
                "codigo": 1,
                "titulo": "Mi libro",
                "autor":"Pepe",
                "año": 2024,
                "categoria": "Sci-fi",
                "numPaginas": 99
            }
        }

class Categoria(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=40)
    libro: int = Field(ge = 1, le = 100)

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Sci-fi",
                "libros": 2
            }
        }

libroFalso = {
    "codigo": 0,
    "titulo":"Indice no encontrado",
    "autor":"",
    "año": 0,
    "categoria": "",
    "numPaginas": 0 
}

libros = [
    {
        "codigo": 1,
        "titulo":"Planet of The Apes",
        "autor":"Pierre Boulle",
        "año": 1963,
        "categoria": "Sci-fi",
        "numPaginas": 272 
    },
    {
        "codigo": 2,
        "titulo":"Scott Pilgrim vs The World",
        "autor":"Bryan Lee O'Malley",
        "año": 2005,
        "categoria": "Comic",
        "numPaginas": 224 
    },
    {
        "codigo": 3,
        "titulo":"Dune",
        "autor":"Frank Herbert",
        "año": 1965,
        "categoria": "Sci-fi",
        "numPaginas": 896 
    }
]

categorias = [
    {
        "id": 1,
        "nombre": "Sci-fi",
        "libros": 2
    },
    {   
        "id": 2,
        "nombre": "Comic",
        "libros": 1
    }
]


# ---------------------------------------------Libros---------------------------------------------#
# Pagina inicio
@app.get("/", tags=["libros"])
def message():
    return HTMLResponse('<h1 style="color:red"> ¡Bienvenido a la libreria! </h1>')

# Buscar libro por id
@app.get('/libros/{codigo}', tags=['libros'], response_model = Libro)
def get_libro(codigo: int = Path(ge = 1, le = 100)):
    for libro in libros:
        if libro["codigo"] == codigo:
            return JSONResponse(status_code = 200, content = libro)
    return JSONResponse(status_code = 404, content = libroFalso)

# Mostrar todos los libros
@app.get('/libros', tags=['libros'], response_model = List[Libro], status_code = 200)
def get_libros() -> List[Libro]:
     return JSONResponse(status_code = 200, content=libros)

# Buscar libros por categoria
@app.get('/libros/', tags=['libros'], response_model = List[Libro], status_code = 200)
def get_libro_by_categoria(categoria: str = Path(min_length = 1, max_lenght = 12)):
    arreglo = []
    for libro in libros:
        if libro["categoria"] == categoria:
            arreglo.append(libro)
            return JSONResponse(status_code = 200, content = arreglo)

# Eliminar un libro
# HECHO POR HAZIEL DEV :
@app.delete('/libros/', tags=['libros'], response_model = str,  status_code= 200)
def delete_libro(codigo: int) -> str:
    for item in libros:
        if item["codigo"] == codigo:
            del_item = libros.pop(item)
            return JSONResponse(status_code= 200, content= del_item['titulo']+" se borro con exito")
        


#------------------------------------------Categorias---------------------------------------#
        
# Mostrar todas las categorias
@app.get('/categorias', tags=['categorias'], response_model = List[Categoria], status_code = 200)
def get_categorias() -> List[Categoria]:
    return JSONResponse(status_code = 200, content=categorias)

# Buscar categoria por id
@app.get('/categorias/{id}', tags=['categorias'], response_model = Categoria, status_code = 200)
def get_categoria_by_categoria(id: int = Path(ge = 1, le = 1000)) -> Categoria:
    for item in categorias:
        if item['id'] == id :
            return JSONResponse(status_code = 200, content = item)
    return JSONResponse(status_code = 404, content = [])

# Crear categoria
@app.post('/categorias/', tags=['categorias'], response_model = str, status_code = 200)
def create_categoria(nombre: str = Body()) -> str:
    for item 
    return JSONResponse(content = "La categoria se creo correctamente")