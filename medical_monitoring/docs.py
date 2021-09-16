from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields

health_report_namespace = Namespace('health_reports', description='Health Report operations', decorators=[
    cross_origin(), jwt_required()])
monitoring_namespace = Namespace('monitoring', description='Monitoring operations', decorators=[cross_origin(),
                                                                                                jwt_required()])
health_report_request = health_report_namespace.model('HealthReportRequest', {
    'is_contact_with_infected': fields.Boolean(required=True),
    'observation': fields.String(required=True),
    'symptoms': fields.List(fields.Integer)
})

doctor_response = monitoring_namespace.model('DoctorResponse', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'dni': fields.String,
    'speciality': fields.String
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

oxygen_response = health_report_namespace.model('OxygenResponse', {
    'id': fields.Integer,
    'value': fields.Float,
    'register_date': fields.DateTime
})

temperature_response = health_report_namespace.model('TemperatureResponse', {
    'id': fields.Integer,
    'value': fields.Float,
    'register_date': fields.DateTime
})

symptom_response = health_report_namespace.model('SymptomResponse', {
    'id': fields.Integer,
    'name': fields.String,
})

health_report_response = health_report_namespace.model('HealthReportResponse', {
    'id': fields.Integer,
    'is_contact_with_infected': fields.Boolean,
    'observation': fields.String,
    'register_date': fields.DateTime,
    'patient': fields.Nested(patient_response),
    'oxygen': fields.Nested(oxygen_response),
    'temperature': fields.Nested(temperature_response),
    'symptoms_quantity': fields.Integer,
    'delicate_health': fields.Boolean
})

monitoring_request = monitoring_namespace.model('MonitoringRequest', {
    'doctor_id': fields.Integer(required=True),
    'patient_id': fields.Integer(required=True)
})

monitoring_response = monitoring_namespace.model('MonitoringResponse', {
    'doctor_id': fields.Integer,
    'doctor': fields.Nested(doctor_response),
    'patient_id': fields.Integer,
    'patient': fields.Nested(patient_response),
    'is_active': fields.Boolean,
    'start_date': fields.DateTime,
    'end_date': fields.Date
})

deleted_monitoring = monitoring_namespace.model('DeletedMonitoring', {
    'message': fields.String('The monitoring was deleted')
})
