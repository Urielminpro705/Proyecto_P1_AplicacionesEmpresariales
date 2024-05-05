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
        return JSONResponse(status_code = 404, content={'message': "Libro no encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Buscar libros por categoria (Revisado por el God del Mewing)
@libro_router.get('/libros/', tags=['libros'], response_model = List[Libro], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_libros_by_categoria(categoria: str = Query(min_length = 3, max_length = 30)) -> List[Libro]:
    db = Session()
    result = db.query(LibroModel).join(LibroModel.categoria).filter(CategoriaModel.nombre == categoria).all()
    return JSONResponse(status_code = 200, content=jsonable_encoder(result))

# Agregar un libro
# (TAMBIEN HECHO POR EL DIOS DEL MEWING)  revivan la grasa :v (livliv)   
@libro_router.post('/libros/', tags=['libros'], response_model= dict, status_code=200, dependencies=[Depends(JWTBearer())])
def create_libro(libro: Libro)->dict:
    db = Session()
    # Verificar si la categoría existe
    categoria = db.query(CategoriaModel).filter(CategoriaModel.nombre == libro.categoria).first()
    if not categoria:
        return JSONResponse(status_code = 404, content={"message": "La categoría no existe."})
    new_libro = LibroModel(**libro.model_dump(), categoriaId = categoria.id)
    db.add(new_libro)
    db.commit()
    return JSONResponse(status_code= 200, content={"message": "El libro: "+ libro.titulo +" se registro con exito!"})

# Eliminar un libro
# HECHO POR HAZIEL DEV (EL DIOS DEL MEWING)
# Editado por livers (skibidi mewing sigma digital circus chamba fortnite)
@libro_router.delete('/libros/{codigo}', tags=['libros'], response_model = dict, status_code= 200, dependencies=[Depends(JWTBearer())])
def delete_libro(id: int = Path(ge = 0)) -> dict:
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
@libro_router.put('/libros/{codigo}', tags=['libros'], response_model = dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def update_libro(id: int, libro:Libro) -> dict:
    db = Session()
    result = db.query(LibroModel).filter(LibroModel.id==id).first()
    if not result:
        return JSONResponse(status_code = 404, content = {"message": "No se encontró el libro."})
    result.titulo = libro.titulo
    result.autor = libro.autor
    result.año = libro.año
    result.categoria = libro.categoria
    result.numPaginas = libro.numPaginas
    db.commit()
    return JSONResponse(status_code=200, content = {"message": "Se actualizó correctamente el libro."})