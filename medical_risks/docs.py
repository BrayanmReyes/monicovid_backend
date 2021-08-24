from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields

comorbidity_namespace = Namespace('comorbidities', description='Comorbidities operations', decorators=[cross_origin(),
                                                                                                       jwt_required()])
symptom_namespace = Namespace('symptoms', description='Symptoms operations', decorators=[cross_origin(),
                                                                                         jwt_required()])

comorbidity_response = comorbidity_namespace.model('ComorbidityResponse', {
    'id': fields.Integer,
    'name': fields.String
})

symptom_response = symptom_namespace.model('SymptomResponse', {
    'id': fields.Integer,
    'name': fields.String,
})
