from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import APIRouter, Body, Path, Query


categoria_router = APIRouter()

categorias = []

class Categoria(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=30)
    libros: Optional[int] = 0

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Sci-fi",
            }
        }

# Mostrar todas las categorias
@categoria_router.get('/categorias', tags=['categorias'], response_model = List[dict], status_code = 200)
def get_categorias() -> List[dict]:
    return JSONResponse(status_code = 200, content=categorias)

# Buscar categoria por id
@categoria_router.get('/categorias/{id}', tags=['categorias'], response_model = dict, status_code = 200)
def get_categoria_by_id(id: int = Path(ge = 1, le = 1000)) -> dict:
    for item in categorias:
        if item['id'] == id :
            return JSONResponse(status_code = 200, content = item)
    return JSONResponse(status_code = 404, content = {"message": "No se encontro la categoria"})

# Crear categoria
@categoria_router.post('/categorias/', tags=['categorias'], response_model = dict, status_code = 200)
def create_categoria(nombre: str = Query(min_length = 3, max_length = 30)) -> dict:
    
    if len(categorias) == 0:
        id = 1
    else:
        ultimo = categorias[-1]
        id = ultimo["id"] + 1
    for item in categorias :
        if item["id"] == nombre:
            return JSONResponse(content= {"message":"La categoria ya existe"})
    categorias.append({
        "id": id,
        "nombre": nombre,
        "libros": 0
    })
    return JSONResponse(status_code = 200, content= {"message":"La categoria se creo correctamente con id " + str(id)})

# Borrar categoria (Hecho por el dios del MEWING)
@categoria_router.delete('/categorias/{id}', tags=['categorias'], response_model= dict, status_code=200)
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
@categoria_router.put('/categorias/{id}', tags=['categorias'], response_model = dict, status_code = 200)
def update_categoria(id: int = Path(ge = 1, le = 1000) , nombre: str = Body()) -> dict:
    for item in categorias:
        if item["id"] == id:
            for libro in libros:
                if libro["categoria"] == item["nombre"]:
                    libro["categoria"] = nombre
            item["nombre"] = nombre
            return JSONResponse(status_code = 200 ,content = {"message": "Se actualizo correctamente la categoria: "+nombre+" 👍"})
    return JSONResponse(status_code = 404, content = {"mesage": "La categoria: "+nombre+" no existe 😔"})