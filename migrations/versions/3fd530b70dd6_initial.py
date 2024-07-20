"""initial

Revision ID: 3fd530b70dd6
Revises: 
Create Date: 2024-07-20 06:53:38.855425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '3fd530b70dd6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('apps',
                    sa.Column('uuid', sa.UUID(), nullable=False),
                    sa.Column('kind', sa.String(length=32), nullable=False),
                    sa.Column('name', sa.String(length=128), nullable=False),
                    sa.Column('version', sa.String(), nullable=False),
                    sa.Column('description', sa.String(length=4096), nullable=True),
                    sa.Column('state', sa.Enum('NEW', 'INSTALLING', 'RUNNING', name='state'), nullable=True),
                    sa.Column('json', sa.JSON(), nullable=False),
                    sa.PrimaryKeyConstraint('uuid')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('apps')
    # ### end Alembic commands ###
