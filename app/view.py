from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import ComentarioForm, ContatoForm, UserForm, LoginForm, PostForm, EditPostForm
from app.models import Comentario, Contato, User, Post
from flask_login import login_user, logout_user, current_user



@app.route('/', methods=['GET','POST'])
def homepage():
    usuario = 'Mateus'
    idade = 17
    form = LoginForm()


    if form.validate_on_submit():
        user = form.login()
        login_user(user, remember=True)


    context = {
        'usuario':usuario,
        'idade':idade
    }
    return render_template('index.html', context=context, form = form)


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


@app.route('/contato/', methods=['GET', 'POST'])
def contato():
    form = ContatoForm()
    context = {}
    if form.validate_on_submit():
        form.save()
        return redirect(url_for('homepage'))
    return render_template('contato.html', context=context, form=form)


@app.route('/contato/lista/')
def contatoLista():
    if request.method == 'GET':
        pesquisa = request.args.get('pesquisa', '')
    dados  = Contato.query.order_by('nome')
    if pesquisa != '':
        dados = dados.filter_by(nome=pesquisa)
    context = {'dados': dados.all()}
    return render_template('contato_lista.html', context=context)
   
@app.route('/contato/<int:id>')
def contatoDetail(id):
    obj = Contato.query.get(id)
    return render_template('contato_detail.html', obj=obj)


@app.route('/post/novo', methods=['GET', 'POST'])
def PostNovo():
    form = PostForm()
    if form.validate_on_submit():
        form.save(current_user.id)
        return redirect(url_for('PostLista'))
    return render_template('post_novo.html', form=form)


@app.route('/post/lista')
def PostLista():
    posts = Post.query.all()
    print(current_user.posts)
    return render_template('post_lista.html', posts=posts)


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def postDetail(id):
    obj = Post.query.get(id)
    turma = Turma.query.filter_by(post_id=id).first()  # Exemplo de busca da turma associada ao post
    form = ComentarioForm()

    if form.validate_on_submit():
        comentario = Comentario(
            text=form.text.data,
            post_id=id,
            user_id=current_user.id
        )
        db.session.add(comentario)
        db.session.commit()
        return redirect(url_for('postDetail', id=id))

    return render_template('post_detail.html', obj=obj, form=form, turma=turma)



@app.route('/post/delete/<int:id>', methods=['POST'])
def postDelete(id):
    post = Post.query.get(id)
    if post:
        db.session.delete(post)
        db.session.commit()
    return redirect(url_for('PostLista'))

@app.route('/post/edit/<int:id>', methods=['GET', 'POST'])
def postEdit(id):
    post = Post.query.get(id)
    if not post:
        return redirect(url_for('PostLista'))

    form = EditPostForm(obj=post)
    if form.validate_on_submit():
        form.save(post_id=id)
        return redirect(url_for('PostLista'))

    return render_template('post_edit.html', form=form, post=post)

@app.route('/turma/<int:id>', methods=['GET', 'POST'])
def turmaDetail(id):
    turma = Post.query.get(id)
    atividade_form = AtividadeForm()
    aluno_form = AlunoForm()

    if atividade_form.validate_on_submit():
        atividade_form.save(turma_id=id)
        return redirect(url_for('turmaDetail', id=id))

    if aluno_form.validate_on_submit():
        aluno_form.save(turma_id=id)
        return redirect(url_for('turmaDetail', id=id))

    return render_template('turma_detail.html', turma=turma, atividade_form=atividade_form, aluno_form=aluno_form)

@app.route('/aluno/delete/<int:id>', methods=['POST'])
def alunoDelete(id):
    aluno = Aluno.query.get(id)
    if aluno:
        db.session.delete(aluno)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/atividade/delete/<int:id>', methods=['POST'])
def atividadeDelete(id):
    atividade = Atividade.query.get(id)
    if atividade:
        db.session.delete(atividade)
        db.session.commit()
    return redirect(request.referrer)

@app.route('/atividade/concluir/<int:id>', methods=['POST'])
def atividadeConcluir(id):
    atividade = Atividade.query.get(id)
    if atividade:
        db.session.delete(atividade)
        db.session.commit()
    return redirect(request.referrer)



