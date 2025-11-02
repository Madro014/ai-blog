# AI Blog Project - Backend

Este repositorio contiene el código del backend para el proyecto AI Blog, una aplicación que permite la gestión de usuarios, autenticación, y la creación y publicación de posts generados con inteligencia artificial.

## Tecnologías Utilizadas

*   **FastAPI:** Framework web para construir APIs con Python.
*   **Uvicorn:** Servidor ASGI para ejecutar aplicaciones FastAPI.
*   **Pydantic:** Para la validación de datos y la definición de esquemas.
*   **SQLAlchemy:** ORM para interactuar con la base de datos.
*   **PostgreSQL:** Base de datos relacional.
*   **Passlib:** Para el hashing seguro de contraseñas (utilizando Argon2).
*   **Google Generative AI:** Para la generación de contenido de los posts.
*   **python-multipart:** Para el manejo de datos de formularios.
*   **python-jose:** Para la implementación de JSON Web Tokens (JWT).
*   **anyio:** Biblioteca de E/S asíncrona.

## Configuración del Entorno

### 1. Clonar el Repositorio

```bash
git clone <(https://github.com/Madro014/ai-blog)>
cd ai-blog-project/backend
```

### 2. Crear y Activar un Entorno Virtual

Es altamente recomendable usar un entorno virtual para gestionar las dependencias del proyecto.

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\activate

# Activar entorno virtual (macOS/Linux)
source venv/bin/activate
```

### 3. Instalar Dependencias

Instala todas las dependencias necesarias utilizando `pip`:

```bash
pip install -r requirements.txt
```

### 4. Configuración de Variables de Entorno

El backend requiere las siguientes variables de entorno para funcionar correctamente. Puedes crearlas en un archivo `.env` en la raíz del directorio `backend` (asegúrate de que `.env` esté en tu `.gitignore`):

*   `DATABASE_URL`: URL de conexión a tu base de datos PostgreSQL (ej. `postgresql://user:password@host:port/dbname`).
*   `SECRET_KEY`: Una clave secreta fuerte para la seguridad de los tokens JWT.
*   `ALGORITHM`: Algoritmo de hashing para JWT (ej. `HS256`).
*   `ACCESS_TOKEN_EXPIRE_MINUTES`: Tiempo de expiración de los tokens de acceso en minutos.
*   `GOOGLE_API_KEY`: Tu clave de API para acceder a los servicios de Google Generative AI.
*   `CORS_ORIGINS`: Orígenes permitidos para CORS (ej. `https://aiblogmad.netlify.app,http://localhost:3000`).

Ejemplo de `.env`:
DATABASE_URL="postgresql://usuario:contraseña@host:puerto/nombre_base_datos"
GEMINI_API_KEY= "tu api key"

### 5. Ejecutar el Servidor Backend

Una vez que las dependencias estén instaladas y las variables de entorno configuradas, puedes iniciar el servidor Uvicorn:

```bash
uvicorn main:app --reload
```

Esto iniciará el servidor en `http://127.0.0.1:8000` (o el puerto que configures) y se recargará automáticamente con los cambios en el código.

## Estructura del Proyecto

*   `main.py`: Punto de entrada de la aplicación FastAPI, define las rutas principales.
*   `auth.py`: Contiene la lógica de autenticación, incluyendo el hashing de contraseñas y la gestión de JWT.
*   `database.py`: Configuración de la base de datos y modelos de SQLAlchemy.
*   `schemas.py`: Define los modelos de datos (Pydantic) para las solicitudes y respuestas de la API.
*   `ai.py`: Lógica para la interacción con la API de Google Generative AI.
*   `requirements.txt`: Lista de dependencias del proyecto.
*   `Dockerfile`: Para la contenerización de la aplicación.

## Endpoints de la API (Ejemplos)

*   `POST /register`: Registro de nuevos usuarios.
*   `POST /token`: Obtención de tokens de acceso (login).
*   `GET /posts`: Obtener todos los posts públicos.
*   `POST /posts`: Crear un nuevo post (requiere autenticación).
*   `GET /posts/{post_id}`: Obtener un post específico.
*   `PUT /posts/{post_id}`: Actualizar un post (requiere autenticación y ser el autor).
*   `DELETE /posts/{post_id}`: Eliminar un post (requiere autenticación y ser el autor).
*   `POST /generate-post`: Generar contenido de post con IA (requiere autenticación).

## Despliegue

Este backend está diseñado para ser desplegado en plataformas como Render, que soporta aplicaciones Python y bases de datos PostgreSQL. Asegúrate de configurar las variables de entorno en tu proveedor de despliegue.

---
