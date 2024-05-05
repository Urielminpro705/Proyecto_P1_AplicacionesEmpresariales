from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import APIRouter, Body, Depends, Path, Query
from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from models.libro import Libro as LibroModel
from models.categoria import Categoria as CategoriaModel
from fastapi.encoders import jsonable_encoder

libro_router = APIRouter()
libros = []

class Libro(BaseModel):
    id: Optional[int] = None
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

# Mostrar todos los libros
@libro_router.get('/libros', tags=['libros'], response_model = List[Libro], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_libros() -> List[Libro]:
    db = Session()
    result = db.query(LibroModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Buscar libro por id
@libro_router.get('/libros/{codigo}', tags=['libros'], response_model = Libro, dependencies=[Depends(JWTBearer())])
def get_libro(id: int = Path(ge = 1)) -> Libro:
    db = Session()
    result = db.query(LibroModel).filter(LibroModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message': "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Buscar libros por categoria (Revisado por el God del Mewing)
@libro_router.get('/libros/', tags=['libros'], response_model = List[dict], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_libros_by_categoria(categoria: str = Query(min_length = 3, max_length = 30)) -> List[dict]:
    db = Session()
    result = db.query(LibroModel).join(LibroModel.categoria).filter(CategoriaModel.nombre == categoria).all()
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

# # Eliminar un libro
# # HECHO POR HAZIEL DEV (EL DIOS DEL MEWING):
# @libro_router.delete('/libros/{codigo}', tags=['libros'], response_model = dict,  status_code= 200, dependencies=[Depends(JWTBearer())])
# def delete_libro(codigo: int = Path(ge = 1, le = 1000)) -> dict:
#     nombre = ""
#     for item in libros:
#         if item["codigo"] == codigo:
#             nombre = item['titulo']
#             libros.remove(item)
#             for cat in categorias:
#                 if cat["nombre"] == item["categoria"]:
#                     cat["libros"] -= 1 
#             return JSONResponse(status_code= 200, content= {"message": "El libro: "+nombre+" se borro con exito"})
#     return JSONResponse(status_code= 404, content= {"message": "no se encontro el id: "+ str(codigo)})
            
# Actualizar un libro
# @libro_router.put('/libros/{codigo}', tags=['libros'], response_model = dict, status_code = 200, dependencies=[Depends(JWTBearer())])
# def update_libro(codigo: int = Path(ge = 1, le = 1000), titulo: str=Body(), autor: str=Body(), año: int=Body(), categoria: str=Body(), numPaginas: int=Body()):
#     for item in categorias:
#         if item["nombre"] == categoria:
#             for item in libros:
#                 if item["codigo"] == codigo:
#                     item["titulo"] = titulo
#                     item["autor"] = autor
#                     item["año"] = año
#                     item["categoria"] = categoria
#                     item["numPaginas"] = numPaginas
#                     return JSONResponse(status_code=200, content = {"message": "Se actualizó correctamente el libro."})
#             return JSONResponse(status_code = 404, content = {"message": "No se encontró el libro."})
#     return JSONResponse(status_code = 404, content={"message": "La categoría especificada no existe."})


# # Agregar un libro
# # (TAMBIEN HECHO POR EL DIOS DEL MEWING)       
# @libro_router.post('/libros/', tags=['libros'], response_model= dict, status_code=200, dependencies=[Depends(JWTBearer())])
# def create_libro(nombre: str = Body(), autor: str = Body(), año: int = Body(), categoria: str = Body(), numPaginas: int = Body())->dict:
#     exists = False
#     #//? Aqui empieza el ciclo for, donde se verifica que exista la categoria y asignar el id
#     for cat in categorias:
#         if cat['nombre'] == categoria:
#             exists = True
#             cat["libros"] += 1 
#             if len(libros) > 0:
#                 ultimo = libros[-1]
#                 cod = ultimo["codigo"]
#             else:
#                 cod = 0     
#     #//? Aqui termina el ciclo for
#     if exists == True:
#         libros.append({
#             "codigo": (cod + 1),
#             "nombre": nombre,
#             "autor": autor,
#             "año": año,
#             "categoria": categoria,
#             "numPaginas": numPaginas
#         })
#         return JSONResponse(status_code= 200, content={"message": "El libro: "+nombre+" se registro con exito! con id " + str(cod + 1)})
#     else:
#         return JSONResponse(status_code= 409, content = {"message": "No se encontro la categoria: "+categoria})