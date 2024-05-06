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

class Libro(BaseModel):
    id: Optional[int] = None
    titulo: str = Field(min_length = 1, max_length = 40)
    autor: str  = Field(min_length = 1, max_length = 30)
    año: int = Field(le=2024)
    categoria: str = Field(min_length=1, max_length=30)
    numPaginas: int = Field(ge = 1, le = 3000)

    class Config:
        json_schema_extra = {
            "example": {
                "titulo": "Mi libro",
                "autor":"Pepe",
                "año": 2024,
                "categoria": "Sci-fi",
                "numPaginas": 99
            }
        }

def agregarNombreCategoria(result):
    libros = []
    for libro, nombreCategoria in result:
        libros.append({
            "id": libro.id,
            "titulo": libro.titulo,
            "autor": libro.autor,
            "año": libro.año,
            "categoria": nombreCategoria,
            "numPaginas": libro.numPaginas
        })
    return libros

# Mostrar todos los libros
@libro_router.get('/libros', tags=['libros'], response_model = List[Libro], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_libros() -> List[Libro]:
    db = Session()
    result = db.query(LibroModel, CategoriaModel.nombre).join(CategoriaModel).all()
    if not result:
        return JSONResponse(status_code = 404, content={'message': "No se encontraron libros"})
    libros = agregarNombreCategoria(result)
    return JSONResponse(status_code=200, content=libros)

# Buscar libro por id
@libro_router.get('/libros/{id}', tags=['libros'], response_model = Libro, dependencies=[Depends(JWTBearer())])
def get_libro(id: int = Path(ge = 1)) -> Libro:
    db = Session()
    result = db.query(LibroModel, CategoriaModel.nombre).join(LibroModel.categoria)\
                .filter(LibroModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message': "Libro no encontrado"})
    libros = agregarNombreCategoria([result])
    return JSONResponse(status_code=200, content=libros)

# Buscar libros por categoria (Revisado por el God del Mewing)
@libro_router.get('/libros/', tags=['libros'], response_model = List[Libro], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_libros_by_categoria(categoria: str = Query(min_length = 1, max_length = 30)) -> List[Libro]:
    db = Session()
    result = db.query(LibroModel, CategoriaModel.nombre)\
            .join(CategoriaModel)\
            .filter(CategoriaModel.nombre == categoria)\
            .all()
    if not result:
        return JSONResponse(status_code = 404, content={'message': "No se encontraron libros"})
    libros = agregarNombreCategoria(result)
    return JSONResponse(status_code=200, content=libros)

# Agregar un libro
# (TAMBIEN HECHO POR EL DIOS DEL MEWING)  revivan la grasa :v (livliv)   
@libro_router.post('/libros/', tags=['libros'], response_model= dict, status_code=200, dependencies=[Depends(JWTBearer())])
def create_libro(libro: Libro)->dict:
    db = Session()
    # Verificar si la categoría existe
    categoria = db.query(CategoriaModel).filter(CategoriaModel.nombre == libro.categoria).first()
    if not categoria:
        return JSONResponse(status_code = 404, content={"message": "La categoría no existe."})
    libro2 = libro.model_dump()
    del libro2["categoria"]
    libro2["categoriaId"] = categoria.id
    new_libro = LibroModel(**libro2)
    db.add(new_libro)
    db.commit()
    return JSONResponse(status_code= 200, content={"message": "El libro: "+ libro.titulo +" se registro con exito!"})

# Eliminar un libro
# HECHO POR HAZIEL DEV (EL DIOS DEL MEWING)
# Editado por livers (skibidi mewing sigma digital circus chamba fortnite)
@libro_router.delete('/libros/{id}', tags=['libros'], response_model = dict, status_code= 200, dependencies=[Depends(JWTBearer())])
def delete_libro(id: int = Path(ge = 1)) -> dict:
    db = Session()
    result = db.query(LibroModel).filter(LibroModel.id==id).first()
    if not result:
        return JSONResponse(status_code= 404, content= {"message": "no se encontro el id: "+ str(id)})
    titulo = result.titulo
    db.delete(result)
    db.commit()
    return JSONResponse(status_code= 200, content= {"message": "El libro: " + titulo + " se borró con exito"})
            
# Actualizar un libro
# livliv (¿eeeeeeees confuso verdad? sin embargo, skibidi mewing sigma está mal, todo el globo de texto te lo hace saber. te notas chad, con pensamientos en decadencia. un sentimiento de que el prime no volverá a ser lo mismo.)
@libro_router.put('/libros/{id}', tags=['libros'], response_model = dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def update_libro(id: int, libro:Libro) -> dict:
    db = Session()
    result = db.query(LibroModel).filter(LibroModel.id==id).first()
    if not result:
        return JSONResponse(status_code = 404, content = {"message": "No se encontró el libro."})
    categoria = db.query(CategoriaModel).filter(CategoriaModel.nombre == libro.categoria).first()
    if not categoria:
        return JSONResponse(status_code = 404, content = {"message": "No se encontró la categoria"})
    result.titulo = libro.titulo
    result.autor = libro.autor
    result.año = libro.año
    result.categoriaId = categoria.id
    result.numPaginas = libro.numPaginas
    db.commit()
    return JSONResponse(status_code=200, content = {"message": "Se actualizó correctamente el libro."})