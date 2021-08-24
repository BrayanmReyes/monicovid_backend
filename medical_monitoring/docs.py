from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields

oxygen_namespace = Namespace('oxygens', description='Oxygen operations', decorators=[cross_origin(), jwt_required()])
temperature_namespace = Namespace('temperatures', description='Temperature operations', decorators=[cross_origin(),
                                                                                                    jwt_required()])

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
