from flask import Blueprint
from flask_restx import Api
from profiles.resources import user_namespace, patient_namespace, contact_namespace
profiles_blueprint = Blueprint('profiles_api', __name__, url_prefix='/profiles-api')
api = Api(profiles_blueprint, title='Accounts API', description='A accounts api', doc='/doc')

api.add_namespace(user_namespace)
api.add_namespace(patient_namespace)
api.add_namespace(contact_namespace)
