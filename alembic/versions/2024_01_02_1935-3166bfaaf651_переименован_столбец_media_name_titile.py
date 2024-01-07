"""переименован столбец media_name -> title

Revision ID: 3166bfaaf651
Revises: 0f90a65e8d1e
Create Date: 2024-01-02 19:35:37.659413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3166bfaaf651'
down_revision: Union[str, None] = '0f90a65e8d1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media') as batch_op:
        batch_op.alter_column(column_name='media_name', new_column_name='title')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('media') as batch_op:
        batch_op.alter_column(column_name='title', new_column_name='media_name')
    # ### end Alembic commands ###
