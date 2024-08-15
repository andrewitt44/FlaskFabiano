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
    turmas = db.relationship('Turma', backref='author', lazy=True)
    comentarios = db.relationship('Comentario', backref='author', lazy=True)

class Contato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_envio = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    assunto = db.Column(db.String, nullable=True)
    mensagem = db.Column(db.String, nullable=True)
    respondido = db.Column(db.Integer, default=0)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    nome = db.Column(db.String, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    comentarios = db.relationship('Comentario', backref='turma', lazy=True, cascade="all, delete-orphan")
    alunos = db.relationship('Aluno', back_populates='turma', cascade='all, delete-orphan')
    atividades = db.relationship('Atividade', back_populates='turma', cascade='all, delete-orphan')

    @staticmethod
    def realinhar_ids():
        turmas = Turma.query.order_by(Turma.id).all()
        for idx, turma in enumerate(turmas, start=1):
            turma.id = idx
            db.session.add(turma)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        Turma.realinhar_ids()

class Comentario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    data = db.Column(db.DateTime, default=datetime.now())
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=True)
    turma = db.relationship('Turma', back_populates='alunos')

class Atividade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String, nullable=False)
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=True)
    turma = db.relationship('Turma', back_populates='atividades')
    atividade_numero = db.Column(db.Integer, nullable=False)

    def __init__(self, descricao, turma_id):
        self.descricao = descricao
        self.turma_id = turma_id
        max_numero = Atividade.query.filter_by(turma_id=turma_id).count()
        self.atividade_numero = max_numero + 1

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def realinhar_ids(turma_id):
        atividades = Atividade.query.filter_by(turma_id=turma_id).order_by(Atividade.atividade_numero).all()
        for idx, atividade in enumerate(atividades, start=1):
            atividade.atividade_numero = idx
            db.session.add(atividade)
        db.session.commit()

    def delete(self):
        turma_id = self.turma_id
        db.session.delete(self)
        db.session.commit()
        Atividade.realinhar_ids(turma_id)

class Maquina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, nullable=False)
    descricao = db.Column(db.String, nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.now())
    turma_id = db.Column(db.Integer, db.ForeignKey('turma.id'), nullable=True)
    
    @staticmethod
    def realinhar_ids():
        maquinas = Maquina.query.order_by(Maquina.id).all()
        for idx, maquina in enumerate(maquinas, start=1):
            maquina.id = idx
            db.session.add(maquina)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        Maquina.realinhar_ids()
