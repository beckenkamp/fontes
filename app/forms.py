from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo
from app.models import User

class LoginForm(Form):
    username = TextField('Nome de usuario', validators=[Required()])
    password = PasswordField('Senha', validators=[Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Usuario inexistente!')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Senha invalida!')
            return False

        self.user = user
        return True


class RegisterForm(Form):
    username = TextField('Nome de usuario', validators=[Required()])
    password = PasswordField('Senha', validators=[Required(), EqualTo('confirm')])
    confirm	 = PasswordField('Confirme a senha')


class SourceForm(Form):
    name = TextField('Nome', validators=[Required()])
    specialty = TextField('Especialidade', validators=[Required()], description="Separe mais de um item com virgula")
    time_experience = TextField('Tempo de experiencia', validators=[Required()])
    proof = TextField('Comprovacao', validators=[Required()])
    interview_type = TextField('Como aceita falar', validators=[Required()], description="Separe mais de um item com virgula")
    media_type = TextField('Para quais veiculos aceita falar', validators=[Required()], description="Separe mais de um item com virgula")
    contacts = TextField('Contatos', validators=[Required()], description="Separe mais de um item com virgula")