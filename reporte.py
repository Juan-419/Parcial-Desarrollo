from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from db import get_session
from models import Estudiante, Materia, Matricula, Profesor, MatriculaProfesorLink
from typing import List


router = APIRouter(tags=["Reportes"])


@router.get("/reporte/estudiante/{estudiante_id}", summary="Generar reporte completo de un estudiante")
def generar_reporte_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    

    estudiante = session.exec(
        select(Estudiante)
        .where(Estudiante.id == estudiante_id)
    ).first()

    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")

    report_data = estudiante.model_dump(by_alias=True)
    report_data['matriculas_detalladas'] = []

    for matricula in estudiante.matriculas:
        
        
        matricula_detalle = matricula.model_dump(by_alias=True)
        
        
        materia_obj = session.get(Materia, matricula.materia_id)
        matricula_detalle['materia'] = materia_obj.nombre if materia_obj else "Materia eliminada"
        profesores_nombres = [p.nombre for p in matricula.profesores]
        matricula_detalle['profesores'] = profesores_nombres
        
        report_data['matriculas_detalladas'].append(matricula_detalle)
    return report_data


@router.get("/reporte/profesores", summary="Listado de profesores y sus matrículas")
def listar_profesores_con_matriculas(session: Session = Depends(get_session)):
    profesores_activos = session.exec(select(Profesor).where(Profesor.active == True)).all()
    
    reporte = []
    for profesor in profesores_activos:
        data = profesor.model_dump(by_alias=True)
        data['matriculas_impartidas'] = [
            f"Matrícula ID {m.id} (Estudiante: {m.estudiante_id}, Materia: {m.materia_id})" 
            for m in profesor.matriculas
        ]
        reporte.append(data)
        
    return reporte