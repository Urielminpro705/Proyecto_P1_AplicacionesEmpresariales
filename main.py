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

# class Libro(BaseModel):
#     codigo: Optional[int] = None
#     titulo: str = Field(min_length = 1, max_length = 40)
#     autor: str  = Field(min_length = 1, max_length = 30)
#     año: int = Field(le=2024)
#     categoria: str = Field(min_length = 3, max_length = 20)
#     numPaginas: int = Field(le = 3, max_length = 2500)

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "codigo": 1,
#                 "titulo": "Mi libro",
#                 "autor":"Pepe",
#                 "año": 2024,
#                 "categoria": "Sci-fi",
#                 "numPaginas": 99
#             }
#         }

# class Categoria(BaseModel):
#     id: Optional[int] = None
#     nombre: str = Field(min_length=1, max_length=30)
#     libros: Optional[int] = 0

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "nombre": "Sci-fi",
#             }
#         }

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
@app.get('/libros/{codigo}', tags=['libros'], response_model = dict)
def get_libro(codigo: int = Path(ge = 1, le = 100)) -> dict:
    for libro in libros:
        if libro["codigo"] == codigo:
            return JSONResponse(status_code = 200, content = libro)
    return JSONResponse(status_code = 404, content = {"message": "No existe este libro"})

# Mostrar todos los libros
@app.get('/libros', tags=['libros'], response_model = List[dict], status_code = 200)
def get_libros() -> List[dict]:
     return JSONResponse(status_code = 200, content=libros)

# Buscar libros por categoria
@app.get('/libros/', tags=['libros'], response_model = List[dict], status_code = 200)
def get_libro_by_categoria(categoria: str = Path(min_length = 1, max_lenght = 12)):
    arreglo = []
    for libro in libros:
        if libro["categoria"] == categoria:
            arreglo.append(libro)
            return JSONResponse(status_code = 200, content = arreglo)
    return JSONResponse(status_code = 404, content= [{"message": "No hay libros con esa categoria"}])

# Eliminar un libro
# HECHO POR HAZIEL DEV (EL DIOS DEL MEWING):
@app.delete('/libros/{codigo}', tags=['libros'], response_model = dict,  status_code= 200)
def delete_libro(codigo: int = Path(ge = 1, le = 1000)) -> dict:
    for item in libros:
        if item["codigo"] == codigo:
            del_item = libros.pop(item)
            return JSONResponse(status_code= 200, content= {"message": del_item['titulo']+" se borro con exito"})
        else:
            return JSONResponse(status_code= 404, content= {"message": "no se encontro el id: "+ codigo})
            
# Agregar un libro
# (TAMBIEN HECHO POR EL DIOS DEL MEWING)       
@app.post('libros/', tags=['libros'], response_model= dict, status_code=200)
def create_libro(nombre: str = Body(), autor: str = Body(), año: int = Body(), categoria: str = Body(), numPaginas: int = Body())->dict:
    libro:dict
    for cat in categorias:
        if cat['nombre'] == categoria:
            if len(libros) > 0:
                cod = libros[len(libros)]['codigo'] 
            else:
                cod = 0
            libro["codigo"] = (cod + 1)
            libro['nombre'] = nombre
            libro['autor'] = autor
            libro['año'] = año
            libro['categoria'] = categoria
            libro['numPaginas'] = numPaginas
            libros.append(libro)
            return JSONResponse(status_code= 200, content={"message": "El libro: "+libro['nombre']+" se registro con exito!"})
        else:
            return JSONResponse(status_code= 409, content = {"message": "No se encontro la categoria: "+categoria})

#------------------------------------------Categorias---------------------------------------#
        
# Mostrar todas las categorias
@app.get('/categorias', tags=['categorias'], response_model = List[dict], status_code = 200)
def get_categorias() -> List[dict]:
    return JSONResponse(status_code = 200, content=categorias)

# Buscar categoria por id
@app.get('/categorias/{id}', tags=['categorias'], response_model = dict, status_code = 200)
def get_categoria_by_categoria(id: int = Path(ge = 1, le = 1000)) -> dict:
    for item in categorias:
        if item['id'] == id :
            return JSONResponse(status_code = 200, content = item)
    return JSONResponse(status_code = 404, content = {"message": "No se encontro la categoria"})

# Crear categoria
@app.post('/categorias/', tags=['categorias'], response_model = dict, status_code = 200)
def create_categoria(nombre: str) -> dict:
    categoria: dict
    categoria['nombre'] = nombre
    if not categorias:
        categoria['id'] = 1
    else:
        ultimo = categorias[-1]
        categoria['id']= ultimo['id'] + 1
    for item in categorias :
        if item['nombre'] == categoria['nombre']:
            return JSONResponse(content= {"message":"La categoria ya existe"})
    categorias.append(categoria)
    return JSONResponse(status_code = 200, content= {"message":"La categoria se creo correctamente"})

# Borrar categoria
@app.delete('/categorias/{id}', tags=['categorias'], response_model= dict, status_code=200)
def delete_cat(ido:int = Path(ge = 1, le = 1000)) -> dict:
    for cat in categorias:
        if(cat["id"] == ido):
            if(cat['libros'] > 0):
                del_item = categorias.pop(cat)
                return JSONResponse(status_code=200, content={"message": "La categoria: "+del_item['nombre']+" se borro con exito 👍"})
            else:
                return JSONResponse(status_code=409, content={"message":"No se puede borrar una categoria que tenga libros dentro de ella"})
        else:
            return JSONResponse(status_code=404, content={"message": "No se encontro la categoria con el id: "+ido})
        

# Actualizar categoria
@app.put('/categorias/{id}', tags=['categorias'], response_model = dict, status_code = 200)
def update_categoria(id: int , nombre: str = Body()) -> dict:
    for item in categorias:
        if item['id'] == id:
            for libro in libros:
                if libro['categoria'] == item['nombre']:
                    libro['categoria'] = nombre
            item['nombre'] = nombre
            return JSONResponse(status_code = 200 ,content = {"message": "Se actualizo correctamente la categoria"})
    return JSONResponse(status_code = 404, content = {"mesage": "La categoria que quiere actualiza no existe"})