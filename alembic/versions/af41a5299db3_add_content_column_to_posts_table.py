"""add content column to posts table

Revision ID: af41a5299db3
Revises: 941e700b8819
Create Date: 2025-11-03 13:38:51.981306

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "af41a5299db3"
down_revision: Union[str, Sequence[str], None] = "941e700b8819"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("posts", "content")
    pass
