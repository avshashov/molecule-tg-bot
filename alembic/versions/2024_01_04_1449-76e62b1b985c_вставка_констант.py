"""вставка констант

Revision ID: 76e62b1b985c
Revises: c293b5756e35
Create Date: 2024-01-04 14:49:25.398087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '76e62b1b985c'
down_revision: Union[str, None] = 'c293b5756e35'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        '''INSERT INTO media_block (id, block) VALUES (1, 'rent'), (2, 'picture'), (3, 'about project')'''
    )
    op.execute(
        '''INSERT INTO media_type (id, type) VALUES (1, 'photo'), (2, 'presentation'), (3, 'video')'''
    )


def downgrade() -> None:
    op.execute(
        '''DELETE FROM media_block WHERE id in (1, 2, 3)'''
    )
    op.execute(
        '''DELETE FROM media_type WHERE id in (1, 2, 3)'''
    )
