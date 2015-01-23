from app import db
from werkzeug.security import check_password_hash, generate_password_hash

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class User(Base):
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80), unique=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User %r>' % self.username


class Source(Base):
	name = db.Column(db.String(200))
    specialty = db.Column(db.String(200)) #Área de especialidade
    time_experience = db.Column(db.String(80)) #Tempo de experiência
    proof = db.Column(db.String(500)) #Comprovação - o que faz ser uma boa fonte (ex. coordenador das aulas da única academia em SP especializada em reabilitação de paratletas)
    interview_type = db.Column(db.String(500)) #Como aceita falar (fone, email, pessoalmente, gravação)
    media_type = db.Column(db.String(500)) #Para quais veículos aceita falar (site, revista, jornal, rádio e tv)
    contacts = db.Column(db.String(500)) #Contatos (telefones, email, endereço)

    def __init__(self, name, specialty, time_experience, proof, interview_type, media_type, contacts):
        self.name = name
        self.specialty = specialty
        self.time_experience = time_experience
        self.proof = proof
        self.interview_type = interview_type
        self.media_type = media_type
        self.contacts = contacts

    def __repr__(self):
        return '<User %r>' % self.name


#db.create_all()