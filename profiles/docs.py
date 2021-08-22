from flask_cors import cross_origin
from flask_restx import Namespace, fields

login_namespace = Namespace('login', description='Authentication operations', decorators=[cross_origin()])
user_namespace = Namespace('users', description='User operations', decorators=[cross_origin()])

login_request = login_namespace.model('LoginRequest', {
   'email': fields.String(required=True),
   'password': fields.String(required=True)
})

login_response = login_namespace.model('LoginResponse', {
    'token': fields.String
})

login_unauthorized = login_namespace.model('Unauthorized', {
   'message': fields.String('The credentials are wrong')
})

user_request = user_namespace.model('UserRequest', {
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'dni': fields.String(required=True),
    'type': fields.String(required=True)
})


user_response = user_namespace.model('UserResponse', {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'email': fields.String,
    'dni': fields.String,
    'type': fields.String
})

forgot_password_request = user_namespace.model('ForgotPasswordRequest', {
    'email': fields.String(required=True)
})

forgot_password_response = user_namespace.model('ForgotPasswordResponse', {
    'message': fields.String('The email has been sent')
})

reset_password_request = user_namespace.model('ResetPasswordRequest', {
    'token': fields.String(required=True),
    'password': fields.String(required=True)
})

reset_password_response = user_namespace.model('ResetPasswordResponse', {
    'message': fields.String('Your password has been changed')
})
