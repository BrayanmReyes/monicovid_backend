from flask_cors import cross_origin
from flask_restx import Namespace, fields

auth_namespace = Namespace('', description='Authentication operations', decorators=[cross_origin()])

login_request = auth_namespace .model('LoginRequest', {
   'email': fields.String(required=True),
   'password': fields.String(required=True)
})

login_response = auth_namespace .model('LoginResponse', {
    'token': fields.String
})

login_unauthorized = auth_namespace .model('Unauthorized', {
   'message': fields.String('The credentials are wrong')
})

register_request = auth_namespace .model('RegisterRequest', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'dni': fields.String(required=True),
    'type': fields.String(required=True)
})

register_response = auth_namespace .model('RegisterResponse', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'dni': fields.String,
    'type': fields.String
})

forgot_password_request = auth_namespace .model('ForgotPasswordRequest', {
    'email': fields.String(required=True)
})

forgot_password_response = auth_namespace .model('ForgotPasswordResponse', {
    'message': fields.String('The email has been sent')
})

reset_password_request = auth_namespace .model('ResetPasswordRequest', {
    'token': fields.String(required=True),
    'password': fields.String(required=True)
})

reset_password_response = auth_namespace .model('ResetPasswordResponse', {
    'message': fields.String('Your password has been changed')
})
