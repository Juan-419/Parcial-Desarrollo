from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import List
from db import get_session
from models import Historial, HistorialCreate, Estudiante, HistorialBase 
from sqlmodel import Session


router = APIRouter(prefix="/historiales", tags=["Historial Académico"])


@router.get("/", response_model=List[Historial], summary="Listar todos los Historiales")
def listar_historiales(session: Session = Depends(get_session)):
    return session.exec(select(Historial)).all()


@router.get("/estudiante/{estudiante_id}", response_model=Historial, summary="Obtener Historial por ID del Estudiante")
def obtener_historial_por_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    """
    Busca el Historial Académico asociado a un Estudiante específico.
    - Retorna 404 Not Found si no existe Historial para ese ID.
    """
    historial = session.exec(select(Historial).where(Historial.estudiante_id == estudiante_id)).first()
    if not historial:
        raise HTTPException(status_code=404, detail=f"No se encontró Historial para el Estudiante ID {estudiante_id}")
    return historial


@router.get("/{historial_id}", response_model=Historial, summary="Obtener Historial por ID")
def obtener_historial(historial_id: int, session: Session = Depends(get_session)):
    historial = session.get(Historial, historial_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")
    return historial


@router.post("/", response_model=Historial, status_code=201, summary="Crear un nuevo Historial")
def crear_historial(nuevo: HistorialCreate, session: Session = Depends(get_session)):

    """
    Crea un nuevo Historial Académico. 
    Aplica Lógica de Negocio: La relación es 1:1, por lo que un estudiante solo puede tener un Historial.
    - Retorna 400 Bad Request si el Estudiante ya tiene un Historial.
    - Retorna 404 Not Found si el Estudiante ID no existe.
    """
    
    estudiante = session.get(Estudiante, nuevo.estudiante_id)
    if not estudiante or not estudiante.active:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado o inactivo")
        
    
    historial_existente = session.exec(select(Historial).where(Historial.estudiante_id == nuevo.estudiante_id)).first()
    if historial_existente:
        raise HTTPException(status_code=400, detail="El Estudiante ya tiene un Historial asociado")
        
    
    db_historial = Historial.model_validate(nuevo)
    session.add(db_historial)
    session.commit()
    session.refresh(db_historial)
    return db_historial


@router.put("/{historial_id}", response_model=Historial, summary="Actualizar un registro de Historial")
def actualizar_historial(historial_id: int, historial_actualizado: HistorialBase, session: Session = Depends(get_session)):
    historial_db = session.get(Historial, historial_id)
    if not historial_db:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    
    if hasattr(historial_actualizado, 'estudiante_id') and historial_actualizado.estudiante_id != historial_db.estudiante_id: #Has atribute
        raise HTTPException(status_code=400, detail="El estudiante_id no puede ser modificado directamente en este endpoint de PUT. Cree un nuevo Historial para otro Estudiante.")

    update_data = historial_actualizado.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(historial_db, key, value)  #Set atribute

    session.add(historial_db)
    session.commit()
    session.refresh(historial_db)
    return historial_db


@router.delete("/{historial_id}", summary="Eliminar físicamente un Historial")
def eliminar_historial(historial_id: int, session: Session = Depends(get_session)):
    historial = session.get(Historial, historial_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Historial no encontrado")

    session.delete(historial)
    session.commit()
    return {"mensaje": f"Historial {historial_id} eliminado exitosamente"}