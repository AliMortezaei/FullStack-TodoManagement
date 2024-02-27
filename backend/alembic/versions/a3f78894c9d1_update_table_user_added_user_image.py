"""update table user added user image

Revision ID: a3f78894c9d1
Revises: 0094ad012e81
Create Date: 2024-02-27 16:09:48.742794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'a3f78894c9d1'
down_revision: Union[str, None] = '0094ad012e81'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('image', sa.LargeBinary(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'image')
    # ### end Alembic commands ###