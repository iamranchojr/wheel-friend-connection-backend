"""Added is_superuser field to User model

Revision ID: 8694fdac2847
Revises: cbb2b9462d12
Create Date: 2024-07-03 18:57:41.564139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8694fdac2847'
down_revision: Union[str, None] = 'cbb2b9462d12'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'user',
        sa.Column(
            'is_superuser',
            sa.Boolean(),
            nullable=False,
            default=False,
            server_default=sa.false(),
        )
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_superuser')
    # ### end Alembic commands ###