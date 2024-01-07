"""убрано ограничение длины для Media.title

Revision ID: a5c737358754
Revises: fc771ac0cd66
Create Date: 2024-01-04 00:11:49.673082

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5c737358754'
down_revision: Union[str, None] = 'fc771ac0cd66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media', 'title',
                    existing_type=sa.String(length=15),
                    type_=sa.String(),
                    existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('media', 'title',
                    existing_type=sa.String(),
                    type_=sa.String(length=15),
                    existing_nullable=False)
    # ### end Alembic commands ###
