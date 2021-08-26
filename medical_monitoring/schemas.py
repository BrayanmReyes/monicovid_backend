from marshmallow import post_load, validates_schema

from medical_risks.schemas import TemperatureSchema, OxygenSchema
from profiles.schemas import PatientSchema
from settings.exceptions import BadRequestException
from settings.layers.serialization import ma
from medical_monitoring.models import HealthReport


class HealthReportSchema(ma.Schema):
    class Meta:
        fields = ("id", "is_contact_with_infected", "observation", "register_date", "patient", "temperature", "oxygen",
                  "symptoms_quantity")
        model = HealthReport

    patient = ma.Nested(PatientSchema)
    temperature = ma.Nested(TemperatureSchema)
    oxygen = ma.Nested(OxygenSchema)
    symptoms_quantity = ma.Method("get_quantity_of_symptoms")

    def get_quantity_of_symptoms(self, obj):
        symptoms = obj.symptoms.filter().all()
        return len(symptoms)

    @validates_schema()
    def validate_health_report(self, data, **kwargs):
        errors = {}
        is_contact_with_infected = data.get('is_contact_with_infected', None)
        observation = data.get('observation', None)
        if is_contact_with_infected is None:
            errors['is_contact_with_infected'] = 'Is contact with infected is required'
        if observation is None:
            errors['observation'] = 'Observation is required'
        if observation == '':
            errors['observation'] = 'Observation must not be blank'
        if errors:
            raise BadRequestException(errors)

    @post_load
    def make_oxygen(self, data, **kwargs):
        is_contact_with_infected = data['is_contact_with_infected'].lower()
        data['is_contact_with_infected'] = True if is_contact_with_infected == 'true' else False
        return HealthReport(**data)
