from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from db import get_session
from models import Estudiante, EstudianteCreate  

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/", response_model=List[Estudiante], summary="Listar todos los estudiantes activos")
def listar_estudiantes(session: Session = Depends(get_session)):
    return session.exec(select(Estudiante).where(Estudiante.active == True)).all()


@router.get("/eliminados", response_model=List[Estudiante], summary="Listar estudiantes dados de baja (borrado lógico)")
def listar_estudiantes_eliminados(session: Session = Depends(get_session)):
    return session.exec(select(Estudiante).where(Estudiante.active == False)).all()


@router.get("/correo/{estudiante_correo}", response_model=Estudiante, summary="Buscar estudiante por correo")
def obtener_estudiante_por_correo(estudiante_correo: str, session: Session = Depends(get_session)):
    estudiante = session.exec(select(Estudiante).where(Estudiante.correo == estudiante_correo)).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado o correo mal digitado")
    return estudiante


@router.get("/{estudiante_id}", response_model=Estudiante, summary="Obtener estudiante por ID")
def obtener_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.get("/telefono/{estudiante_telefono}", response_model=Estudiante, summary="Buscar estudiante por teléfono")
def obtener_estudiante_por_telefono(estudiante_telefono: str, session: Session = Depends(get_session)):
    estudiante = session.exec(select(Estudiante).where(Estudiante.telefono == estudiante_telefono)).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.post("/", response_model=Estudiante, summary="Crear un nuevo estudiante")
def crear_estudiante(estudiante: EstudianteCreate, session: Session = Depends(get_session)):
    db_estudiante = Estudiante.model_validate(estudiante)
    session.add(db_estudiante)
    session.commit()
    session.refresh(db_estudiante)
    return db_estudiante


@router.delete("/{estudiante_id}", summary="Marcar estudiante como eliminado (baja lógica)")
def eliminar_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
   
    estudiante.active = False
    session.add(estudiante)
    session.commit()
    return {"mensaje": f"Estudiante {estudiante_id} marcado como eliminado"}


@router.put("/{estudiante_id}", response_model=Estudiante, summary="Actualizar estudiante completo")
def actualizar_estudiante(estudiante_id: int, estudiante_actualizado: EstudianteCreate, session: Session = Depends(get_session)):
    estudiante_db = session.get(Estudiante, estudiante_id)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")


    estudiante_db.nombre = estudiante_actualizado.nombre
    estudiante_db.telefono = estudiante_actualizado.telefono
    estudiante_db.correo = estudiante_actualizado.correo

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)
    return estudiante_db