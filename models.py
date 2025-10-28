from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
# NUEVA IMPORTACIÓN REQUERIDA
from sqlalchemy import UniqueConstraint 


class MatriculaProfesorLink(SQLModel, table=True):
    matricula_id: Optional[int] = Field(default=None, foreign_key="matricula.id", primary_key=True)
    profesor_id: Optional[int] = Field(default=None, foreign_key="profesor.id", primary_key=True)


class EstudianteBase(SQLModel):
    nombre: Optional[str] = None
    # CORRECCIÓN: Agregar unique=True al teléfono (usado como cédula) y correo.
    telefono: Optional[str] = Field(default=None, unique=True)
    correo: Optional[str] = Field(default=None, unique=True) 

class Estudiante(EstudianteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    active: bool = Field(default=True)
    
    # RELACIÓN: Ya estaba bien, permite cargar las matrículas
    matriculas: List["Matricula"] = Relationship(back_populates="estudiante") 
    historial: Optional["Historial"] = Relationship(back_populates="estudiante", sa_relationship_kwargs={"uselist": False})

class EstudianteCreate(EstudianteBase):
    pass


class MateriaBase(SQLModel):
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    # CORRECCIÓN: Agregar unique=True al código de curso
    codigo: Optional[str] = Field(default=None, unique=True) 

class Materia(MateriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    active: bool = Field(default=True)
    
    matriculas: List["Matricula"] = Relationship(back_populates="materia")
    profesores: List["Profesor"] = Relationship(back_populates="materias", link_model=MatriculaProfesorLink)

class MateriaCreate(MateriaBase):
    pass


class HistorialBase(SQLModel):
    puntaje_icfes: Optional[float] = None
    
class Historial(HistorialBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: Optional[int] = Field(default=None, foreign_key="estudiante.id", nullable=True)
    
    estudiante: Optional[Estudiante] = Relationship(back_populates="historial")

class HistorialCreate(HistorialBase):
    estudiante_id: int


class ProfesorBase(SQLModel):
    nombre: Optional[str] = None
    especialidad: Optional[str] = None

class Profesor(ProfesorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    active: bool = Field(default=True)
    
    matriculas: List["Matricula"] = Relationship(back_populates="profesores", link_model=MatriculaProfesorLink)

class ProfesorCreate(ProfesorBase):
    pass


class MatriculaBase(SQLModel):
    nota_final: Optional[float] = None
    fecha_registro: Optional[date] = Field(default_factory=date.today)
    
class Matricula(MatriculaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    active: bool = Field(default=True)
    
    estudiante_id: Optional[int] = Field(default=None, foreign_key="estudiante.id", nullable=True)
    materia_id: Optional[int] = Field(default=None, foreign_key="materia.id", nullable=True)
    
    # CORRECCIÓN: Restricción Única Compuesta para Matrícula Única
    __table_args__ = (UniqueConstraint("estudiante_id", "materia_id"),) 

    estudiante: Optional[Estudiante] = Relationship(back_populates="matriculas")
    materia: Optional[Materia] = Relationship(back_populates="matriculas")
    profesores: List[Profesor] = Relationship(back_populates="matriculas", link_model=MatriculaProfesorLink)

class MatriculaCreate(MatriculaBase):
    estudiante_id: int
    materia_id: int
    profesor_ids: List[int] = [] # Para asociar profesores al matricular