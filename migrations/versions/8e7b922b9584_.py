"""empty message

Revision ID: 8e7b922b9584
Revises: ff80cb1a56bf
Create Date: 2024-07-15 21:54:42.428046

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e7b922b9584'
down_revision = 'ff80cb1a56bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aluno',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('turma_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['turma_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('atividade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=False),
    sa.Column('turma_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['turma_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('atividade')
    op.drop_table('aluno')
    # ### end Alembic commands ###
