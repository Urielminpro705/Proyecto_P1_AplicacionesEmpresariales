from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Libro(Base):

    __tablename__ = "libros"

    id = Column(Integer, primary_key = True)
    titulo = Column(String)
    autor = Column(String)
    año = Column(Integer)
    categoriaId = Column(Integer, ForeignKey('categorias.id'))
    numPaginas = Column(Integer)

    categoria = relationship("Categoria", back_populates="libros")