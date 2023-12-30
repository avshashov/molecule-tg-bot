"""добавлены внешние таблицы к Media

Revision ID: 19ec8dcec622
Revises: 630fdb6b0963
Create Date: 2023-12-30 14:10:24.572486

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19ec8dcec622'
down_revision: Union[str, None] = '630fdb6b0963'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_block',
    sa.Column('block', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('media_type',
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media_type')
    op.drop_table('media_block')
    # ### end Alembic commands ###
