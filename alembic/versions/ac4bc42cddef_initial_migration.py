"""initial migration

Revision ID: ac4bc42cddef
Revises:
Create Date: 2025-11-13 15:54:18.839999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ac4bc42cddef'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create tables for geografia_electoral
    op.create_table('pais',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre')
    )
    op.create_table('departamento',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('pais_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['pais_id'], ['pais.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provincia',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('departamento_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['departamento_id'], ['departamento.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('municipio',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('provincia_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['provincia_id'], ['provincia.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('localidad',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('municipio_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['municipio_id'], ['municipio.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recintos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('localidad_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['localidad_id'], ['localidad.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('mesas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('numero', sa.Integer(), nullable=False),
        sa.Column('habilitada', sa.Boolean(), nullable=True),
        sa.Column('recinto_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['recinto_id'], ['recintos.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('recinto_id', 'numero', name='uq_recinto_numero')
    )

    # Create tables for organizacion_electoral
    op.create_table('partidos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('sigla', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nombre'),
        sa.UniqueConstraint('sigla')
    )
    op.create_table('cargos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('procesos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombre', sa.String(length=255), nullable=False),
        sa.Column('fecha_inicio', sa.Date(), nullable=False),
        sa.Column('fecha_fin', sa.Date(), nullable=False),
        sa.Column('tipo', sa.String(length=50), nullable=False),
        sa.Column('estado', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('candidatos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('nombres', sa.String(length=255), nullable=False),
        sa.Column('apellidos', sa.String(length=255), nullable=False),
        sa.Column('partido_id', sa.Integer(), nullable=True),
        sa.Column('cargo_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['cargo_id'], ['cargos.id'], ),
        sa.ForeignKeyConstraint(['partido_id'], ['partidos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('elecciones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('proceso_id', sa.Integer(), nullable=False),
        sa.Column('cargo_id', sa.Integer(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('fecha', sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(['cargo_id'], ['cargos.id'], ),
        sa.ForeignKeyConstraint(['proceso_id'], ['procesos.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create tables for seguridad
    op.create_table('roles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('username', sa.String(length=150), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )
    op.create_table('user_roles',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('role_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('user_roles')
    op.drop_table('users')
    op.drop_table('roles')
    op.drop_table('elecciones')
    op.drop_table('candidatos')
    op.drop_table('procesos')
    op.drop_table('cargos')
    op.drop_table('partidos')
    op.drop_table('mesas')
    op.drop_table('recintos')
    op.drop_table('localidad')
    op.drop_table('municipio')
    op.drop_table('provincia')
    op.drop_table('departamento')
    op.drop_table('pais')
