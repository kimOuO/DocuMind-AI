"""Section and document summaries built at ingestion time (P3).

Revision ID: 0004
Revises: 0003
Create Date: 2026-11-05 21:30:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0004'
down_revision: Union[str, Sequence[str], None] = '0003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('summaries',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('document_id', sa.UUID(), nullable=False),
    sa.Column('level', sa.Text(), nullable=False),
    sa.Column('ordinal', sa.Integer(), nullable=False),
    sa.Column('title', sa.Text(), nullable=True),
    sa.Column('page_start', sa.Integer(), nullable=False),
    sa.Column('page_end', sa.Integer(), nullable=False),
    sa.Column('source_chunk_ids', postgresql.ARRAY(sa.UUID()), server_default=sa.text("'{}'::uuid[]"), nullable=False),
    sa.Column('source_summary_ids', postgresql.ARRAY(sa.UUID()), server_default=sa.text("'{}'::uuid[]"), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('token_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("level IN ('section', 'document')", name='ck_summaries_level'),
    sa.ForeignKeyConstraint(['document_id'], ['documents.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('document_id', 'level', 'ordinal', name='uq_summaries_document_level_ordinal')
    )
    op.create_index(op.f('ix_summaries_document_id'), 'summaries', ['document_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_summaries_document_id'), table_name='summaries')
    op.drop_table('summaries')
