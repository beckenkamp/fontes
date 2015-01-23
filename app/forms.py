from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, EqualTo
from models import User

class LoginForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required()])

    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append('Usuario inexsitente!')
            return False

        if not user.check_password(self.password.data):
            self.password.errors.append('Senha invalida!')
            return False

        self.user = user
        return True

class RegisterForm(Form):
    username = TextField('username', validators=[Required()])
    password = PasswordField('password', validators=[Required(), EqualTo('confirm')])
    confirm	 = PasswordField('confirm')