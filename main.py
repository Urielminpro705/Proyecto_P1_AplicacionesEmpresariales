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
from typing import List

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

# Mostrar todos los libros
@app.get('/libros', tags=['libros'], response_model = List[dict], status_code = 200)
def get_libros() -> List[dict]:
    return JSONResponse(status_code = 200, content=libros)

# Buscar libro por id
@app.get('/libros/{codigo}', tags=['libros'], response_model = dict)
def get_libro(codigo: int = Path(ge = 1, le = 100)) -> dict:
    for libro in libros:
        if libro["codigo"] == codigo:
            return JSONResponse(status_code = 200, content = libro)
    return JSONResponse(status_code = 404, content = {"message": "No existe este libro"})

# Buscar libros por categoria (Revisado por el God del Mewing)
@app.get('/libros/', tags=['libros'], response_model = List[dict], status_code = 200)
def get_libros_by_categoria(categoria: str = Query(min_length = 3, max_length = 30)) -> List[dict]:
    arreglo = []
    for libro in libros:
        if libro["categoria"] == categoria:
            arreglo.append(libro)
    
    if(len(arreglo) > 0):
        return JSONResponse(status_code = 200, content = arreglo)
    else:
        return JSONResponse(status_code = 404, content= [{"message": "No hay libros con la Categoria: "+categoria}])

# Eliminar un libro
# HECHO POR HAZIEL DEV (EL DIOS DEL MEWING):
@app.delete('/libros/{codigo}', tags=['libros'], response_model = dict,  status_code= 200)
def delete_libro(codigo: int = Path(ge = 1, le = 1000)) -> dict:
    nombre = ""
    for item in libros:
        if item["codigo"] == codigo:
            nombre = item['titulo']
            libros.remove(item)
            for cat in categorias:
                if cat["nombre"] == item["categoria"]:
                    cat["libros"] -= 1 
            return JSONResponse(status_code= 200, content= {"message": "El libro: "+nombre+" se borro con exito"})
    return JSONResponse(status_code= 404, content= {"message": "no se encontro el id: "+ str(codigo)})
            
# Actualizar un libro
@app.put('/libros/{codigo}', tags=['libros'], response_model = dict, status_code = 200)
def update_libro(codigo: int = Path(ge = 1, le = 1000), titulo: str=Body(), autor: str=Body(), año: int=Body(), categoria: str=Body(), numPaginas: int=Body()):
    for item in categorias:
        if item["nombre"] == categoria:
            for item in libros:
                if item["codigo"] == codigo:
                    item["titulo"] = titulo
                    item["autor"] = autor
                    item["año"] = año
                    item["categoria"] = categoria
                    item["numPaginas"] = numPaginas
                    return JSONResponse(status_code=200, content = {"message": "Se actualizó correctamente el libro."})
            return JSONResponse(status_code = 404, content = {"message": "No se encontró el libro."})
    return JSONResponse(status_code = 404, content={"message": "La categoría especificada no existe."})


# Agregar un libro
# (TAMBIEN HECHO POR EL DIOS DEL MEWING)       
@app.post('/libros/', tags=['libros'], response_model= dict, status_code=200)
def create_libro(nombre: str = Body(), autor: str = Body(), año: int = Body(), categoria: str = Body(), numPaginas: int = Body())->dict:
    exists = False
    #//? Aqui empieza el ciclo for, donde se verifica que exista la categoria y asignar el id
    for cat in categorias:
        if cat['nombre'] == categoria:
            exists = True
            cat["libros"] += 1 
            if len(libros) > 0:
                ultimo = libros[-1]
                cod = ultimo["codigo"]
            else:
                cod = 0     
    #//? Aqui termina el ciclo for
    if exists == True:
        libros.append({
            "codigo": (cod + 1),
            "nombre": nombre,
            "autor": autor,
            "año": año,
            "categoria": categoria,
            "numPaginas": numPaginas
        })
        return JSONResponse(status_code= 200, content={"message": "El libro: "+nombre+" se registro con exito! con id " + str(cod + 1)})
    else:
        return JSONResponse(status_code= 409, content = {"message": "No se encontro la categoria: "+categoria})

#------------------------------------------Categorias---------------------------------------#
        
# Mostrar todas las categorias
@app.get('/categorias', tags=['categorias'], response_model = List[dict], status_code = 200)
def get_categorias() -> List[dict]:
    return JSONResponse(status_code = 200, content=categorias)

# Buscar categoria por id
@app.get('/categorias/{id}', tags=['categorias'], response_model = dict, status_code = 200)
def get_categoria_by_id(id: int = Path(ge = 1, le = 1000)) -> dict:
    for item in categorias:
        if item['id'] == id :
            return JSONResponse(status_code = 200, content = item)
    return JSONResponse(status_code = 404, content = {"message": "No se encontro la categoria"})

# Crear categoria
@app.post('/categorias/', tags=['categorias'], response_model = dict, status_code = 200)
def create_categoria(nombre: str = Query(min_length = 3, max_length = 30)) -> dict:
    
    if len(categorias) == 0:
        id = 1
    else:
        ultimo = categorias[-1]
        id = ultimo["id"] + 1
    for item in categorias :
        if item["nombre"] == nombre:
            return JSONResponse(content= {"message":"La categoria ya existe"})
    categorias.append({
        "id": id,
        "nombre": nombre,
        "libros": 0
    })
    return JSONResponse(status_code = 200, content= {"message":"La categoria se creo correctamente con id " + str(id)})

# Borrar categoria (Hecho por el dios del MEWING)
@app.delete('/categorias/{id}', tags=['categorias'], response_model= dict, status_code=200)
def delete_cat(id:int = Path(ge = 1, le = 1000)) -> dict:
    name = ""
    for cat in categorias:
        if(cat["id"] == id):
            if(cat["libros"] == 0):
                name = cat['nombre']
                categorias.remove(cat)
                return JSONResponse(status_code=200, content={"message": "La categoria: "+name+" se borro con exito 👍"})
            else:
                return JSONResponse(status_code=409, content={"message":"No se puede borrar una categoria que tenga libros dentro de ella"})
    return JSONResponse(status_code=404, content={"message": "No se encontro la categoria con el id: "+str(id)})
        
# Actualizar categoria
@app.put('/categorias/{id}', tags=['categorias'], response_model = dict, status_code = 200)
def update_categoria(id: int = Path(ge = 1, le = 1000) , nombre: str = Body()) -> dict:
    for item in categorias:
        if item["id"] == id:
            for libro in libros:
                if libro["categoria"] == item["nombre"]:
                    libro["categoria"] = nombre
            item["nombre"] = nombre
            return JSONResponse(status_code = 200 ,content = {"message": "Se actualizo correctamente la categoria: "+nombre+" 👍"})
    return JSONResponse(status_code = 404, content = {"mesage": "La categoria: "+nombre+" no existe 😔"})