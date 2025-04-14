from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from sqlalchemy import select
import  crud.empresas
from schemas.empresa import EmpresaId, EmpresaData
from fastapi.responses import Response
from core.database import SessionLocal, engine
import models
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# 🔐 CORS para conexión con frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Cambia si tu frontend está en otro dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🧩 DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def  root():
    return "Hi, This is my first API"

@app.get('/empresa/',response_model=list[EmpresaId])
async def  get_empresas(db: Session = Depends(get_db)):
    return crud.empresas.obtener_empresas(db=db)

@app.post('/empresa/', response_model=EmpresaId)
async def create_empresa(empresa:EmpresaData, db: Session= (get_db)):
    return crud.empresas.create_empresa(db=db,empresa=empresa)


# @app.post("/empresas/")
# async def create_empresa(
#     razonSocial: str = Form(...),
#     ruc: str = Form(...),
#     correo: str = Form(...),
#     direccion: str = Form(...),
#     telefono: str = Form(...),
#     paginaWeb: str = Form(...),
#     logo: UploadFile = File(None),
#     db: Session = Depends(get_db)
# ):
#     logo_binario = await logo.read() if logo else None

#     nueva = empresa.Empresas(
#         razonSocial=razonSocial,
#         ruc=ruc,
#         correo=correo,
#         direccion=direccion,
#         telefono=telefono,
#         paginaWeb=paginaWeb,
#         logo=logo_binario
#     )
#     db.add(nueva)
#     db.commit()
#     db.refresh(nueva)
#     return {"message": "Empresa creada", "id": nueva.id}


# @app.get("/empresas/")
# def obtener_empresas(ruc: Optional[str] = None, db: Session = Depends(get_db)):
#     if ruc:
#         empresa = db.query(empresa.Empresas).filter(empresa.Empresas.ruc == ruc).first()
#         if not empresa:
#             raise HTTPException(status_code=404, detail="Empresa no encontrada")

#         return {
#             "id": empresa.id,
#             "ruc": empresa.ruc,
#             "razonSocial": empresa.razonSocial,
#             "correo": empresa.correo,
#             "direccion": empresa.direccion,
#             "telefono": empresa.telefono,
#             "paginaWeb": empresa.paginaWeb,
#             "logo_url": f"http://localhost:8000/empresas/{empresa.id}/logo" if empresa.logo else None
#         }

#     empresas = db.query(empresa.Empresas).all()
#     resultado = []
#     for empresa in empresas:
#         resultado.append({
#             "id": empresa.id,
#             "razonSocial": empresa.razonSocial,
#             "ruc": empresa.ruc,
#             "direccion": empresa.direccion,
#             "telefono": empresa.telefono,
#             "correo": empresa.correo,
#             "paginaWeb": empresa.paginaWeb,
#             "logo": f"http://localhost:8000/empresas/{empresa.id}/logo" if empresa.logo else None
#         })
#     return resultado



# @app.patch("/empresas/{ruc}")
# async def modificar_empresa_por_ruc(
#     ruc: str,
#     razonSocial: Optional[str] = Form(None),
#     correo: Optional[str] = Form(None),
#     direccion: Optional[str] = Form(None),
#     telefono: Optional[str] = Form(None),
#     paginaWeb: Optional[str] = Form(None),
#     logo: Optional[UploadFile] = File(None),
#     db: Session = Depends(get_db)
# ):
#     empresa = db.query(empresa.Empresas).filter(empresa.Empresas.ruc == ruc).first()

#     if not empresa:
#         raise HTTPException(status_code=404, detail="Empresa no encontrada")

#     if razonSocial:
#         empresa.razon_social = razonSocial
#     if correo:
#         empresa.correo = correo
#     if direccion:
#         empresa.direccion = direccion
#     if telefono:
#         empresa.telefono = telefono
#     if paginaWeb:
#         empresa.pagina_web = paginaWeb
#     if logo:
#         empresa.logo = await logo.read()

#     db.commit()
#     db.refresh(empresa)

#     return {
#         "message": "Empresa actualizada parcialmente",
#         "empresa": {
#             "ruc": empresa.ruc,
#             "razon_social": empresa.razonSocial,
#             "correo": empresa.correo,
#             "direccion": empresa.direccion,
#             "telefono": empresa.telefono,
#             "pagina_web": empresa.paginaWeb,
#             "logo_url": f"http://localhost:8000/empresas/{empresa.id}/logo" if empresa.logo else None
#         }
#     }



# @app.delete("/empresas/{ruc}")
# def eliminar_empresa_por_ruc(
#     ruc: str,
#     db: Session = Depends(get_db)
# ):
#     empresa = db.query(empresa.Empresas).filter(empresa.Empresas.ruc == ruc).first()

#     if not empresa:
#         raise HTTPException(status_code=404, detail="Empresa no encontrada")

#     db.delete(empresa)
#     db.commit()

#     return {"message": f"Empresa con RUC {ruc} eliminada correctamente"}