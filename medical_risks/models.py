from sqlalchemy.orm import backref
from sqlalchemy.sql import func
from settings.layers.database import db, BaseModel


class Symptom(db.Model, BaseModel):
    __tablename__ = 'symptoms'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))

    def __init__(self, name):
        self.name = name


class Comorbidity(db.Model, BaseModel):
    __tablename__ = 'comorbidities'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    patients = db.relationship("Patient", secondary=lambda: patients_comorbidities, lazy='dynamic',
                               backref=backref("comorbidities", lazy='dynamic'))

    def __init__(self, name):
        self.name = name


class Oxygen(db.Model, BaseModel):
    __tablename__ = 'oxygens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    register_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __init__(self, value):
        self.value = value


class Temperature(db.Model, BaseModel):
    __tablename__ = 'temperatures'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.Float, nullable=False)
    register_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)

    def __init__(self, value):
        self.value = value


patients_comorbidities = db.Table('patients_comorbidities', db.metadata,
                                  db.Column('patient_id', db.ForeignKey('patients.id'), primary_key=True),
                                  db.Column('comorbidity_id', db.ForeignKey('comorbidities.id'), primary_key=True)
                                  )
