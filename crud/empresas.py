from sqlalchemy.orm import Session
import models
# from schemas.empresa import EmpresasData
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Path
from typing import Optional

import models.empresa


async def create_empresa(db: Session,
    razonSocial: str = Form(...),
    ruc: str = Form(...),
    correo: str = Form(...),
    direccion: str = Form(...),
    telefono: str = Form(...),
    paginaWeb: str = Form(...),
    logo: UploadFile = File(None)
    
):
    logo_binario = await logo.read() if logo else None

    nueva = models.empresa.Empresas(
        razonSocial=razonSocial,
        ruc=ruc,
        correo=correo,
        direccion=direccion,
        telefono=telefono,
        paginaWeb=paginaWeb,
        logo=logo_binario
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return {"message": "Empresa creada", "id": nueva.id}



def obtener_empresas( db: Session, ruc: Optional[str] = None):
    if ruc:
        empresa = db.query(models.empresa.Empresas).filter(models.empresa.Empresas.ruc == ruc).first()
        if not empresa:
            raise HTTPException(status_code=404, detail="Empresa no encontrada")

        return {
            "id": empresa.id,
            "ruc": empresa.ruc,
            "razonSocial": empresa.razonSocial,
            "correo": empresa.correo,
            "direccion": empresa.direccion,
            "telefono": empresa.telefono,
            "paginaWeb": empresa.paginaWeb,
            "logo_url": f"http://localhost:8000/empresas/{empresa.id}/logo" if empresa.logo else None
        }

    empresas = db.query(models.empresa.Empresas).all()
    resultado = []
    for empresa in empresas:
        resultado.append({
            "id": empresa.id,
            "razonSocial": empresa.razonSocial,
            "ruc": empresa.ruc,
            "direccion": empresa.direccion,
            "telefono": empresa.telefono,
            "correo": empresa.correo,
            "paginaWeb": empresa.paginaWeb,
            "logo": f"http://localhost:8000/empresas/{empresa.id}/logo" if empresa.logo else None
        })
    return resultado


async def modificar_empresa_por_ruc(db: Session,
    ruc: str,
    razonSocial: Optional[str] = Form(None),
    correo: Optional[str] = Form(None),
    direccion: Optional[str] = Form(None),
    telefono: Optional[str] = Form(None),
    paginaWeb: Optional[str] = Form(None),
    logo: Optional[UploadFile] = File(None)
    
):
    empresa = db.query(empresa.Empresas).filter(empresa.Empresas.ruc == ruc).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    if razonSocial:
        empresa.razon_social = razonSocial
    if correo:
        empresa.correo = correo
    if direccion:
        empresa.direccion = direccion
    if telefono:
        empresa.telefono = telefono
    if paginaWeb:
        empresa.pagina_web = paginaWeb
    if logo:
        empresa.logo = await logo.read()

    db.commit()
    db.refresh(empresa)

    return {
        "message": "Empresa actualizada parcialmente",
        "empresa": {
            "ruc": empresa.ruc,
            "razon_social": empresa.razonSocial,
            "correo": empresa.correo,
            "direccion": empresa.direccion,
            "telefono": empresa.telefono,
            "pagina_web": empresa.paginaWeb,
            "logo_url": f"http://localhost:8000/empresas/{empresa.id}/logo" if empresa.logo else None
        }
    }



def eliminar_empresa_por_ruc(
    ruc: str,
    db: Session
):
    empresa = db.query(empresa.Empresas).filter(empresa.Empresas.ruc == ruc).first()

    if not empresa:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    db.delete(empresa)
    db.commit()

    return {"message": f"Empresa con RUC {ruc} eliminada correctamente"}



