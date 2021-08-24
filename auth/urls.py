from flask import Blueprint
from flask_restx import Api
from auth.resources import auth_namespace
auth_blueprint = Blueprint('auth_api', __name__, url_prefix='/auth-api')
api = Api(auth_blueprint, title='Auth API', description='Auth api', doc='/doc')

api.add_namespace(auth_namespace)
