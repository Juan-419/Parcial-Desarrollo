# 🎓 Universidad API: Sistema de Matrículas

Este repositorio contiene la implementación de una **Web API** para la gestión de estudiantes, materias, matrículas, historial académico y profesores de una universidad.

Desarrollada con **FastAPI** y **SQLModel**, utiliza una base de datos local **SQLite**.

## ⚙️ Tecnologías y Requerimientos

** Python (3.10 o superior): Totalmente compatible con Python 3.13 (versión utilizada para la entrega).

** Framework (FastAPI): Para la creación de los endpoints.

** ORM (SQLModel): Para la interacción con la base de datos (SQLite).

-----

## 🚀 Guía de Instalación y Ejecución

Sigue estos pasos para levantar el proyecto en tu máquina local.

### 1\. Clonar el Repositorio

```bash
git clone https://docs.github.com/es/repositories/creating-and-managing-repositories/quickstart-for-repositories
cd [Nombre de la Carpeta del Proyecto]
```

### 2\. Crear y Activar el Entorno Virtual (`venv`)

Es fundamental trabajar dentro de un entorno virtual para aislar las dependencias.

Windows:

Crear entorno: python -m venv venv
Activar entorno: .\venv\Scripts\activate

Linux/macOS:

Crear entorno: python3 -m venv venv
Activar entorno: source venv/bin/activate

### 3\. Instalar Dependencias

Asegúrate de que tu entorno virtual (`(venv)`) esté **activo** antes de ejecutar:

```bash
pip install -r requirements.txt
```

### 4\. Ejecutar el Servidor Uvicorn

Inicia el servidor de desarrollo usando `uvicorn main:app` desde la carpeta raíz:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: **`http://127.0.0.1:8000`**

### 5\. Acceder a la Documentación (Swagger UI)

Abre la documentación interactiva en tu navegador para probar todos los *endpoints*:

  * **URL:** `http://127.0.0.1:8000/docs`

-----

## 📂 Estructura del Proyecto

El proyecto sigue una estructura modular donde cada archivo se enfoca en una funcionalidad específica:

  * **`main.py`**: Archivo de entrada de la aplicación. Inicializa FastAPI y registra todos los *routers*.
  * **`models.py`**: Contiene todas las clases **SQLModel** (esquemas y tablas), incluyendo las relaciones entre entidades.
  * **`db.py`**: Configuración de la conexión a la base de datos y la función `create_db_and_tables`.
  * **`estudiante.py`**, **`materia.py`**, **`profesor.py`**, etc.: Módulos que implementan los *routers* (`APIRouter`) con la lógica **CRUD** y las reglas de negocio específicas para cada entidad.
  * **`requirements.txt`**: Lista de dependencias del proyecto.


## 👨‍💻 Autor
**Juan David Vega Alfonso** — Estudiante de Ingeniería de Sistemas, Universidad Católica de Colombia.

-----