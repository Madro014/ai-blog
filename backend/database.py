from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")

# Verificar que la URL de la base de datos esté configurada
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no está configurada en el archivo .env")

# Crear el motor de la base de datos
# El argumento 'pool_pre_ping=True' ayuda a mantener las conexiones activas
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Configurar la sesión de la base de datos
# autocommit=False: No se confirman los cambios automáticamente
# autoflush=False: No se vacían los cambios automáticamente
# bind=engine: Asocia la sesión con el motor de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa para los modelos de SQLAlchemy
Base = declarative_base()

# Función de utilidad para obtener una sesión de base de datos
# Esta función se usará como una dependencia en FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Ejemplo de modelo de SQLAlchemy: Tabla de Usuarios
# Puedes definir tus propias tablas aquí siguiendo este patrón
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)  # Especificar longitud
    hashed_password = Column(String(255), nullable=False)  # Especificar longitud

    posts = relationship("Post", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


# Nuevo modelo para la tabla 'posts'
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)  # Especificar longitud
    content = Column(Text)  # Text para contenido más largo
    created_at = Column(DateTime, default=datetime.now)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_public = Column(Boolean, default=False)  # Boolean con valor por defecto
    author_name = Column(String(100), default="")  # CORREGIDO: Valor por defecto string vacío en lugar de nullable=True

    owner = relationship("User", back_populates="posts")

    def __repr__(self):
        return f"<Post(id={self.id}, title='{self.title}', owner_id={self.owner_id}, is_public={self.is_public})>"

# Opcional: Función para crear todas las tablas definidas en la base de datos
# Deberías llamar a esta función una vez al inicio de tu aplicación
# (por ejemplo, en main.py o en un script de inicialización)
def create_db_tables():
    Base.metadata.create_all(bind=engine)