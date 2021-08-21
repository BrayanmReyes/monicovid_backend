from flask import Blueprint
from flask_restx import Api
from profiles.resources import login_namespace, user_namespace
profiles_blueprint = Blueprint('profiles_api', __name__, url_prefix='/profiles-api')
api = Api(profiles_blueprint, title='Accounts API', description='A accounts api', doc='/doc')

api.add_namespace(login_namespace)
api.add_namespace(user_namespace)
