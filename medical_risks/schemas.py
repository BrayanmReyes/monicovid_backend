from marshmallow import validates_schema, post_load

from settings.exceptions import BadRequestException
from settings.layers.serialization import ma
from medical_risks.models import Comorbidity, Symptom, Oxygen, Temperature


class ComorbiditySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = Comorbidity


class SymptomSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = Symptom


class OxygenSchema(ma.Schema):
    class Meta:
        fields = ("id", "value", "register_date")
        model = Oxygen

    @validates_schema()
    def validate_oxygen(self, data, **kwargs):
        errors = {}
        value = data.get('value', None)
        if value is None:
            errors['value'] = 'Value is required'
        if errors:
            raise BadRequestException(errors)

    @post_load
    def make_oxygen(self, data, **kwargs):
        return Oxygen(**data)


class TemperatureSchema(ma.Schema):
    class Meta:
        fields = ("id", "value", "register_date")
        model = Temperature

    @validates_schema()
    def validate_temperature(self, data, **kwargs):
        errors = {}
        value = data.get('value', None)
        if value is None:
            errors['value'] = 'Value is required'
        if errors:
            raise BadRequestException(errors)

    @post_load
    def make_oxygen(self, data, **kwargs):
        return Temperature(**data)
