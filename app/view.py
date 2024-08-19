from app import app, db
from flask import render_template, url_for, request, redirect, flash, session
from app.forms import ComentarioForm, UserForm, LoginForm, TurmaForm, EditTurmaForm, EditAtividadeForm, MaquinaForm, EditMaquinaForm, AlunoForm, EditAlunoForm
from app.models import Comentario, Turma, Atividade, Maquina, Aluno
from flask_login import login_user, logout_user, current_user
import os

@app.before_request
def before_request():
    if 'app_initiated' not in session:
        session['app_initiated'] = True
        if current_user.is_authenticated:
            logout_user()
        return redirect(url_for('homepage'))

@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = LoginForm()

    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)
        return redirect(url_for('homepage')) 

    return render_template('Codes/index.html', form=form)

@app.route('/cadastro/', methods=['GET', 'POST'])
def cadastro():
    form = UserForm()
    if form.validate_on_submit():
        user = form.save()
        flash('Cadastro realizado com sucesso! Por favor, faça o login para continuar.')
        return redirect(url_for('homepage'))
    return render_template('Codes/cadastro.html', form=form)

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
    return render_template('Turma/turma_novo.html', form=form)

@app.route('/turma/lista')
def TurmaLista():
    turmas = Turma.query.all()
    return render_template('Turma/turma_lista.html', turmas=turmas)

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
    return render_template('Turma/turma_detail.html', turma=turma, form=form)

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

    return render_template('Turma/turma_edit.html', form=form, turma=turma)

@app.route('/atividade_edit/<int:id>', methods=['GET', 'POST'])
def atividadeEdit(id):
    atividade = Atividade.query.get_or_404(id)
    form = EditAtividadeForm()
    if form.validate_on_submit():
        form.save(id)
        return redirect(url_for('turmaDetail', id=atividade.turma_id))
    elif request.method == 'GET':
        form.descricao.data = atividade.descricao
    return render_template('Turma/atividade_edit.html', form=form, atividade=atividade)

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

    return render_template('Turma/atividade_novo.html', form=form, turma=turma)

@app.route('/maquinas')
def listar_maquinas():
    maquinas = Maquina.query.all()
    return render_template('Maquina/listar_maquinas.html', maquinas=maquinas)

@app.route('/maquinas/nova', methods=['GET', 'POST'])
def nova_maquina():
    form = MaquinaForm()
    if form.validate_on_submit():
        turma_id = request.args.get('turma_id')
        form.save(turma_id)
        flash('Máquina criada com sucesso!')
        return redirect(url_for('listar_maquinas'))
    return render_template('Maquina/nova_maquina.html', form=form)

@app.route('/maquinas/editar/<int:maquina_id>', methods=['GET', 'POST'])
def editar_maquina(maquina_id):
    maquina = Maquina.query.get_or_404(maquina_id)
    form = EditMaquinaForm(obj=maquina)
    if form.validate_on_submit():
        form.save(maquina_id)
        flash('Máquina atualizada com sucesso!')
        return redirect(url_for('listar_maquinas'))
    return render_template('Maquina/editar_maquina.html', form=form, maquina=maquina)

@app.route('/excluir_maquina/<int:maquina_id>', methods=['POST'])
def excluir_maquina(maquina_id):
    maquina = Maquina.query.get_or_404(maquina_id)
    maquina.delete()
    flash('Máquina excluída com sucesso!')
    return redirect(url_for('listar_maquinas'))

@app.route('/alunos')
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('Aluno/listar_alunos.html', alunos=alunos)

@app.route('/alunos/novo', methods=['GET', 'POST'])
def aluno_novo():
    form = AlunoForm()
    if form.validate_on_submit():
        turma_id = request.args.get('turma_id')
        form.save(turma_id)
        flash('Aluno criado com sucesso!')
        return redirect(url_for('listar_alunos'))
    return render_template('Aluno/aluno_novo.html', form=form)

@app.route('/alunos/editar/<int:aluno_id>', methods=['GET', 'POST'])
def editar_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    form = EditAlunoForm(obj=aluno)
    if form.validate_on_submit():
        form.save(aluno_id)
        flash('Aluno atualizado com sucesso!')
        return redirect(url_for('listar_alunos'))
    return render_template('Aluno/editar_aluno.html', form=form, aluno=aluno)

@app.route('/excluir_aluno/<int:aluno_id>', methods=['POST'])
def excluir_aluno(aluno_id):
    aluno = Aluno.query.get_or_404(aluno_id)
    db.session.delete(aluno)
    db.session.commit()
    flash('Aluno excluído com sucesso!')
    return redirect(url_for('listar_alunos'))
