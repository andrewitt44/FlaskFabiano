"""empty message

Revision ID: 8581580a5e09
Revises: e6a50f4a6da7
Create Date: 2024-11-07 09:15:17.673440

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8581580a5e09'
down_revision = 'e6a50f4a6da7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('turma', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagem', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('turma', schema=None) as batch_op:
        batch_op.drop_column('imagem')

    # ### end Alembic commands ###