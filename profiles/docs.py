from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields

user_namespace = Namespace('users', description='User operations', decorators=[cross_origin(), jwt_required()])
patient_namespace = Namespace('patients', description='Patient operations', decorators=[cross_origin(), jwt_required()])
contact_namespace = Namespace('contacts', description='Contact operations', decorators=[cross_origin(), jwt_required()])

user_response = user_namespace.model('UserResponse', {
    'id': fields.Integer,
    'email': fields.String,
    'type': fields.String
})

patient_request = user_namespace.model('PatientRequest', {
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'password': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'dni': fields.String,
    'username': fields.String,
    'recovered': fields.Boolean,
    'comorbidities': fields.List(fields.Integer)
})

patient_response = user_namespace.model('PatientResponse', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'address': fields.String,
    'dni': fields.String,
    'username': fields.String,
    'recovered': fields.Boolean
})

contact_request = contact_namespace.model('ContactRequest', {
    'name': fields.String(required=True),
    'email': fields.String(required=True),
    'phone': fields.String(required=True)
})

contact_response = contact_namespace.model('ContactResponse', {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
    'patient': fields.Nested(patient_response)
})

contact_deleted = contact_namespace.model('ContactDeleted', {
    'message': fields.String('The contact was deleted')
})

comorbidity_response = patient_namespace.model('ComorbidityResponse', {
    'id': fields.Integer,
    'name': fields.String
})
