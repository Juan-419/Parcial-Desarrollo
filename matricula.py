from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlmodel import select
from db import get_session
from models import Matricula, MatriculaCreate, MatriculaProfesorLink, Profesor, Estudiante, Materia
from sqlmodel import Session


router = APIRouter(prefix="/matriculas", tags=["Matrículas"])


@router.get("/", response_model=List[Matricula], summary="Listar todas las matrículas activas")
def listar_matriculas(session: Session = Depends(get_session)):
    return session.exec(select(Matricula).where(Matricula.active == True)).all()


@router.get("/eliminadas", response_model=List[Matricula], summary="Listar matrículas dadas de baja ")
def listar_matriculas_eliminadas(session: Session = Depends(get_session)):
    return session.exec(select(Matricula).where(Matricula.active == False)).all()


@router.get("/{matricula_id}", response_model=Matricula, summary="Obtener matrícula por ID")
def obtener_matricula(matricula_id: int, session: Session = Depends(get_session)):
    matricula = session.get(Matricula, matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    return matricula


@router.post("/", response_model=Matricula, status_code=201, summary="Crear nueva matrícula y asociar profesores")
def crear_matricula(nueva: MatriculaCreate, session: Session = Depends(get_session)):
    """
    Implementa la Lógica de Negocio: Matrícula única (Estudiante + Materia).
    """

    matricula_existente = session.exec(
        select(Matricula).where(
            Matricula.estudiante_id == nueva.estudiante_id,
            Matricula.materia_id == nueva.materia_id
        )
    ).first()
    

    if matricula_existente and matricula_existente.active:
        raise HTTPException(status_code=409, detail="El estudiante ya está matriculado en este curso.")


    estudiante = session.get(Estudiante, nueva.estudiante_id)
    if not estudiante or not estudiante.active:
        raise HTTPException(status_code=404, detail=f"Estudiante ID {nueva.estudiante_id} no encontrado o inactivo")
        
    materia = session.get(Materia, nueva.materia_id)
    if not materia or not materia.active:
        raise HTTPException(status_code=404, detail=f"Materia ID {nueva.materia_id} no encontrada o inactiva")

    db_matricula = Matricula(
        estudiante_id=nueva.estudiante_id,
        materia_id=nueva.materia_id,
        nota_final=nueva.nota_final, 
        fecha_registro=nueva.fecha_registro 
    )
    session.add(db_matricula)
    session.commit()
    session.refresh(db_matricula)
    
    
    if nueva.profesor_ids:
        for profesor_id in nueva.profesor_ids:

            profesor = session.get(Profesor, profesor_id)
            if not profesor or not profesor.active:
                session.rollback()
                raise HTTPException(status_code=404, detail=f"Profesor ID {profesor_id} no encontrado o inactivo")


            link = MatriculaProfesorLink(matricula_id=db_matricula.id, profesor_id=profesor.id)
            session.add(link)
    
    session.commit()
    session.refresh(db_matricula)
    return db_matricula


@router.put("/{matricula_id}", response_model=Matricula, summary="Actualizar matrícula completa")
def actualizar_matricula(matricula_id: int, matricula_actualizada: MatriculaCreate, session: Session = Depends(get_session)):
    matricula_db = session.get(Matricula, matricula_id)
    if not matricula_db:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    matricula_db.nota_final = matricula_actualizada.nota_final
    matricula_db.fecha_registro = matricula_actualizada.fecha_registro
    
    
    session.add(matricula_db)
    session.commit()
    session.refresh(matricula_db)
    return matricula_db


@router.delete("/{matricula_id}", summary="Marcar matrícula como eliminada ")
def eliminar_matricula(matricula_id: int, session: Session = Depends(get_session)):
    
    matricula = session.get(Matricula, matricula_id)
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula no encontrada")
    
    matricula.active = False
    session.add(matricula)
    session.commit()
    return {"mensaje": f"Matrícula {matricula_id} marcada como eliminada"}