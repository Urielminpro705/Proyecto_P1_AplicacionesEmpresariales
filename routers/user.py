from fastapi.responses import JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token
from fastapi import APIRouter, HTTPException

user_router = APIRouter()

class User(BaseModel):
    email: str
    password: str

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    raise HTTPException(status_code = 403, detail = "Credenciales Incorrectas")