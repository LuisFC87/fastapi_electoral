-- =====================================
-- INITIAL MIGRATION (ac4bc42cddef)
-- VALIDADO PARA EJECUTAR DE UNA SOLA VEZ
-- =====================================

-- =============================
-- GEOGRAFÍA ELECTORAL
-- =============================

CREATE TABLE pais (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE departamento (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL,
    pais_id INTEGER NOT NULL REFERENCES pais(id)
);

CREATE TABLE provincia (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL,
    departamento_id INTEGER NOT NULL REFERENCES departamento(id)
);

CREATE TABLE municipio (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL,
    provincia_id INTEGER NOT NULL REFERENCES provincia(id)
);

CREATE TABLE localidad (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL,
    municipio_id INTEGER NOT NULL REFERENCES municipio(id)
);

CREATE TABLE recintos (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL,
    localidad_id INTEGER NOT NULL REFERENCES localidad(id)
);

CREATE TABLE mesas (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    numero INTEGER NOT NULL,
    habilitada BOOLEAN,
    recinto_id INTEGER NOT NULL REFERENCES recintos(id),
    CONSTRAINT uq_recinto_numero UNIQUE(recinto_id, numero)
);

-- =============================
-- ORGANIZACIÓN ELECTORAL
-- =============================

CREATE TABLE partidos (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL UNIQUE,
    sigla VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE cargos (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT
);

CREATE TABLE procesos (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombre VARCHAR(255) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    estado VARCHAR(50) NOT NULL
);

CREATE TABLE candidatos (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    nombres VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    partido_id INTEGER REFERENCES partidos(id),
    cargo_id INTEGER REFERENCES cargos(id)
);

CREATE TABLE elecciones (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    proceso_id INTEGER NOT NULL REFERENCES procesos(id),
    cargo_id INTEGER NOT NULL REFERENCES cargos(id),
    descripcion TEXT,
    fecha DATE
);

-- =============================
-- SEGURIDAD
-- =============================

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    uuid UUID NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN
);

CREATE TABLE user_roles (
    user_id INTEGER NOT NULL REFERENCES users(id),
    role_id INTEGER NOT NULL REFERENCES roles(id),
    PRIMARY KEY (user_id, role_id)
);
