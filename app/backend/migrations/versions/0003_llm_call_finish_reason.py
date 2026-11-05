"""Record how each LLM call ended: natural stop, output limit, exhausted
context or a client that disconnected.

Revision ID: 0003
Revises: 0002
Create Date: 2026-11-05 19:40:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '0003'
down_revision: Union[str, Sequence[str], None] = '0002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('llm_calls', sa.Column('finish_reason', sa.Text(), nullable=True))
    op.create_check_constraint(
        'ck_llm_calls_finish_reason',
        'llm_calls',
        "finish_reason IN ('stop', 'output_limit', 'context_exhausted', 'client_disconnect', 'unknown')",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('ck_llm_calls_finish_reason', 'llm_calls', type_='check')
    op.drop_column('llm_calls', 'finish_reason')
