from pydantic import BaseModel

class EmpresaData(BaseModel):
    razonSocial : str
    ruc : str
    correo: str 
    direccion: str 
    telefono: str 
    paginaWeb: str
    logo: bytes

class EmpresaId(EmpresaData):
        id:  int
