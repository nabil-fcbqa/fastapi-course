"""add foreign key to posts table

Revision ID: 6ceca38d28b3
Revises: 4f7455e7f7cb
Create Date: 2025-11-03 13:54:03.224208

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6ceca38d28b3"
down_revision: Union[str, Sequence[str], None] = "4f7455e7f7cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "posts_users_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE"
    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
    pass
