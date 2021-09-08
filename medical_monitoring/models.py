from sqlalchemy.orm import backref

from settings.layers.database import db, BaseModel
from sqlalchemy.sql import func


class HealthReport(db.Model, BaseModel):
    __tablename__ = 'health_reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_contact_with_infected = db.Column(db.Boolean, nullable=False)
    observation = db.Column(db.String(255), nullable=False)
    register_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    patient = db.relationship("Patient")
    oxygen_id = db.Column(db.Integer, db.ForeignKey('oxygens.id'))
    oxygen = db.relationship("Oxygen", backref=backref("health_reports", uselist=False))
    temperature_id = db.Column(db.Integer, db.ForeignKey('temperatures.id'))
    temperature = db.relationship("Temperature", backref=backref("health_reports", uselist=False))
    symptoms = db.relationship("Symptom", secondary=lambda: health_reports_symptoms, lazy='dynamic',
                               backref=backref("health_reports", lazy='dynamic'))

    def __init__(self, is_contact_with_infected, observation):
        self.is_contact_with_infected = is_contact_with_infected
        self.observation = observation


class Monitoring(db.Model, BaseModel):
    __tablename__ = 'monitoring'

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    doctor = db.relationship("Doctor", back_populates="monitoring")
    patient = db.relationship("Patient", back_populates="monitoring")
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    start_date = db.Column(db.DateTime(timezone=True), default=func.now(), nullable=False)
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)

    def __init__(self, doctor_id, patient_id):
        self.doctor_id = doctor_id
        self.patient_id = patient_id


health_reports_symptoms = db.Table('health_reports_symptoms', db.metadata,
                                   db.Column('health_report_id', db.ForeignKey('health_reports.id'), primary_key=True),
                                   db.Column('symptom_id', db.ForeignKey('symptoms.id'), primary_key=True)
                                   )
