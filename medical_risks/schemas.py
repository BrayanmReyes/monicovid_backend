from settings.layers.serialization import ma
from medical_risks.models import Comorbidity, Symptom


class ComorbiditySchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = Comorbidity


class SymptomSchema(ma.Schema):
    class Meta:
        fields = ("id", "name")
        model = Symptom
