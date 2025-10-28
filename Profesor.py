from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from db import get_session
from models import Profesor, ProfesorCreate 

router = APIRouter(prefix="/profesores", tags=["Profesores"]) 


@router.get("/", response_model=List[Profesor], summary="Listar todos los profesores activos")
def listar_profesores(session: Session = Depends(get_session)):
    return session.exec(select(Profesor).where(Profesor.active == True)).all()

"""
    Recupera una lista de todos los profesores que están marcados como activos en la base de datos.
"""

@router.get("/eliminados", response_model=List[Profesor], summary="Listar profesores que se fueron")
def listar_profesores_eliminados(session: Session = Depends(get_session)):
    return session.exec(select(Profesor).where(Profesor.active == False)).all()


@router.get("/{profesor_id}", response_model=Profesor, summary="Obtener profesor por ID")
def obtener_profesor(profesor_id: int, session: Session = Depends(get_session)):
    profesor = session.get(Profesor, profesor_id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    return profesor



@router.post("/", response_model=Profesor, summary="Crear un nuevo profesor")
def crear_profesor(profesor: ProfesorCreate, session: Session = Depends(get_session)):
    """
    Registra un nuevo profesor en el sistema.
    - No requiere validación de unicidad según los requisitos del proyecto.
    """
    
    db_profesor = Profesor.model_validate(profesor)
    session.add(db_profesor)
    session.commit()
    session.refresh(db_profesor)
    return db_profesor


@router.delete("/{profesor_id}", summary="Marcar profesor como eliminado")
def eliminar_profesor(profesor_id: int, session: Session = Depends(get_session)):
    profesor = session.get(Profesor, profesor_id)
    if not profesor:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")
    
    profesor.active = False
    session.add(profesor)
    session.commit()
    return {"mensaje": f"Profesor {profesor_id} marcado como eliminado"}


@router.put("/{profesor_id}", response_model=Profesor, summary="Actualizar profesor completo")
def actualizar_profesor(profesor_id: int, profesor_actualizado: ProfesorCreate, session: Session = Depends(get_session)):
    profesor_db = session.get(Profesor, profesor_id)
    if not profesor_db:
        raise HTTPException(status_code=404, detail="Profesor no encontrado")

    profesor_db.nombre = profesor_actualizado.nombre
    profesor_db.especialidad = profesor_actualizado.especialidad

    session.add(profesor_db)
    session.commit()
    session.refresh(profesor_db)
    return profesor_db