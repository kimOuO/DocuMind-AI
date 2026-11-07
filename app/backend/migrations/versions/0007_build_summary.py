"""Per-document choice of building the summary tree (D91).

Revision ID: 0007
Revises: 0006
Create Date: 2026-11-08 02:40:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0007'
down_revision: Union[str, Sequence[str], None] = '0006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

STATUSES_BEFORE = "'none', 'processing', 'ready', 'failed'"
STATUSES_AFTER = STATUSES_BEFORE + ", 'skipped'"


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'documents',
        sa.Column('build_summary', sa.Boolean(), server_default=sa.text('true'), nullable=False),
    )
    op.drop_constraint('ck_documents_summary_status', 'documents', type_='check')
    op.create_check_constraint(
        'ck_documents_summary_status', 'documents', f'summary_status IN ({STATUSES_AFTER})'
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("UPDATE documents SET summary_status = 'none' WHERE summary_status = 'skipped'")
    op.drop_constraint('ck_documents_summary_status', 'documents', type_='check')
    op.create_check_constraint(
        'ck_documents_summary_status', 'documents', f'summary_status IN ({STATUSES_BEFORE})'
    )
    op.drop_column('documents', 'build_summary')
