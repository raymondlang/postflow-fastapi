"""add content column to posts table

Revision ID: de907cdfab5c
Revises: bef8d6598a3d
Create Date: 2023-10-06 12:53:00.271441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'de907cdfab5c'
down_revision: Union[str, None] = 'bef8d6598a3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
