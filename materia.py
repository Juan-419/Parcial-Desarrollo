from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional 
from db import get_session

from models import Materia, MateriaCreate 

router = APIRouter(prefix="/materias", tags=["Materias"])


@router.get("/", response_model=List[Materia], summary="Listar todas las materias (Filtro por Créditos)")
def listar_materias(session: Session = Depends(get_session), creditos: Optional[int] = None):
    """
    Lista todas las materias activas, con la opción de filtrar por número de créditos.
    """
    statement = select(Materia).where(Materia.active == True)
    if creditos is not None:
        statement = statement.where(Materia.creditos == creditos)
        
    return session.exec(statement).all()


@router.get("/eliminadas", response_model=List[Materia], summary="Listar materias retiradas" )
def listar_materias_eliminadas(session: Session = Depends(get_session)):
    """
    Lista todas las materias que han sido marcadas como inactivas (retiradas).
    """
    return session.exec(select(Materia).where(Materia.active == False)).all()


@router.get("/codigo/{materia_codigo}", response_model=Materia, summary="Buscar materia por código")
def obtener_materia_por_codigo(materia_codigo: str, session: Session = Depends(get_session)):
    """
    Busca una materia utilizando su código único.
    - Retorna 404 Not Found si el código no existe.
    """
    materia = session.exec(select(Materia).where(Materia.codigo == materia_codigo)).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada o código mal digitado")
    return materia


@router.get("/{materia_id}", response_model=Materia, summary="Obtener materia por ID")
def obtener_materia(materia_id: int, session: Session = Depends(get_session)):
    """
    Busca una materia utilizando su ID primario.
    - Retorna 404 Not Found si el ID no existe.
    """
    materia = session.get(Materia, materia_id)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    return materia


@router.post("/", response_model=Materia, status_code=201, summary="Crear una nueva materia")
def crear_materia(materia: MateriaCreate, session: Session = Depends(get_session)):
    """
    Crea una nueva materia. 
    Aplica Lógica de Negocio: El código de curso debe ser único.
    - Retorna 409 Conflict si el código ya está registrado.
    """

    codigo_existente = session.exec(select(Materia).where(Materia.codigo == materia.codigo)).first()
    if codigo_existente:
        raise HTTPException(status_code=409, detail=f"Ya existe una materia con el código '{materia.codigo}'.")


    db_materia = Materia.model_validate(materia)
    session.add(db_materia)
    session.commit()
    session.refresh(db_materia)
    return db_materia


@router.delete("/{materia_id}", summary="Marcar materia como eliminada ")
def eliminar_materia(materia_id: int, session: Session = Depends(get_session)):
    """
    Realiza una eliminación lógica, marcando la materia como inactiva.
    - Retorna 404 Not Found si el ID no existe.
    """
    materia = session.get(Materia, materia_id)
    if not materia:
        raise HTTPException(status_code=404, detail="Materia no encontrada")
    
    materia.active = False
    session.add(materia)
    session.commit()
    return {"mensaje": f"Materia {materia_id} marcada como eliminada"}


@router.put("/{materia_id}", response_model=Materia, summary="Actualizar materia completa")
def actualizar_materia(materia_id: int, materia_actualizada: MateriaCreate, session: Session = Depends(get_session)):
    """
    Actualiza completamente un registro de materia.
    - Retorna 404 Not Found si el ID no existe.
    """
    materia_db = session.get(Materia, materia_id)
    if not materia_db:
        raise HTTPException(status_code=404, detail="Materia no encontrada")

    
    materia_db.nombre = materia_actualizada.nombre
    materia_db.creditos = materia_actualizada.creditos
    materia_db.codigo = materia_actualizada.codigo

    session.add(materia_db)
    session.commit()
    session.refresh(materia_db)
    return materia_db
