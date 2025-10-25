from typing import Optional, List
from datetime import date
from sqlmodel import SQLModel, Field, Relationship


class MatriculaProfesorLink(SQLModel, table=True):
    matricula_id: Optional[int] = Field(default=None, foreign_key="matricula.id", primary_key=True)
    profesor_id: Optional[int] = Field(default=None, foreign_key="profesor.id", primary_key=True)


class EstudianteBase(SQLModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[str] = None

class Estudiante(EstudianteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    active: bool = Field(default=True)
    matriculas: List["Matricula"] = Relationship(back_populates="estudiante")
    historial: Optional["Historial"] = Relationship(back_populates="estudiante", sa_relationship_kwargs={"uselist": False})

class EstudianteCreate(EstudianteBase):
    pass


class MateriaBase(SQLModel):
    nombre: Optional[str] = None
    creditos: Optional[int] = None
    codigo: Optional[str] = None

class Materia(MateriaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    active: bool = Field(default=True)
    
    matriculas: List["Matricula"] = Relationship(back_populates="materia")

class MateriaCreate(MateriaBase):
    pass


class HistorialBase(SQLModel):
    numero: Optional[str] = None
    fecha_emision: Optional[date] = None

class Historial(HistorialBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estudiante_id: Optional[int] = Field(default=None, foreign_key="estudiante.id", unique=True, nullable=True)
    
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
    
    estudiante: Optional[Estudiante] = Relationship(back_populates="matriculas")
    materia: Optional[Materia] = Relationship(back_populates="matriculas")
    
    profesores: List[Profesor] = Relationship(back_populates="matriculas", link_model=MatriculaProfesorLink)

class MatriculaCreate(MatriculaBase):
    estudiante_id: int
    materia_id: int
    profesor_ids: Optional[List[int]] = []