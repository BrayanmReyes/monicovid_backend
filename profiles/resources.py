from flask import request
from flask_restx import Resource

from medical_risks.schemas import ComorbiditySchema
from profiles.docs import user_namespace, patient_namespace, doctor_namespace, contact_namespace, user_response,\
    doctor_request, doctor_response, patient_request, patient_response, contact_request, contact_response,\
    contact_deleted, comorbidity_response
from profiles.models import Patient, Contact
from profiles.schemas import UserSchema, DoctorSchema, PatientSchema, ContactSchema
from profiles.services import get_param, get_variable, find_user, find_doctor, find_patient, find_contact,\
    update_doctor, update_patient


@user_namespace.route('/<int:user_id>')
class UserDetailResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = UserSchema()

    @user_namespace.response(code=200, description='Success', model=user_response)
    @user_namespace.response(code=404, description='User not found')
    def get(self, user_id):
        user = find_user(user_id)
        result = self.schema.dump(user)
        return result, 200


@doctor_namespace.route('/<int:doctor_id>')
class DoctorDetailResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = DoctorSchema()

    @doctor_namespace.response(code=200, description='Success', model=doctor_response)
    @doctor_namespace.response(code=404, description='Doctor not found')
    def get(self, doctor_id):
        doctor = find_doctor(doctor_id)
        result = self.schema.dump(doctor)
        return result, 200

    @doctor_namespace.expect(doctor_request)
    @doctor_namespace.response(code=200, description='Success', model=doctor_response)
    @doctor_namespace.response(code=404, description='Doctor not found')
    def put(self, doctor_id):
        data = request.get_json()
        doctor = update_doctor(find_doctor(doctor_id), data)
        result = self.schema.dump(doctor)
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

    @patient_namespace.response(code=200, description='Success', model=patient_response)
    @patient_namespace.response(code=404, description='Patient not found')
    def get(self, patient_id):
        patient = find_patient(patient_id)
        result = self.schema.dump(patient)
        return result, 200

    @contact_namespace.expect(patient_request)
    @contact_namespace.response(code=200, description='Success', model=patient_response)
    @contact_namespace.response(code=404, description='Patient not found')
    def put(self, patient_id):
        data = request.get_json()
        comorbidities = data.get('comorbidities', None)
        patient = update_patient(find_patient(patient_id), data, comorbidities)
        result = self.schema.dump(patient)
        return result, 200


@patient_namespace.route('/<int:patient_id>/comorbidities')
class ComorbiditiesByPatientResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schemas = ComorbiditySchema(many=True)

    @patient_namespace.response(code=404, description='Patient not found')
    @patient_namespace.marshal_list_with(comorbidity_response, code=200, description='Success')
    def get(self, patient_id):
        patient = find_patient(patient_id)
        comorbidities = patient.comorbidities.filter().all()
        result = self.schemas.dump(comorbidities)
        return result, 200


@contact_namespace.route('')
@contact_namespace.doc(params={'patient_id': 'Patient Id'})
class ContactListResource(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schemas = ContactSchema(many=True)
        self.schema = ContactSchema()

    @contact_namespace.marshal_list_with(contact_response, code=200, description='Success')
    @contact_namespace.response(code=400, description='Bad Request')
    def get(self):
        params = request.args
        patient_id = get_param(params, 'patient_id')
        if find_patient(patient_id):
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
        patient_id = get_param(params, 'patient_id')
        contact = self.schema.load(data)
        if find_patient(patient_id):
            contact.patient_id = patient_id
            result = self.schema.dump(contact.save())
            return result, 201


@contact_namespace.route('/<int:contact_id>')
class ContactDetailResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schema = ContactSchema()

    @contact_namespace.response(code=200, description='Success', model=contact_response)
    @contact_namespace.response(code=404, description='Contact not found')
    def get(self, contact_id):
        contact = find_contact(contact_id)
        result = self.schema.dump(contact)
        return result, 200

    @contact_namespace.expect(contact_request)
    @contact_namespace.response(code=200, description='Success', model=contact_response)
    @contact_namespace.response(code=404, description='Contact not found')
    def put(self, contact_id):
        data = request.get_json()
        contact = find_contact(contact_id)
        contact.name = get_variable(data, 'name', contact.name)
        contact.email = get_variable(data, 'email', contact.email)
        contact.phone = get_variable(data, 'phone', contact.phone)
        result = self.schema.dump(contact.update())
        return result, 200

    @contact_namespace.response(code=200, description='Success', model=contact_deleted)
    @contact_namespace.response(code=404, description='Contact not found')
    def delete(self, contact_id):
        contact = find_contact(contact_id)
        contact.delete()
        return {'message': 'The contact was deleted'}, 200
