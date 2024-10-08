"""empty message

Revision ID: e6a50f4a6da7
Revises: 
Create Date: 2024-08-20 16:00:08.408083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6a50f4a6da7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contato',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_envio', sa.DateTime(), nullable=True),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('assunto', sa.String(), nullable=True),
    sa.Column('mensagem', sa.String(), nullable=True),
    sa.Column('respondido', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('sobrenome', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('senha', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('turma',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('nome', sa.String(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('aluno',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('maquina', sa.String(), nullable=False),
    sa.Column('turma_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['turma_id'], ['turma.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('atividade',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=False),
    sa.Column('turma_id', sa.Integer(), nullable=True),
    sa.Column('atividade_numero', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['turma_id'], ['turma.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comentario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('data', sa.DateTime(), nullable=True),
    sa.Column('turma_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['turma_id'], ['turma.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('maquina',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('descricao', sa.String(), nullable=True),
    sa.Column('data_criacao', sa.DateTime(), nullable=True),
    sa.Column('turma_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['turma_id'], ['turma.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('maquina')
    op.drop_table('comentario')
    op.drop_table('atividade')
    op.drop_table('aluno')
    op.drop_table('turma')
    op.drop_table('user')
    op.drop_table('contato')
    # ### end Alembic commands ###
