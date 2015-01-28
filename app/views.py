from flask import render_template, request, flash, redirect, url_for
from app import app, db, lm
from app.models import User, Source
from flask.ext.login import login_required, login_user, logout_user
from app.forms import LoginForm, RegisterForm, SourceForm
from werkzeug.security import generate_password_hash

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    sources = Source.query.all()
    return render_template("index.html", title=u"Fontes", sources=sources)

@app.route('/source', methods=['GET', 'POST'])
@app.route('/source/<int:id>', methods=['GET', 'POST'])
@login_required
def source(id = None):
    if id:
        source = Source.query.filter_by(id=id).first_or_404()
        form = SourceForm(obj=source)
        title = u"Editar Fonte %s" % source.name
        btn_label = u"Editar"
    else:
        form = SourceForm()
        title = u"Nova Fonte"
        btn_label = u"Criar"

    if form.validate_on_submit() and id == None:
        name = form.name.data
        specialty = form.specialty.data
        time_experience = form.time_experience.data
        proof = form.proof.data
        interview_type = form.interview_type.data
        media_type = form.media_type.data
        contacts = form.contacts.data
        source = Source(name, specialty, time_experience, proof, interview_type, media_type, contacts)
        db.session.add(source)
        db.session.commit()
        flash(u'Fonte %s adicionada com sucesso!' % source.name)
        return redirect(url_for('source'))

    if form.validate_on_submit() and id != None:
        source.name = form.name.data
        source.specialty = form.specialty.data
        source.time_experience = form.time_experience.data
        source.proof = form.proof.data
        source.interview_type = form.interview_type.data
        source.media_type = form.media_type.data
        source.contacts = form.contacts.data
        #source = Source(name, specialty, time_experience, proof, interview_type, media_type, contacts)
        #db.session.add(source)
        db.session.commit()
        flash(u'Fonte %s alterada com sucesso!' % source.name)
        return redirect(url_for('index'))

    return render_template("source.html", title=title, form=form, btn_label=btn_label)

@app.route('/source/delete/<int:id>', methods=['GET'])
@login_required
def delete_source(id):
    if id:
        source = Source.query.filter_by(id=id).first_or_404()
        db.session.delete(source)
        db.session.commit()
        flash(u'Fonte %s removida da base de dados' % source.name)
        return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return u'Ops, nada encontrado aqui.', 404


@app.errorhandler(500)
def page_not_found(e):
    return u'Vish, erro interno do servidor: {}'.format(e), 500

@lm.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first_or_404()

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        login_user(user)
        flash(u"Bem-vindo, %s" % user.username)
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", title=u"Entrar", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)	
        db.session.add(user)
        db.session.commit()
        flash(u'Usuário %s criado' % user.username)
    return render_template('register.html', title=u"Novo Usuário", form=form)