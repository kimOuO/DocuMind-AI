"""One vector per block of a multi-block table chunk (D82).

Revision ID: 0006
Revises: 0005
Create Date: 2026-11-07 14:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy

# revision identifiers, used by Alembic.
revision: str = '0006'
down_revision: Union[str, Sequence[str], None] = '0005'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'chunk_vectors',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('chunk_id', sa.Uuid(), nullable=False),
        sa.Column('ordinal', sa.Integer(), nullable=False),
        sa.Column('embedding', pgvector.sqlalchemy.vector.VECTOR(dim=1024), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['chunk_id'], ['chunks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('chunk_id', 'ordinal', name='uq_chunk_vectors_chunk_ordinal'),
    )
    op.create_index(
        'ix_chunk_vectors_embedding_hnsw', 'chunk_vectors', ['embedding'], unique=False,
        postgresql_using='hnsw', postgresql_ops={'embedding': 'vector_cosine_ops'},
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        'ix_chunk_vectors_embedding_hnsw', table_name='chunk_vectors',
        postgresql_using='hnsw', postgresql_ops={'embedding': 'vector_cosine_ops'},
    )
    op.drop_table('chunk_vectors')
