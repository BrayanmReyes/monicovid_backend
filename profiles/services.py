from medical_risks.services import find_comorbidity
from profiles.models import User, Doctor, Patient, Contact
from werkzeug.security import generate_password_hash
from settings.exceptions import NotFoundException, EmailException


def get_param(params, search):
    return int(params.get(search)) if params.get(search) else None


def get_variable(data, search, default):
    return data.get(search) if data.get(search) else default


def get_verify_email(data, search, default):
    if data.get(search):
        email = data.get(search)
        if email == default:
            return default
        else:
            user = User.get_one(**{'email': email})
            if not user:
                return email
            else:
                raise EmailException()
    else:
        return default


def get_hashed_password(data, search, default):
    return generate_password_hash(data.get(search)) if data.get(search) else default


def get_boolean_variable(data, search, default):
    if data.get(search):
        is_recovered = data.get(search).lower()
        return True if is_recovered == 'true' else False
    else:
        return default


def find_user(user_id):
    user = User.get_by_id(user_id)
    if user:
        return user
    else:
        raise NotFoundException('user', 'id', user_id)


def find_doctor(doctor_id):
    doctor = Doctor.get_by_id(doctor_id)
    if doctor:
        return doctor
    else:
        raise NotFoundException('doctor', 'id', doctor_id)


def find_patient(patient_id):
    patient = Patient.get_by_id(patient_id)
    if patient:
        return patient
    else:
        raise NotFoundException('patient', 'id', patient_id)


def find_contact(contact_id):
    contact = Contact.get_by_id(contact_id)
    if contact:
        return contact
    else:
        raise NotFoundException('contact', 'id', contact_id)


def update_doctor(doctor, data):
    doctor.first_name = get_variable(data, 'first_name', doctor.first_name)
    doctor.last_name = get_variable(data, 'last_name', doctor.last_name)
    doctor.email = get_verify_email(data, 'email', doctor.email)
    doctor.password = get_hashed_password(data, 'password', doctor.password)
    doctor.phone = get_variable(data, 'phone', doctor.phone)
    doctor.address = get_variable(data, 'address', doctor.address)
    doctor.dni = get_variable(data, 'dni', doctor.dni)
    doctor.speciality = get_variable(data, 'speciality', doctor.speciality)
    return doctor.update()


def compare(patient, list_new, list_own):
    set_new = set(list_new)
    set_own = set(list_own)
    if set_new == set_own:
        print('IS THE SAME')
    else:
        if len(set_own) > len(set_new):
            set_minus = set_own - set_new
            for minus in set_minus:
                patient.comorbidities.remove(minus)
        else:
            set_plus = set_new - set_own
            for plus in set_plus:
                patient.comorbidities.append(plus)
            set_minus = set_own - set_new
            for minus in set_minus:
                patient.comorbidities.remove(minus)

        patient.commit()


def update_comorbidities(patient, comorbidity_ids):
    comorbidities = []
    if comorbidity_ids is not None:
        for comorbidity_id in comorbidity_ids:
            comorbidity = find_comorbidity(comorbidity_id)
            comorbidities.append(comorbidity)
        comorbidities_from_patient = patient.comorbidities.filter().all()
        if len(comorbidities_from_patient) == 0:
            for comorbidity in comorbidities:
                patient.comorbidities.append(comorbidity)
                patient.commit()
        else:
            compare(patient, comorbidities, comorbidities_from_patient)
    return patient


def update_patient(patient, data, comorbidity_ids):
    patient.first_name = get_variable(data, 'first_name', patient.first_name)
    patient.last_name = get_variable(data, 'last_name', patient.last_name)
    patient.email = get_verify_email(data, 'email', patient.email)
    patient.password = get_hashed_password(data, 'password', patient.password)
    patient.phone = get_variable(data, 'phone', patient.phone)
    patient.address = get_variable(data, 'address', patient.address)
    patient.dni = get_variable(data, 'dni', patient.dni)
    patient.username = get_variable(data, 'username', patient.username)
    patient.recovered = get_boolean_variable(data, 'recovered', patient.recovered)
    return update_comorbidities(patient.update(), comorbidity_ids)
