from sqlalchemy.orm import backref

from settings.layers.database import db, BaseModel
from sqlalchemy.sql import func


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


# class HealthReport(db.Model, BaseModel):
#     __tablename__ = 'health_reports'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     is_contact_with_infected = db.Column(db.Boolean, nullable=False)
#     observation = db.Column(db.String(255), nullable=False)
#     register_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
#     patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
#     patient = db.relationship("Patient")
#     oxygen_id = db.Column(db.Integer, db.ForeignKey('oxygens.id'), nullable=False)
#     oxygen = db.relationship("Oxygen", backref=backref("health_reports", uselist=False))
#     temperature_id = db.Column(db.Integer, db.ForeignKey('temperatures.id'), nullable=False)
#     temperature = db.relationship("Temperature", backref=backref("health_reports", uselist=False))
#
#     def __init__(self, is_contact_with_infected, observation):
#         self.is_contact_with_infected = is_contact_with_infected
#         self.observation = observation
