from flask_restx import Resource

from medical_risks.docs import comorbidity_namespace, symptom_namespace, comorbidity_response, symptom_response
from medical_risks.models import Comorbidity, Symptom
from medical_risks.schemas import ComorbiditySchema, SymptomSchema


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
