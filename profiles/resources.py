import datetime

from flask import request, make_response
from flask_jwt_extended import jwt_required, create_access_token
from flask_restx import Resource
from werkzeug.security import check_password_hash

from profiles.docs import login_namespace, user_namespace, user_response, user_request, login_response, login_request,\
    login_unauthorized
from profiles.models import User
from profiles.schemas import UserSchema, LoginSchema


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
            return make_response({'token': token}, 201)
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
        filters = {'email': email}
        user = User.get_one(**filters)
        if not user:
            user = self.schema.load(data)
            result = self.schema.dump(user.save())
            return result, 201
        else:
            return make_response({'message': 'User already exists. Please Log in'}, 202)
