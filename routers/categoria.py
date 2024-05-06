from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import APIRouter, Depends, Path
from middlewares.jwt_bearer import JWTBearer
from models.categoria import Categoria as CategoriaModel
from models.libro import Libro as LibroModel
from config.database import Session

categoria_router = APIRouter()

class Categoria(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(min_length=1, max_length=30)

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Sci-fi",
            }
        }

# Mostrar todas las categorias
@categoria_router.get('/categorias', tags=['categorias'], response_model = List[Categoria], status_code = 200, dependencies=[Depends(JWTBearer())])
def get_categorias() -> List[Categoria]:
    db = Session()
    result = db.query(CategoriaModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

# Buscar categoria por id
@categoria_router.get('/categorias/{id}', tags=['categorias'], response_model = Categoria, status_code = 200, dependencies=[Depends(JWTBearer())])
def get_categoria_by_id(id: int = Path(ge = 0)) -> Categoria:
    db = Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
        return JSONResponse(status_code = 404, content={'message': "Categoria con el id:"+id+" No encontrada :c"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@categoria_router.post('/categorias/', tags=['categorias'], response_model = dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def create_categoria(categoria:Categoria) -> dict:
    db = Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.nombre == categoria.nombre).first()
    if result:
        return JSONResponse(status_code = 404, content={'message': "Ya existe esta categoria"})
    new_categoria = CategoriaModel(nombre=categoria.nombre)
    db.add(new_categoria)
    db.commit()
    return JSONResponse(status_code= 200, content={"message": "La categoría: "+ categoria.nombre +" se registro con exito."})

# Borrar categoria (Hecho por el dios del MEWING HAZIELDEV))
@categoria_router.delete('/categorias/{id}', tags=['categorias'], response_model= dict, status_code=200, dependencies=[Depends(JWTBearer())])
def delete_cat(id:int = Path(ge = 1)) -> dict:
    db = Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id == id).first()
    if not result:
        return JSONResponse(status_code= 404, content = {"message":"No se encontro la categoria con el id: ("+str(id)+") :c"})
    libros = db.query(LibroModel).filter(LibroModel.categoriaId == id).all()
    if libros:
        librosCount = len(libros)
        return JSONResponse(status_code=404, content= {"message":"No se puede borrar porque hay ("+str(librosCount)+") libros en esta categoria"})
    db.delete()
    db.commit()
    return JSONResponse(status_code= 200, content={"message":"Se borro la categoria ("+result.nombre+")"})
    
# Actualizar categoria
@categoria_router.put('/categorias/{id}', tags=['categorias'], response_model = dict, status_code = 200, dependencies=[Depends(JWTBearer())])
def update_categoria(id: int, categoria: Categoria) -> dict:
    db = Session()
    result = db.query(CategoriaModel).filter(CategoriaModel.id==id).first()
    if not result:
        return JSONResponse(status_code = 404, content = {"message": "No se encontró la categoría."})
    result.nombre = categoria.nombre
    db.commit()
    return JSONResponse(status_code=200, content = {"message": "Se actualizó correctamente la categoría."})
