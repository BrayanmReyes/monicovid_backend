from sqlalchemy import case

from settings.layers.database import db, BaseModel


class User(db.Model, BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    dni = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=True)
    recovered = db.Column(db.String(200), nullable=True)
    type = db.Column(db.String(200), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': case([
            (type == "patient", "patient"),
            (type == "doctor", "doctor")
        ], else_="user")
    }

    def __init__(self, first_name, last_name,  email, password, dni, type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.dni = dni
        self.type = type


class Patient(User):
    __tablename__ = 'patients'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    comorbidity = db.Column(db.String(200), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'patient',
    }


class Doctor(User):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    speciality = db.Column(db.String(200), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'doctor',
    }
