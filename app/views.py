from flask import render_template, request, flash, redirect, url_for
from app import app, db, lm
from app.models import User
from flask.ext.login import login_required, login_user, logout_user
from app.forms import LoginForm, RegisterForm, SourceForm
from werkzeug.security import generate_password_hash

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html", title="Fontes")

@app.route('/source', methods=['GET', 'POST'])
@login_required
def source():
    form = SourceForm()
    return render_template("source.html", title="Nova Fonte", form=form)

@app.errorhandler(404)
def page_not_found(e):
    return 'Sorry, Nothing found here.', 404


@app.errorhandler(500)
def page_not_found(e):
    return 'Sorry, internal server error: {}'.format(e), 500

@lm.user_loader
def load_user(userid):
    return User.query.filter_by(id=userid).first_or_404()

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first_or_404()
        login_user(user)
        flash("Logged in successfully.")
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("login.html", title="Entrar", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)	
        db.session.add(user)
        db.session.commit()
        flash('Usuario %s criado' % user.username)
    return render_template('register.html', title="Novo Usuario", form=form)