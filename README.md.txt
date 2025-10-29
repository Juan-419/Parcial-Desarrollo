# Sistema de Gestión de Universidad (API RESTful)

Este proyecto implementa una API RESTful para la gestión de estudiantes, materias y matrículas de una universidad, utilizando **FastAPI** y **SQLModel**.

## ⚙️ Tecnologías Utilizadas

* **Backend Framework:** FastAPI
* **ORM / Base de Datos:** SQLModel (SQLite por defecto)
* **Servidor ASGI:** Uvicorn
* **Generación de Reportes:** ReportLab

## 📋 Requisitos Previos

Necesitas tener **Python 3.10+** instalado en tu sistema (Compatible con Python 3.13).

## 💾 Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone [TU URL DE GITHUB]
    cd [NOMBRE DEL REPOSITORIO]
    ```

2.  **Crear y activar el entorno virtual (Recomendado):**
    ```bash
    python -m venv venv
    # En Windows:
    .\venv\Scripts\activate
    # En Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Instala todas las librerías necesarias utilizando el archivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

## 🚀 Ejecución del Proyecto

1.  **Iniciar la aplicación:**
    Ejecuta el servidor Uvicorn desde la carpeta raíz:
    ```bash
    uvicorn main:app --reload
    ```
    La opción `--reload` permite que el servidor se reinicie automáticamente al detectar cambios en el código.

2.  **Acceder a la Documentación (Swagger UI):**
    Una vez que el servidor esté corriendo, puedes acceder a la documentación interactiva de la API en tu navegador:
    
    * **URL:** `http://127.0.0.1:8000/docs`

    Aquí podrás probar todos los *endpoints* CRUD (GET, POST, PUT, DELETE) para `Estudiantes`, `Materias`, `Matrículas`, `Profesores` e `Historiales`.