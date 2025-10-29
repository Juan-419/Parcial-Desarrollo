from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Optional 
from db import get_session
from models import Estudiante, EstudianteCreate  
from sqlalchemy.orm import selectinload 

router = APIRouter(prefix="/estudiantes", tags=["Estudiantes"])


@router.get("/", response_model=List[Estudiante], summary="Listar todos los estudiantes (Filtro por Semestre)")
def listar_estudiantes(session: Session = Depends(get_session), semestre: Optional[int] = None):
    """
    Lista todos los estudiantes activos, con la opción de filtrar por semestre académico.
    """
    statement = select(Estudiante).where(Estudiante.active == True)
    
    if semestre is not None:
        statement = statement.where(Estudiante.semestre == semestre)
        
    return session.exec(statement).all()


@router.get("/eliminados", response_model=List[Estudiante], summary="Listar estudiantes dados de baja ")
def listar_estudiantes_eliminados(session: Session = Depends(get_session)):
    """
    Lista todos los estudiantes que han sido marcados como inactivos.
    """
    return session.exec(select(Estudiante).where(Estudiante.active == False)).all()


@router.get("/correo/{estudiante_correo}", response_model=Estudiante, summary="Buscar estudiante por correo")
def obtener_estudiante_por_correo(estudiante_correo: str, session: Session = Depends(get_session)):
    """
    Busca un estudiante específico utilizando su dirección de correo electrónico.
    - Retorna 404 Not Found si el correo no existe.
    """
    estudiante = session.exec(select(Estudiante).where(Estudiante.correo == estudiante_correo)).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado o correo mal digitado")
    return estudiante


@router.get("/{estudiante_id}", response_model=Estudiante, summary="Obtener estudiante por ID con sus matrículas")
def obtener_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    """
    Consulta relacional obligatoria: Obtener estudiante y sus cursos matriculados.
    Utiliza selectinload para cargar las matrículas de manera eficiente.
    - Retorna 404 Not Found si el ID no existe.
    """
    statement = (
        select(Estudiante)
        .where(Estudiante.id == estudiante_id)
        .options(selectinload(Estudiante.matriculas))
    )
    estudiante = session.exec(statement).first()
    
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.get("/cedula/{estudiante_cedula}", response_model=Estudiante, summary="Buscar estudiante por cédula")
def obtener_estudiante_por_cedula(estudiante_cedula: str, session: Session = Depends(get_session)):
    """
    Busca un estudiante utilizando su cédula (ID único).
    - Retorna 404 Not Found si la cédula no existe.
    """
    estudiante = session.exec(select(Estudiante).where(Estudiante.cedula == estudiante_cedula)).first()
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return estudiante


@router.post("/", response_model=Estudiante, status_code=201, summary="Crear un nuevo estudiante")
def crear_estudiante(estudiante: EstudianteCreate, session: Session = Depends(get_session)):
    """
    Crea un nuevo estudiante en la base de datos. 
    Verifica que la cédula y el correo sean únicos (Lógica de Negocio).
    - Retorna 409 Conflict si la cédula o correo ya están registrados.
    """

    correo_existente = session.exec(select(Estudiante).where(Estudiante.correo == estudiante.correo)).first()
    if correo_existente:
        raise HTTPException(status_code=409, detail=f"El correo '{estudiante.correo}' ya está registrado.")
    cedula_existente = session.exec(select(Estudiante).where(Estudiante.cedula == estudiante.cedula)).first()
    if cedula_existente:
        raise HTTPException(status_code=409, detail=f"La cédula '{estudiante.cedula}' ya está registrada.")


    db_estudiante = Estudiante.model_validate(estudiante)
    session.add(db_estudiante)
    session.commit()
    session.refresh(db_estudiante)
    return db_estudiante


@router.delete("/{estudiante_id}", summary="Eliminar estudiante FÍSICAMENTE (Activa Cascada)")
def eliminar_estudiante(estudiante_id: int, session: Session = Depends(get_session)):
    """
    Elimina físicamente al estudiante de la base de datos.
    LÓGICA DE NEGOCIO: La eliminación activa la cascada en models.py, 
    eliminando automáticamente sus matrículas y historial asociados.
    - Retorna 404 Not Found si el ID no existe.
    """
    estudiante = session.get(Estudiante, estudiante_id)
    if not estudiante:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
   
    session.delete(estudiante)
    session.commit()
    return {"mensaje": f"Estudiante {estudiante_id} y sus matrículas/historial asociados han sido eliminados."}


@router.put("/{estudiante_id}", response_model=Estudiante, summary="Actualizar estudiante completo")
def actualizar_estudiante(estudiante_id: int, estudiante_actualizado: EstudianteCreate, session: Session = Depends(get_session)):
    """
    Actualiza completamente un registro de estudiante.
    - Retorna 404 Not Found si el ID no existe.
    """
    estudiante_db = session.get(Estudiante, estudiante_id)
    if not estudiante_db:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    estudiante_db.nombre = estudiante_actualizado.nombre
    estudiante_db.cedula = estudiante_actualizado.cedula
    estudiante_db.correo = estudiante_actualizado.correo
    estudiante_db.semestre = estudiante_actualizado.semestre

    session.add(estudiante_db)
    session.commit()
    session.refresh(estudiante_db)
    return estudiante_db