from flask import request
from flask_restx import Resource
from medical_monitoring.docs import health_report_namespace, health_report_request, health_report_response,\
    symptom_response
from medical_monitoring.models import HealthReport
from medical_monitoring.schemas import HealthReportSchema
from medical_monitoring.services import get_param, find_health_report, save_health_report
from medical_risks.schemas import SymptomSchema
from profiles.services import find_patient


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
            contacts = HealthReport.simple_filter(**{'patient_id': patient_id})
            result = self.schemas.dump(contacts)
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
