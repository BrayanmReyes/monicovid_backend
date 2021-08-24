from marshmallow import post_load, validates_schema
from settings.exceptions import BadRequestException
from settings.layers.serialization import ma
from medical_monitoring.models import Oxygen, Temperature


class OxygenSchema(ma.Schema):
    class Meta:
        fields = ("id", "value", "register_date")
        model = Oxygen

    @validates_schema()
    def validate_tag(self, data, **kwargs):
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
    def validate_tag(self, data, **kwargs):
        errors = {}
        value = data.get('value', None)
        if value is None:
            errors['value'] = 'Value is required'
        if errors:
            raise BadRequestException(errors)

    @post_load
    def make_oxygen(self, data, **kwargs):
        return Temperature(**data)
