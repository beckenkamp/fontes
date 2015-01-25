from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo
from app.models import User

class LoginForm(Form):
    username = TextField(u'Nome de usuário', validators=[Required()])
    password = PasswordField(u'Senha', validators=[Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append(u'Usuário inexistente!')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append(u'Senha inválida!')
            return False

        self.user = user
        return True


class RegisterForm(Form):
    username = TextField(u'Nome de usuário', validators=[Required()])
    password = PasswordField(u'Senha', validators=[Required(), EqualTo('confirm')])
    confirm	 = PasswordField(u'Confirme a senha')


class SourceForm(Form):
    name = TextField(u'Nome', validators=[Required()])
    specialty = TextField(u'Especialidade', validators=[Required()], description=u"Separe mais de um item com vírgula")
    time_experience = TextField(u'Tempo de experiência', validators=[Required()])
    proof = TextField(u'Comprovação', validators=[Required()])
    interview_type = TextField(u'Como aceita falar', validators=[Required()], description=u"Separe mais de um item com vírgula")
    media_type = TextField(u'Para quais veículos aceita falar', validators=[Required()], description=u"Separe mais de um item com vírgula")
    contacts = TextField(u'Contatos', validators=[Required()], description=u"Separe mais de um item com vírgula")