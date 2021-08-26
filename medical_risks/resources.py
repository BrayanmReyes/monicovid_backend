from flask import request
from flask_restx import Resource

from medical_risks.services import get_param
from profiles.services import find_patient
from settings.layers.database import db
from medical_risks.docs import comorbidity_namespace, symptom_namespace, oxygen_namespace, temperature_namespace, \
    oxygen_request, temperature_request, comorbidity_response, symptom_response, oxygen_response, temperature_response
from medical_risks.models import Comorbidity, Symptom, Oxygen, Temperature
from profiles.models import Patient
from medical_monitoring.models import HealthReport
from medical_risks.schemas import ComorbiditySchema, SymptomSchema, OxygenSchema, TemperatureSchema


@comorbidity_namespace.route('')
class ComorbidityListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ComorbiditySchema(many=True)

    @comorbidity_namespace.marshal_list_with(comorbidity_response, code=200, description='Success')
    def get(self):
        comorbidities = Comorbidity.get_all()
        result = self.schema.dump(comorbidities)
        return result, 200


@symptom_namespace.route('')
class SymptomListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = SymptomSchema(many=True)

    @symptom_namespace.marshal_list_with(symptom_response, code=200, description='Success')
    def get(self):
        symptoms = Symptom.get_all()
        result = self.schema.dump(symptoms)
        return result, 200


@oxygen_namespace.route('')
class OxygenListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = OxygenSchema()

    @oxygen_namespace.expect(oxygen_request)
    @oxygen_namespace.response(code=400, description='Bad Request')
    @oxygen_namespace.response(code=201, description='Success', model=oxygen_response)
    def post(self):
        data = request.get_json()
        oxygen = self.schema.load(data)
        result = self.schema.dump(oxygen.save())
        return result, 201


@oxygen_namespace.route('/reports')
@oxygen_namespace.doc(params={'patient_id': 'Patient Id'})
class OxygenReportResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = OxygenSchema(many=True)

    @oxygen_namespace.response(code=400, description='Bad Request')
    @oxygen_namespace.marshal_list_with(oxygen_response, code=200, description='Success')
    def get(self):
        params = request.args
        patient_id = get_param(params, 'patient_id')
        if find_patient(patient_id):
            query = db.session.query(Oxygen).join(HealthReport).join(Patient)
            query = query.filter(Patient.id == patient_id)
            result = self.schema.dump(query)
            return result, 200


@temperature_namespace.route('')
class TemperatureListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = TemperatureSchema()

    @oxygen_namespace.expect(temperature_request)
    @oxygen_namespace.response(code=400, description='Bad Request')
    @oxygen_namespace.response(code=201, description='Success', model=temperature_response)
    def post(self):
        data = request.get_json()
        temperature = self.schema.load(data)
        result = self.schema.dump(temperature.save())
        return result, 201


@temperature_namespace.route('/reports')
@temperature_namespace.doc(params={'patient_id': 'Patient Id'})
class TemperatureReportResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = TemperatureSchema(many=True)

    @temperature_namespace.response(code=400, description='Bad Request')
    @temperature_namespace.marshal_list_with(temperature_response, code=200, description='Success')
    def get(self):
        params = request.args
        patient_id = get_param(params, 'patient_id')
        if find_patient(patient_id):
            query = db.session.query(Temperature).join(HealthReport).join(Patient)
            query = query.filter(Patient.id == patient_id)
            result = self.schema.dump(query)
            return result, 200
