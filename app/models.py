from app import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=True)
    sobrenome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    senha = db.Column(db.String, nullable=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    comentarios = db.relationship('Comentario', backref='author', lazy=True)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    assunto = db.Column(db.String, nullable=True)
    mensagem = db.Column(db.String, nullable=True)
    respondido = db.Column(db.Integer, default=0)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    mensagem = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    comentarios = db.relationship('Comentario', backref='post', lazy=True, cascade="all, delete-orphan")

    def msg_resumo(self):
        return f"{self.mensagem[:10]} ..."

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    data = db.Column(db.DateTime, default=datetime.now())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    turma = db.relationship('Post', back_populates='alunos')

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=True)
    turma = db.relationship('Post', back_populates='atividades')

Post.alunos = db.relationship('Aluno', back_populates='turma', cascade='all, delete-orphan')
Post.atividades = db.relationship('Atividade', back_populates='turma', cascade='all, delete-orphan')

