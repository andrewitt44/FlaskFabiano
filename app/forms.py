from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app import db, bcrypt
from app.models import Contato, User, Turma, Atividade, Aluno

class UserForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    sobrenome = StringField('Sobrenome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    confirmacao_senha = PasswordField('Confimar senha', validators=[DataRequired(), EqualTo('senha')])
    btnSubmit = SubmitField('Cadastrar')

    def validade_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError('Usuário já cadastrado com esse E-mail!!!')

    def save(self):
        senha = bcrypt.generate_password_hash(self.senha.data.encode('utf-8'))
        user = User(
            nome=self.nome.data,
            sobrenome=self.sobrenome.data,
            email=self.email.data,
            senha=senha
        )
        db.session.add(user)
        db.session.commit()
        return user

class ContatoForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    assunto = StringField('Assunto', validators=[DataRequired()])
    mensagem = StringField('Mensagem', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self):
        contato = Contato(
            nome=self.nome.data,
            email=self.email.data,
            assunto=self.assunto.data,
            mensagem=self.mensagem.data
        )
        db.session.add(contato)
        db.session.commit()

class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    btnSubmit = SubmitField('Login')

    def login(self):
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.senha, self.senha.data.encode('utf-8')):
                return user
            else:
                raise Exception('Senha Incorreta!!!')
        else:
            raise Exception('Usuário não encontrado')

class TurmaForm(FlaskForm):
    nome = StringField('Nome da turma', validators=[DataRequired()])
    btnSubmit = SubmitField('Enviar')

    def save(self, user_id):
        turma = Turma(
            nome=self.nome.data,
            user_id=user_id
        )
        db.session.add(turma)
        db.session.commit()

class ComentarioForm(FlaskForm):
    text = TextAreaField('Atividade', validators=[DataRequired()])
    submit = SubmitField('Adicionar atividade')

class EditTurmaForm(FlaskForm):
    nome = StringField('Insira o novo nome da turma', validators=[DataRequired()])
    btnSubmit = SubmitField('Atualizar')

    def save(self, turma_id):
        turma = Turma.query.get(turma_id)
        if turma:
            turma.nome = self.nome.data
            db.session.commit()
        return turma
    
class EditAtividadeForm(FlaskForm):
    descricao = StringField('Nome da atividade', validators=[DataRequired()])
    btnSubmit = SubmitField('Atualizar')

    def save(self, atividade_id):
        atividade = Atividade.query.get(atividade_id)
        if atividade:
            atividade.descricao = self.descricao.data
            db.session.commit()
        return atividade


class AlunoForm(FlaskForm):
    nome = StringField('Nome do Aluno', validators=[DataRequired()])
    btnSubmit = SubmitField('Adicionar Aluno')

    def save(self, turma_id):
        aluno = Aluno(nome=self.nome.data, turma_id=turma_id)
        db.session.add(aluno)
        db.session.commit()

class AtividadeForm(FlaskForm):
    descricao = StringField('Descrição da Atividade', validators=[DataRequired()])
    btnSubmit = SubmitField('Adicionar Atividade')

    def save(self, turma_id):
        atividade = Atividade(descricao=self.descricao.data, turma_id=turma_id)
        db.session.add(atividade)
        db.session.commit()
