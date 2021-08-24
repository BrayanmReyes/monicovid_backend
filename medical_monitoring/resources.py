from flask import request
from flask_restx import Resource

from medical_monitoring.docs import oxygen_namespace, temperature_namespace, oxygen_request, temperature_request,\
    oxygen_response, temperature_response
from medical_monitoring.schemas import OxygenSchema, TemperatureSchema


@oxygen_namespace.route('')
class OxygenListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = OxygenSchema()

    @oxygen_namespace.expect(oxygen_request)
    @oxygen_namespace.response(code=400, description='Bad Request')
    @oxygen_namespace.response(code=201, description='Success', model=oxygen_response)
    def post(self):
        data = request.get_json()
        oxygen = self.schema.load(data)
        result = self.schema.dump(oxygen.save())
        return result, 201


@temperature_namespace.route('')
class TemperatureListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = TemperatureSchema()

    @oxygen_namespace.expect(temperature_request)
    @oxygen_namespace.response(code=400, description='Bad Request')
    @oxygen_namespace.response(code=201, description='Success', model=temperature_response)
    def post(self):
        data = request.get_json()
        temperature = self.schema.load(data)
        result = self.schema.dump(temperature.save())
        return result, 201
