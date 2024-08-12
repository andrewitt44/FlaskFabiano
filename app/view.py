from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import ComentarioForm, ContatoForm, UserForm, LoginForm, TurmaForm, EditTurmaForm, EditAtividadeForm
from app.models import Comentario, Contato, User, Turma, Atividade
from flask_login import login_user, logout_user, current_user

@app.route('/', methods=['GET', 'POST'])
def homepage():
    usuario = 'Mateus'
    idade = 17
    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)

    context = {
        'usuario': usuario,
        'idade': idade
    }
    return render_template('index.html', context=context, form=form)

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        login_user(user, remember=True)
        return redirect(url_for('homepage'))
    return render_template('cadastro.html', form=form)

@app.route('/sair/')
def logout():
    logout_user()
    return redirect(url_for('homepage'))

@app.route('/turma/novo', methods=['GET', 'POST'])
def TurmaNovo():
    form = TurmaForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('TurmaLista'))
    return render_template('turma_novo.html', form=form)

@app.route('/turma/lista')
def TurmaLista():
    turmas = Turma.query.all()
    return render_template('turma_lista.html', turmas=turmas)

@app.route('/turma/<int:id>', methods=['GET', 'POST'])
def turmaDetail(id):
    turma = Turma.query.get(id)
    form = ComentarioForm()
    if form.validate_on_submit():
        comentario = Comentario(
            text=form.text.data,
            turma_id=id,
            user_id=current_user.id
        )
        db.session.add(comentario)
        db.session.commit()
        return redirect(url_for('turmaDetail', id=id))
    return render_template('turma_detail.html', turma=turma, form=form)

@app.route('/turma/delete/<int:id>', methods=['POST'])
def turmaDelete(id):
    turma = Turma.query.get(id)
    if turma:
        turma.delete()  # Usando o método delete da classe Turma
    return redirect(url_for('TurmaLista'))

@app.route('/turma/edit/<int:id>', methods=['GET', 'POST'])
def turmaEdit(id):
    turma = Turma.query.get(id)
    if not turma:
        return redirect(url_for('TurmaLista'))

    form = EditTurmaForm(obj=turma)
    if form.validate_on_submit():
        form.save(turma_id=id)
        return redirect(url_for('TurmaLista'))

    return render_template('turma_edit.html', form=form, turma=turma)

@app.route('/atividade_edit/<int:id>', methods=['GET', 'POST'])
def atividadeEdit(id):
    atividade = Atividade.query.get_or_404(id)
    form = EditAtividadeForm()
    if form.validate_on_submit():
        form.save(id)
        return redirect(url_for('turmaDetail', id=atividade.turma_id))
    elif request.method == 'GET':
        form.descricao.data = atividade.descricao
    return render_template('atividade_edit.html', form=form, atividade=atividade)

@app.route('/atividade/delete/<int:id>', methods=['POST'])
def atividadeDelete(id):
    atividade = Atividade.query.get(id)
    if atividade:
        atividade.delete()  # Usando o método delete da classe Atividade
        return redirect(url_for('turmaDetail', id=atividade.turma_id))

    return redirect(url_for('TurmaLista'))

@app.route('/atividade/novo/<int:turma_id>', methods=['GET', 'POST'])
def atividade_novo(turma_id):
    turma = Turma.query.get_or_404(turma_id)
    form = EditAtividadeForm()

    if form.validate_on_submit():
        atividade = Atividade(
            descricao=form.descricao.data,
            turma_id=turma_id
        )
        db.session.add(atividade)
        db.session.commit()
        return redirect(url_for('turmaDetail', id=turma_id))

    return render_template('atividade_novo.html', form=form, turma=turma)
