from flask import request
from flask_restx import Resource

from profiles.docs import user_namespace, patient_namespace, contact_namespace, user_response, patient_response,\
    contact_request, contact_response, contact_deleted
from profiles.models import User, Patient, Contact
from profiles.schemas import UserSchema, PatientSchema, ContactSchema
from settings.exceptions import NotFoundException


@user_namespace.route('/<int:user_id>')
class UserDetailResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = UserSchema()

    @staticmethod
    def find_user(user_id):
        user = User.get_by_id(user_id)
        if user is not None:
            return user
        else:
            raise NotFoundException('user', 'id', user_id)

    @user_namespace.response(code=200, description='Success', model=user_response)
    @user_namespace.response(code=404, description='User not found')
    def get(self, user_id):
        user = self.find_user(user_id)
        result = self.schema.dump(user)
        return result, 200


@patient_namespace.route('')
class PatientListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = PatientSchema(many=True)

    @patient_namespace.marshal_list_with(patient_response, code=200, description='Success')
    def get(self):
        patients = Patient.get_all()
        result = self.schema.dump(patients)
        return result, 200


@patient_namespace.route('/<int:patient_id>')
class PatientDetailResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = PatientSchema()

    @staticmethod
    def find_patient(patient_id):
        patient = Patient.get_by_id(patient_id)
        if patient is not None:
            return patient
        else:
            raise NotFoundException('patient', 'id', patient_id)

    @patient_namespace.response(code=200, description='Success', model=patient_response)
    @patient_namespace.response(code=404, description='Patient not found')
    def get(self, patient_id):
        patient = self.find_patient(patient_id)
        result = self.schema.dump(patient)
        return result, 200


@contact_namespace.route('')
@contact_namespace.doc(params={'patient_id': 'Patient Id'})
class ContactListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schemas = ContactSchema(many=True)
        self.schema = ContactSchema()

    @staticmethod
    def find_patient(patient_id):
        patient = Patient.get_by_id(patient_id)
        if patient:
            return True
        else:
            raise NotFoundException('patient', 'id', patient_id)

    @contact_namespace.marshal_list_with(contact_response, code=200, description='Success')
    @contact_namespace.response(code=400, description='Bad Request')
    def get(self):
        params = request.args
        patient_id = int(params.get('patient_id')) if params.get('patient_id') else None
        if self.find_patient(patient_id):
            contacts = Contact.simple_filter(**{'patient_id': patient_id})
            result = self.schemas.dump(contacts)
            return result, 200

    @contact_namespace.expect(contact_request)
    @contact_namespace.response(code=400, description='Bad Request')
    @contact_namespace.response(code=201, description='Success', model=contact_response)
    @contact_namespace.response(code=404, description='Patient not found')
    def post(self):
        data = request.get_json()
        params = request.args
        patient_id = int(params.get('patient_id')) if params.get('patient_id') else None
        contact = self.schema.load(data)
        if self.find_patient(patient_id):
            contact.patient_id = patient_id
            result = self.schema.dump(contact.save())
            return result, 201


@contact_namespace.route('/<int:contact_id>')
class ContactDetailResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ContactSchema()

    @staticmethod
    def find_contact(contact_id):
        contact = Contact.get_by_id(contact_id)
        if contact is not None:
            return contact
        else:
            raise NotFoundException('contact', 'id', contact_id)

    @contact_namespace.response(code=200, description='Success', model=contact_response)
    @contact_namespace.response(code=404, description='Contact not found')
    def get(self, contact_id):
        contact = self.find_contact(contact_id)
        result = self.schema.dump(contact)
        return result, 200

    @contact_namespace.expect(contact_request)
    @contact_namespace.response(code=200, description='Success', model=contact_response)
    @contact_namespace.response(code=404, description='Contact not found')
    def put(self, contact_id):
        data = request.get_json()
        contact = self.find_contact(contact_id)
        contact.name = data.get('name') if data.get('name') else contact.name
        contact.email = data.get('email') if data.get('email') else contact.email
        contact.phone = data.get('phone') if data.get('phone') else contact.phone
        result = self.schema.dump(contact.update())
        return result, 200

    @contact_namespace.response(code=200, description='Success', model=contact_deleted)
    @contact_namespace.response(code=404, description='Contact not found')
    def delete(self, contact_id):
        contact = self.find_contact(contact_id)
        contact.delete()
        return {'message': 'The contact was deleted'}, 200
