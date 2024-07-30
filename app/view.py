from app import app, db
from flask import render_template, url_for, request, redirect
from app.forms import ComentarioForm, ContatoForm, UserForm, LoginForm, PostForm
from app.forms import ComentarioForm, ContatoForm, UserForm, LoginForm, PostForm, EditPostForm, EditAtividadeForm
from app.models import Comentario, Contato, User, Post, Atividade
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
    return render_template('post_detail.html', obj=obj, form=form)


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

@app.route('/atividade/edit/<int:id>', methods=['GET', 'POST'])
def atividadeEdit(id):
    atividade = Atividade.query.get(id)
    if not atividade:
        return redirect(url_for('PostDetail'))

    form = EditAtividadeForm(obj=atividade)
    if form.validate_on_submit():
        form.save(atividade_id=id)
        return redirect(url_for('PostDetail'))

    return render_template('atividade_edit.html', form=form, atividade=atividade)

