FastAPI Electoral Project - v2

Es un sistema de gestión electoral basado en FastAPI. Utiliza un stack de Python moderno y asíncrono.

Tecnologías Clave:

Framework: FastAPI
Base de Datos: PostgreSQL (con asyncpg)
ORM: SQLAlchemy (asíncrono)
Migraciones: Alembic
Validación: Pydantic
Arquitectura:

Modular: Separado en un core para componentes compartidos y modules para la lógica de negocio.
Enrutamiento Dinámico: Descubre e incluye automáticamente los endpoints de los módulos.
Inyección de Dependencias: Usado extensivamente para servicios y sesiones de base de datos.
Módulos Principales:

seguridad:
Autenticación de usuarios con JWT.
Gestión de usuarios y roles con control de acceso (RBAC).
elecciones_organizacion:
geografia_electoral: Gestiona la jerarquía geográfica electoral (países, recintos, mesas, etc.).
organizacion_electoral: Gestiona las entidades políticas (partidos, candidatos, elecciones, etc.).