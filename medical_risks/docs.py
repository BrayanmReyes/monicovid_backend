from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields

comorbidity_namespace = Namespace('comorbidities', description='Comorbidities operations', decorators=[cross_origin(),
                                                                                                       jwt_required()])
symptom_namespace = Namespace('symptoms', description='Symptoms operations', decorators=[cross_origin(),
                                                                                         jwt_required()])
oxygen_namespace = Namespace('oxygens', description='Oxygen operations', decorators=[cross_origin(), jwt_required()])
temperature_namespace = Namespace('temperatures', description='Temperature operations', decorators=[cross_origin(),
                                                                                                    jwt_required()])

comorbidity_response = comorbidity_namespace.model('ComorbidityResponse', {
    'id': fields.Integer,
    'name': fields.String
})

symptom_response = symptom_namespace.model('SymptomResponse', {
    'id': fields.Integer,
    'name': fields.String,
})

oxygen_request = oxygen_namespace.model('OxygenRequest', {
    'value': fields.Float(required=True)
})

oxygen_response = oxygen_namespace.model('OxygenResponse', {
    'id': fields.Integer,
    'value': fields.Float,
    'register_date': fields.DateTime
})

temperature_request = temperature_namespace.model('TemperatureRequest', {
    'value': fields.Float(required=True)
})

temperature_response = temperature_namespace.model('TemperatureResponse', {
    'id': fields.Integer,
    'value': fields.Float,
    'register_date': fields.DateTime
})
