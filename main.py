from fastapi import FastAPI
from db import create_db_and_tables
from estudiante import router as estudiante_router
from materia import router as materia_router
from profesor import router as profesor_router
from matricula import router as matricula_router
from historial import router as historial_router
from reporte import router as reportes_router


app = FastAPI(title="Universidad API: Sistema de Matrículas") # Título actualizado

@app.on_event("startup")
def on_startup():
    create_db_and_tables(app)

app.include_router(estudiante_router, prefix="/estudiantes", tags=["Estudiantes"])
app.include_router(materia_router, prefix="/materias", tags=["Materias"])
app.include_router(profesor_router, prefix="/profesores", tags=["Profesores"])
app.include_router(historial_router, prefix="/historiales", tags=["Historial Académico"])
app.include_router(matricula_router, prefix="/matriculas", tags=["Matrículas"])
app.include_router(reportes_router) # Mantenemos esta, el reporte necesita una revisión aparte

@app.get("/")
def root():
    return {"message": "Universidad API - ¡Sistema de Matrículas funcionando!"}