from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields

oxygen_namespace = Namespace('oxygens', description='Oxygen operations', decorators=[cross_origin(), jwt_required()])
temperature_namespace = Namespace('temperatures', description='Temperature operations', decorators=[cross_origin(),
                                                                                                    jwt_required()])
health_report_namespace = Namespace('health_reports', description='Health Report operations', decorators=[
    cross_origin(), jwt_required()])

oxygen_request = oxygen_namespace.model('OxygenRequest', {
    'value': fields.Float(required=True)
})

oxygen_response = oxygen_namespace.model('OxygenResponse', {
    'id': fields.Integer,
    'value': fields.Float,
    'register_date': fields.Date
})

temperature_request = temperature_namespace.model('TemperatureRequest', {
    'value': fields.Float(required=True)
})

temperature_response = temperature_namespace.model('TemperatureResponse', {
    'id': fields.Integer,
    'value': fields.Float,
    'register_date': fields.Date
})

health_report_request = health_report_namespace.model('HealthReportRequest', {
    'is_contact_with_infected': fields.Boolean(required=True),
    'observation': fields.String(required=True),
    'symptoms': fields.List(fields.Integer)
})

patient_response = health_report_namespace.model('PatientResponse', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'dni': fields.String,
    'recovered': fields.Boolean
})

symptom_response = health_report_namespace.model('SymptomResponse', {
    'id': fields.Integer,
    'name': fields.String,
})

health_report_response = health_report_namespace.model('HealthReportResponse', {
    'id': fields.Integer,
    'is_contact_with_infected': fields.Boolean,
    'observation': fields.String,
    'register_date': fields.Date,
    'patient': fields.Nested(patient_response),
    'oxygen': fields.Nested(oxygen_response),
    'temperature': fields.Nested(temperature_response),
    'symptoms_quantity': fields.Integer
})
