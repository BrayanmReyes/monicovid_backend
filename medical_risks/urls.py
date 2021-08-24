from flask import Blueprint
from flask_restx import Api
from medical_risks.resources import comorbidity_namespace, symptom_namespace
medical_risks_blueprint = Blueprint('medical_risks_api', __name__, url_prefix='/medical-risks-api')
api = Api(medical_risks_blueprint, title='Medical Risks API', description='A medical risks api', doc='/doc')

api.add_namespace(comorbidity_namespace)
api.add_namespace(symptom_namespace)
