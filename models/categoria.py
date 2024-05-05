from config.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Categoria(Base):

    __tablename__ = "categorias"

    id = Column(Integer, primary_key = True)
    nombre = Column(String)

    libros = relationship("Libro", back_populates="categoria")