from config.database import Base
from sqlalchemy import Column, Integer, String

class Libro(Base):

    __tablename__ = "libros"

    