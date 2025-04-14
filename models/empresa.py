from sqlalchemy import Column, String, Integer, LargeBinary
from core.database import Base

class Empresas(Base):
    __tablename__ = "empresas"
    id = Column(Integer, primary_key=True, index=True)
    razonSocial = Column(String, nullable=False)
    ruc = Column(String, nullable=False)
    direccion = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    paginaWeb = Column(String, nullable=False)
    logo = Column(LargeBinary, nullable=True)  # Imagen guardada en binario


