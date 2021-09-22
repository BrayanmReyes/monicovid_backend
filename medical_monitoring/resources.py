from flask import request
from flask_restx import Resource
from sqlalchemy import func

from medical_monitoring.docs import health_report_namespace, monitoring_namespace, health_report_request, \
    monitoring_request, health_report_response, monitoring_response, symptom_response, patient_response, \
    deleted_monitoring
from medical_monitoring.models import HealthReport, Monitoring
from medical_monitoring.schemas import HealthReportSchema, MonitoringSchema
from medical_monitoring.services import get_param, find_health_report, save_health_report, create_monitoring, \
    get_last_health_report, find_monitoring
from medical_risks.schemas import SymptomSchema
from profiles.models import Patient, Doctor
from profiles.schemas import PatientSchema
from profiles.services import find_doctor, find_patient
from settings.layers.database import db


@health_report_namespace.route('')
@health_report_namespace.doc(params={'patient_id': 'Patient Id'})
class HealthReportListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schemas = HealthReportSchema(many=True)
        self.schema = HealthReportSchema()

    @health_report_namespace.response(code=400, description='Bad Request')
    @health_report_namespace.marshal_list_with(health_report_response, code=200, description='Success')
    def get(self):
        params = request.args
        patient_id = get_param(params, 'patient_id')
        if find_patient(patient_id):
            health_reports = HealthReport.simple_filter(**{'patient_id': patient_id})
            result = self.schemas.dump(health_reports)
            return result, 200

    @health_report_namespace.expect(health_report_request)
    @health_report_namespace.response(code=400, description='Bad Request')
    @health_report_namespace.response(code=201, description='Success', model=health_report_response)
    @health_report_namespace.doc(params={'temperature_id': 'Temperature Id'})
    @health_report_namespace.doc(params={'oxygen_id': 'Oxygen Id'})
    def post(self):
        data = request.get_json()
        params = request.args
        patient_id = get_param(params, 'patient_id')
        temperature_id = get_param(params, 'temperature_id')
        oxygen_id = get_param(params, 'oxygen_id')
        symptoms = data.get('symptoms', None)
        if find_patient(patient_id):
            if symptoms is not None:
                del data['symptoms']
            health_report = save_health_report(self.schema.load(data), patient_id, oxygen_id, temperature_id, symptoms)
            result = self.schema.dump(health_report)
            return result, 201


@health_report_namespace.route('/last-report')
@health_report_namespace.doc(params={'patient_id': 'Patient Id'})
class LastReportResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = HealthReportSchema()

    @health_report_namespace.response(code=400, description='Bad Request')
    @health_report_namespace.response(code=200, description='Success', model=health_report_response)
    def get(self):
        params = request.args
        patient_id = get_param(params, 'patient_id')
        if find_patient(patient_id):
            health_report = get_last_health_report(patient_id)
            result = self.schema.dump(health_report)
            return result, 200


@health_report_namespace.route('/<int:health_report_id>/symptoms')
class SymptomsByHealthReportResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schemas = SymptomSchema(many=True)

    @health_report_namespace.response(code=404, description='HealthReport not found')
    @health_report_namespace.marshal_list_with(symptom_response, code=200, description='Success')
    def get(self, health_report_id):
        health_report = find_health_report(health_report_id)
        symptoms = health_report.symptoms.filter().all()
        result = self.schemas.dump(symptoms)
        return result, 200


@monitoring_namespace.route('')
class MonitoringListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = MonitoringSchema()

    @monitoring_namespace.expect(monitoring_request)
    @monitoring_namespace.response(code=400, description='Bad Request')
    @monitoring_namespace.response(code=201, description='Success', model=monitoring_response)
    def post(self):
        data = request.get_json()
        patient_id = data.get('patient_id', None)
        doctor_id = data.get('doctor_id', None)
        if find_patient(patient_id) and find_doctor(doctor_id):
            monitoring = create_monitoring(self.schema.load(data))
            result = self.schema.dump(monitoring)
            return result, 201

    @monitoring_namespace.expect(monitoring_request)
    @monitoring_namespace.response(code=400, description='Bad Request')
    @monitoring_namespace.response(code=200, description='Success', model=deleted_monitoring)
    def delete(self):
        data = request.get_json()
        patient_id = data.get('patient_id', None)
        doctor_id = data.get('doctor_id', None)
        if find_patient(patient_id) and find_doctor(doctor_id):
            monitoring = find_monitoring(doctor_id, patient_id)
            monitoring.is_active = False
            monitoring.end_date = func.now()
            monitoring.commit()
            return {'message': 'The monitoring was deleted'}, 200


@monitoring_namespace.route('/patients')
@monitoring_namespace.doc(params={'doctor_id': 'Doctor Id'})
class PatientByMonitoringResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = PatientSchema(many=True)

    @monitoring_namespace.response(code=400, description='Bad Request')
    @monitoring_namespace.marshal_list_with(patient_response, code=200, description='Success')
    def get(self):
        params = request.args
        doctor_id = get_param(params, 'doctor_id')
        if find_doctor(doctor_id):
            query = db.session.query(Patient).join(Monitoring).join(Doctor)
            query = query.filter(Doctor.id == doctor_id, Monitoring.is_active is True)
            result = self.schema.dump(query)
            return result, 200
