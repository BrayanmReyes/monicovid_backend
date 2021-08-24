from flask import Blueprint
from flask_restx import Api
from medical_monitoring.resources import oxygen_namespace, temperature_namespace
medical_monitoring_blueprint = Blueprint('medical_monitoring_api', __name__, url_prefix='/medical-monitoring-api')
api = Api(medical_monitoring_blueprint, title='Medical Monitoring API', description='A medical monitoring api',
          doc='/doc')

api.add_namespace(oxygen_namespace)
api.add_namespace(temperature_namespace)
