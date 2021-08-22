import datetime

from flask import request, make_response
from flask_jwt_extended import jwt_required, create_access_token
from flask_restx import Resource
from werkzeug.security import check_password_hash, generate_password_hash

from profiles.docs import login_namespace, user_namespace, user_request, user_response, login_request, login_response, \
    login_unauthorized, forgot_password_request, forgot_password_response, reset_password_request, \
    reset_password_response
from profiles.models import User
from profiles.schemas import UserSchema, LoginSchema
from profiles.utils import encrypt_data, decrypt_data
from settings.layers.mail import send_email


@login_namespace.route('')
class LoginResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = LoginSchema()

    @login_namespace.expect(login_request)
    @login_namespace.response(code=200, description='Success', model=login_response)
    @login_namespace.response(code=401, description='Unauthorized', model=login_unauthorized)
    def post(self):
        data = self.schema.load(request.get_json())
        email = data.get('email')
        password = data.get('password')
        user = User.get_one(**{'email': email})
        if not user:
            return make_response({'message': 'No user found with that email'}, 401)
        if check_password_hash(user.password, password):
            token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=5))
            return make_response({'token': token}, 200)
        return make_response({'message': 'The credentials are wrong'}, 401)


@user_namespace.route('')
class UserListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schemas = UserSchema(many=True)
        self.schema = UserSchema()

    @user_namespace.marshal_list_with(user_response, code=200, description='Success')
    @jwt_required()
    def get(self):
        users = User.get_all()
        result = self.schemas.dump(users)
        return result, 200

    @user_namespace.expect(user_request)
    @user_namespace.response(code=400, description='Bad Request')
    @user_namespace.response(code=200, description='Success', model=user_response)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        user = User.get_one(**{'email': email})
        if not user:
            user = self.schema.load(data)
            result = self.schema.dump(user.save())
            return result, 201
        else:
            return make_response({'message': 'User already exists. Please Log in'}, 202)


@user_namespace.route('/forgot-password')
class ForgotPasswordResource(Resource):

    @user_namespace.expect(forgot_password_request)
    @user_namespace.response(code=400, description='Bad Request')
    @user_namespace.response(code=200, description='Success', model=forgot_password_response)
    def post(self):
        data = request.get_json()
        email = data.get('email')
        user = User.get_one(**{'email': email})
        if user:
            token = encrypt_data(user.email)
            reset_link = f'http://127.0.0.1:3000/?token={token}'
            if send_email('Forgot Password', f'Please, click the link to restore your password: {reset_link}',
                          [user.email]):
                return make_response({'message': 'The email has been sent'}, 200)
            else:
                return make_response({'message': 'Could not sent the email'}, 400)
        else:
            return make_response({'message': 'The user with the given email does not exist'}, 202)


@user_namespace.route('/reset-password')
class ResetPasswordResource(Resource):

    @user_namespace.expect(reset_password_request)
    @user_namespace.response(code=400, description='Bad Request')
    @user_namespace.response(code=200, description='Success', model=reset_password_response)
    def post(self):
        data = request.get_json()
        token = data.get('token')
        password = data.get('password')
        user = User.get_one(**{'email': decrypt_data(token)})
        if user:
            user.password = generate_password_hash(password)
            user.save()
            return make_response({'message': 'Your password has been changed successfully'}, 200)
        else:
            return make_response({'message': 'The entered token is invalid'}, 202)
