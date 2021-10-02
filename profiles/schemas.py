from marshmallow import post_load, validates_schema
from settings.exceptions import BadRequestException
from settings.layers.serialization import ma
from profiles.models import User, Doctor, Patient, Contact


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "type")
        model = User


class DoctorSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone", "address", "dni", "speciality")
        model = Doctor


class PatientSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "phone", "address", "dni", "username", "recovered",
                  "recovered_date")
        model = Patient


class ContactSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "phone", "patient")
        model = Contact

    patient = ma.Nested(PatientSchema)

    @validates_schema()
    def validate_contact(self, data, **kwargs):
        errors = {}
        name = data.get('name', None)
        email = data.get('email', None)
        phone = data.get('phone', None)
        if name is None:
            errors['name'] = 'Name is required'
        if email is None:
            errors['email'] = 'Email is required'
        if phone is None:
            errors['phone'] = 'Phone is required'
        if name == '':
            errors['name'] = 'Name must not be blank'
        if email == '':
            errors['email'] = 'Email must not be blank'
        if phone == '':
            errors['phone'] = 'Phone must not be blank'
        if errors:
            raise BadRequestException(errors)

    @post_load
    def make_contact(self, data, **kwargs):
        return Contact(**data)
